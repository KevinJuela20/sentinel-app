"""
image_utils.py
--------------
Utilidades para la manipulación de imágenes y conversión de formatos.
"""

import logging
import numpy as np
from PIL import Image
import rasterio
from rasterio.merge import merge

logger = logging.getLogger(__name__)

def normalize_band(band_data: np.ndarray, min_val: int = 0, max_val: int = 3000) -> np.ndarray:
    """
    Normaliza una banda de 16-bit a 8-bit usando un umbral de saturación.
    
    Args:
        band_data: Array de la banda (uint16).
        min_val: Valor que será mapeado a 0.
        max_val: Valor que será mapeado a 255.
        
    Returns:
        Array uint8.
    """
    # Clip y normalización lineal
    clipped = np.clip(band_data, min_val, max_val)
    normalized = ((clipped - min_val) / (max_val - min_val) * 255).astype(np.uint8)
    return normalized


def save_rgb_png(r: np.ndarray, g: np.ndarray, b: np.ndarray, output_path: str):
    """
    Combina tres bandas en una imagen PNG RGB de 8 bits con estiramiento de contraste (2-98%).
    """
    # Combinar en un array (H, W, 3)
    stack = np.dstack((r, g, b)).astype(np.float32)
    
    # Stretch del 2% al 98% para mejorar contraste (según sugerencia del usuario)
    # Esto ayuda a que las imágenes no se vean muy oscuras o lavadas
    low, high = np.nanpercentile(stack, (2, 98))
    
    if high > low:
        rescaled = np.clip((stack - low) / (high - low), 0, 1)
    else:
        # Fallback si el rango es muy pequeño (evitar división por cero)
        rescaled = np.clip(stack / 3000.0, 0, 1)
        
    # Convertir a 8 bits
    rgb_8 = (rescaled * 255).astype(np.uint8)
    
    # Guardar usando PIL con redimensionamiento a 128x128
    img = Image.fromarray(rgb_8)
    img = img.resize((128, 128), resample=Image.Resampling.LANCZOS)
    img.save(output_path)
    logger.debug("PNG guardado con stretch (2-98%%): %s", output_path)


def create_mosaic(input_paths: list[str], output_path: str) -> bool:
    """
    Crea un mosaico a partir de una lista de archivos rasters.
    
    Args:
        input_paths: Lista de rutas a archivos .tif.
        output_path: Ruta del archivo de salida.
        
    Returns:
        True si tuvo éxito, False en caso contrario.
    """
    if not input_paths:
        logger.warning("No hay archivos para crear el mosaico.")
        return False

    try:
        src_files_to_mosaic = []
        for fp in input_paths:
            src = rasterio.open(fp)
            src_files_to_mosaic.append(src)

        # Realizar el merge
        mosaic, out_trans = merge(src_files_to_mosaic)

        # Copiar metadatos del primer archivo
        out_meta = src_files_to_mosaic[0].meta.copy()

        # Actualizar metadatos para el nuevo mosaico
        out_meta.update({
            "driver": "GTiff",
            "height": mosaic.shape[1],
            "width": mosaic.shape[2],
            "transform": out_trans,
            "crs": src_files_to_mosaic[0].crs
        })

        # Guardar mosaico
        with rasterio.open(output_path, "w", **out_meta) as dest:
            dest.write(mosaic)

        # Cerrar archivos fuente
        for src in src_files_to_mosaic:
            src.close()

        logger.info("Mosaico unificado creado: %s", output_path)
        return True

    except Exception as e:
        logger.error("Error creando mosaico: %s", e)
        return False
