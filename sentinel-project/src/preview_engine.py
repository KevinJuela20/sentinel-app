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

import requests
from PIL import Image, ImageDraw, ImageEnhance

logger = logging.getLogger(__name__)


def _draw_aoi_boundary(img: Image.Image, aoi_geom: dict, bbox: list[float]):
    """
    Dibuja el contorno del AOI sobre la imagen PIL usando mapeo lineal desde el bbox.
    """
    draw = ImageDraw.Draw(img)
    width, height = img.size
    minx, miny, maxx, maxy = bbox
    
    # Pre-calculamos los factores de escala
    # Evitar división por cero si el bbox es un punto (no debería pasar)
    scale_x = width / (maxx - minx) if (maxx - minx) != 0 else 1.0
    scale_y = height / (maxy - miny) if (maxy - miny) != 0 else 1.0

    # Extraer geometrías (manejar Polygon y MultiPolygon)
    geoms = []
    if aoi_geom["type"] == "Polygon":
        geoms = [aoi_geom["coordinates"]]
    elif aoi_geom["type"] == "MultiPolygon":
        geoms = aoi_geom["coordinates"]

    for rings in geoms:
        for ring in rings:
            # Proyectar cada punto del anillo al espacio de píxeles
            # ring es una lista de [lon, lat]
            pixel_points = []
            for pt in ring:
                # Mapeo lineal: (lon, lat) -> (px, py)
                # Task 2.2: Slicing pt[:2] para manejar coordenadas 3D [lon, lat, alt]
                lon, lat = pt[:2]
                px = (lon - minx) * scale_x
                py = (maxy - lat) * scale_y
                pixel_points.append((px, py))
            
            # Dibujar el contorno (Rojo puro #FF0000, 2px)
            if len(pixel_points) > 1:
                draw.line(pixel_points, fill=(255, 0, 0, 255), width=2)


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


def apply_aoi_mask(image_bytes: bytes, aoi_geom: dict, bbox: list[float]) -> Optional[Image.Image]:
    """
    Sobrepone el contorno del AOI sobre la imagen completa del tile (sin recorte),
    aplica mejora de contraste y dibuja el borde rojo.
    
    Args:
        image_bytes: Bytes de la imagen original (JPG/PNG).
        aoi_geom: Geometría GeoJSON del área de interés.
        bbox: Bounding Box del tile [minx, miny, maxx, maxy].
        
    Returns:
        Objeto PIL.Image (RGBA) con el contorno superpuesto.
    """
    try:
        # Abrir imagen original
        img = Image.open(io.BytesIO(image_bytes)).convert("RGBA")

        # Mejora estética: Contraste
        enhancer = ImageEnhance.Contrast(img)
        img = enhancer.enhance(1.3) # Factor de realce 1.3

        # Dibujar contorno del AOI sobre el tile completo usando el bbox
        _draw_aoi_boundary(img, aoi_geom, bbox)
        
        return img

    except Exception as exc:
        logger.error("Error al procesar visualización: %s", exc)
        try:
            return Image.open(io.BytesIO(image_bytes)).convert("RGBA")
        except:
            return None


def get_masked_preview(preview_url: str, aoi_geom: dict, bbox: list[float]) -> Optional[Image.Image]:
    """
    Orquestador: descarga la imagen y aplica la superposición del AOI.
    """
    img_bytes = download_image(preview_url)
    if not img_bytes:
        return None
    
    return apply_aoi_mask(img_bytes, aoi_geom, bbox)
