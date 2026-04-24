"""
preview_engine.py
-----------------
Motor de previsualización para Sentinel-2.

Responsabilidades:
  - Descargar thumbnails (rendered_preview) desde MPC.
  - Aplicar recortes espaciales (masking) basados en la geometría del AOI.
  - Generar imágenes RGBA con transparencia para la galería.
"""

import io
import logging
from typing import Optional

import numpy as np
import requests
from PIL import Image

try:
    import rasterio
    from rasterio.mask import mask
    from rasterio.memoryfile import MemoryFile
except ImportError:
    # Para entornos sin dependencias geoespaciales (tests básicos)
    rasterio = None

logger = logging.getLogger(__name__)


def download_image(url: str) -> Optional[bytes]:
    """
    Descarga una imagen desde una URL y retorna los bytes.
    """
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.content
    except Exception as exc:
        logger.error("Error al descargar imagen desde %s: %s", url, exc)
        return None


def apply_aoi_mask(image_bytes: bytes, aoi_geom: dict) -> Optional[Image.Image]:
    """
    Aplica una máscara de transparencia a la imagen basada en la geometría AOI.
    
    Args:
        image_bytes: Bytes de la imagen original (JPG/PNG).
        aoi_geom: Geometría GeoJSON del área de interés.
        
    Returns:
        Objeto PIL.Image (RGBA) recortado, o None si falla.
    """
    if rasterio is None:
        logger.warning("Rasterio no disponible. No se puede aplicar la máscara.")
        return Image.open(io.BytesIO(image_bytes)).convert("RGBA")

    try:
        with MemoryFile(image_bytes) as memfile:
            with memfile.open() as src:
                # Aplicar máscara (crop=True para ajustar al AOI)
                # Nota: Las imágenes 'rendered_preview' de MPC suelen venir sin CRS 
                # o con uno por defecto. rasterio intentará leerlo.
                out_image, out_transform = mask(src, [aoi_geom], crop=True, filled=False)
                
                # out_image es un array (bandas, alto, ancho)
                # Extraer bandas RGB
                rgb = out_image[:3]
                
                # Crear canal Alfa basado en el footprint del recorte
                # La máscara de rasterio devuelve un masked_array
                if hasattr(out_image, "mask"):
                    # 0 para transparente, 255 para opaco
                    alpha = (~out_image.mask[0] * 255).astype(np.uint8)
                else:
                    # Si no hay máscara, todo es opaco por ahora
                    alpha = np.full((out_image.shape[1], out_image.shape[2]), 255, dtype=np.uint8)
                
                # Combinar en RGBA (alto, ancho, 4)
                rgba = np.dstack([
                    rgb[0], rgb[1], rgb[2], alpha
                ])
                
                return Image.fromarray(rgba, "RGBA")

    except Exception as exc:
        logger.error("Error al aplicar máscara AOI: %s", exc)
        # Fallback: retornar imagen original sin máscara si algo falla en el proceso geo
        try:
            return Image.open(io.BytesIO(image_bytes)).convert("RGBA")
        except:
            return None


def get_masked_preview(preview_url: str, aoi_geom: dict) -> Optional[Image.Image]:
    """
    Orquestador: descarga la imagen y aplica el recorte.
    """
    img_bytes = download_image(preview_url)
    if not img_bytes:
        return None
    
    return apply_aoi_mask(img_bytes, aoi_geom)
