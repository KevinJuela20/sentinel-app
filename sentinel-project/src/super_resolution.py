"""
super_resolution.py
-------------------
Motor de super-resolución IA para Sentinel-2 usando modelos EDSR.

Responsabilidades:
  - Cargar modelos pre-entrenados EDSR (x4 y x2).
  - Escalar imágenes secuencialmente de 128x128 a 1024x1024.
  - Verificar la integridad y dimensiones del resultado.
"""

import logging
import os
import shutil
from pathlib import Path
from typing import Optional
import cv2

logger = logging.getLogger(__name__)

class SuperResEngine:
    def __init__(self, models_dir: Optional[str] = None):
        # Verificar disponibilidad del módulo dnn_superres antes de continuar
        if not hasattr(cv2, "dnn_superres"):
            raise ImportError(
                "El módulo 'cv2.dnn_superres' no está disponible. "
                "Asegúrate de haber instalado 'opencv-contrib-python-headless==4.12.0.88'."
            )
            
        if models_dir is None:
            self.models_dir = Path(__file__).parent.parent / "models"
        else:
            self.models_dir = Path(models_dir)
        self._models_found = False
        self._verify_models()

    def _verify_models(self) -> bool:
        """Verifica que los archivos de modelo existan."""
        path_x4 = self.models_dir / "EDSR_x4.pb"
        path_x2 = self.models_dir / "EDSR_x2.pb"
        self._models_found = path_x4.exists() and path_x2.exists()
        if not self._models_found:
            logger.error("No se encontraron los modelos EDSR en %s", self.models_dir)
        return self._models_found

    def upscale(self, image_path: str, output_path: str) -> bool:
        """
        Aplica el pipeline de escalado: 128 -> (x4) -> 512 -> (x2) -> 1024.
        Siguiendo el patrón de estabilidad recomendado:
        1. Carga x4, procesa.
        2. Carga x2, procesa.
        """
        if not self._models_found:
            if not self._verify_models():
                return False

        path_x4 = str(self.models_dir / "EDSR_x4.pb")
        path_x2 = str(self.models_dir / "EDSR_x2.pb")

        try:
            img = cv2.imread(image_path)
            if img is None:
                logger.error("No se pudo leer la imagen: %s", image_path)
                return False

            # 1. Asegurar tamaño base 128x128
            h, w = img.shape[:2]
            if h != 128 or w != 128:
                logger.debug("Redimensionando imagen base de %dx%d a 128x128", w, h)
                img = cv2.resize(img, (128, 128), interpolation=cv2.INTER_CUBIC)

            # Inicializar motor DNN (se recomienda recrear para asegurar limpieza de estado)
            sr = cv2.dnn_superres.DnnSuperResImpl_create()

            # 2. Paso 1: EDSR x4 (128 -> 512)
            logger.debug("Aplicando modelo EDSR x4...")
            sr.readModel(path_x4)
            sr.setModel("edsr", 4)
            img_512 = sr.upsample(img)
            
            # Validación intermedia
            h512, w512 = img_512.shape[:2]
            if h512 != 512 or w512 != 512:
                logger.error("Fallo en escalado x4: dimensiones obtenidas %dx%d", w512, h512)
                return False

            # 3. Paso 2: EDSR x2 (512 -> 1024)
            logger.debug("Aplicando modelo EDSR x2...")
            sr.readModel(path_x2)
            sr.setModel("edsr", 2)
            result_1024 = sr.upsample(img_512)
            
            # Validación final
            h1024, w1024 = result_1024.shape[:2]
            if h1024 != 1024 or w1024 != 1024:
                logger.error("Fallo en escalado final x2: dimensiones obtenidas %dx%d", w1024, h1024)
                # Forzar redimensionamiento si la diferencia es mínima por bordes, 
                # pero los modelos EDSR deberían ser exactos.
                result_1024 = cv2.resize(result_1024, (1024, 1024), interpolation=cv2.INTER_CUBIC)

            # 4. Guardar resultado
            cv2.imwrite(output_path, result_1024)
            logger.info("Super-resolución completada exitosamente: %s (1024x1024)", Path(output_path).name)
            return True

        except (AttributeError, ImportError) as att_err:
            logger.error("Error de módulo/atributo en OpenCV: %s. Verifica la instalación de opencv-contrib.", att_err)
            return False
        except Exception as exc:
            logger.error("Fallo inesperado en el pipeline de super-resolución: %s", exc)
            return False


def process_super_res_batch(crops_dir: Path, progress_callback=None) -> dict:
    """
    Procesa todos los recortes en una carpeta.
    
    Args:
        crops_dir: Directorio con recortes PNG (ej: .../crops/).
        progress_callback: Función opcional para reportar progreso.
        
    Returns:
        Estadísticas del proceso.
    """
    engine = SuperResEngine()
    if not engine._models_found:
        return {"error": f"Modelos no encontrados en {engine.models_dir}"}
        
    pngs = list(crops_dir.glob("*.png"))
    if not pngs:
        return {"error": "No se encontraron recortes PNG."}
        
    # Crear subcarpeta super_res (hermana de crops o hija de fecha)
    # crops_dir suele ser .../DD/crops/ -> queremos .../DD/super_res/
    sr_dir = crops_dir.parent / "super_res"
    sr_dir.mkdir(exist_ok=True)
    
    stats = {"total": len(pngs), "processed": 0, "errors": 0}
    
    for idx, png_path in enumerate(pngs):
        output_name = png_path.stem + "_SR.png"
        output_path = sr_dir / output_name
        
        success = engine.upscale(str(png_path), str(output_path))
        if success:
            stats["processed"] += 1
        else:
            stats["errors"] += 1
            
        if progress_callback:
            progress_callback(idx + 1, len(pngs), png_path.name)
            
    # Task 2.1: Limpiar carpeta de recortes si el proceso fue exitoso
    if stats["errors"] == 0 and stats["processed"] > 0:
        try:
            logger.info("Limpiando carpeta de recortes: %s", crops_dir)
            shutil.rmtree(crops_dir)
        except Exception as e:
            logger.warning("No se pudo eliminar la carpeta de recortes: %s", e)

    return stats
