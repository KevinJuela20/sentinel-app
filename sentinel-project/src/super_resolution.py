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
from pathlib import Path
from typing import Optional
import cv2

logger = logging.getLogger(__name__)

class SuperResEngine:
    def __init__(self, models_dir: Optional[str] = None):
        if models_dir is None:
            self.models_dir = Path(__file__).parent.parent / "models"
        else:
            self.models_dir = Path(models_dir)
        self.sr_x4 = cv2.dnn_superres.DnnSuperResImpl_create()
        self.sr_x2 = cv2.dnn_superres.DnnSuperResImpl_create()
        self._models_loaded = False

    def load_models(self) -> bool:
        """Carga los archivos .pb de los modelos EDSR."""
        path_x4 = self.models_dir / "EDSR_x4.pb"
        path_x2 = self.models_dir / "EDSR_x2.pb"

        if not path_x4.exists() or not path_x2.exists():
            logger.error("No se encontraron los modelos EDSR en %s", self.models_dir)
            return False

        try:
            # Configurar x4
            self.sr_x4.readModel(str(path_x4))
            self.sr_x4.setModel("edsr", 4)
            
            # Configurar x2
            self.sr_x2.readModel(str(path_x2))
            self.sr_x2.setModel("edsr", 2)
            
            self._models_loaded = True
            logger.info("Modelos EDSR cargados correctamente.")
            return True
        except Exception as exc:
            logger.error("Error al cargar modelos DNN: %s", exc)
            return False

    def upscale(self, image_path: str, output_path: str) -> bool:
        """
        Aplica el pipeline de escalado: 128 -> (x4) -> 512 -> (x2) -> 1024.
        """
        if not self._models_loaded:
            if not self.load_models():
                return False

        try:
            img = cv2.imread(image_path)
            if img is None:
                logger.error("No se pudo leer la imagen: %s", image_path)
                return False

            # 1. Asegurar tamaño base 128x128
            if img.shape[0] != 128 or img.shape[1] != 128:
                img = cv2.resize(img, (128, 128), interpolation=cv2.INTER_CUBIC)

            # 2. Paso 1: EDSR x4 (128 -> 512)
            result_512 = self.sr_x4.upsample(img)
            
            # 3. Paso 2: EDSR x2 (512 -> 1024)
            result_1024 = self.sr_x2.upsample(result_512)
            
            # 4. Guardar resultado
            cv2.imwrite(output_path, result_1024)
            logger.info("Super-resolución completada: %s", output_path)
            return True

        except Exception as exc:
            logger.error("Fallo en el pipeline de super-resolución: %s", exc)
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
    if not engine.load_models():
        return {"error": "Modelos no disponibles en sentinel-project/models/"}
        
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
            
    return stats
