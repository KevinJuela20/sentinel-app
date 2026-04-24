"""
image_utils.py
--------------
Utilidades para la manipulación de imágenes y conversión de formatos.
"""

import logging
import numpy as np
from PIL import Image

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
    Combina tres bandas en una imagen PNG RGB de 8 bits.
    """
    # Normalizar cada banda
    r_8 = normalize_band(r)
    g_8 = normalize_band(g)
    b_8 = normalize_band(b)
    
    # Combinar en un array (H, W, 3)
    rgb_stack = np.dstack((r_8, g_8, b_8))
    
    # Guardar usando PIL
    img = Image.fromarray(rgb_stack)
    img.save(output_path)
    logger.debug("PNG guardado: %s", output_path)
