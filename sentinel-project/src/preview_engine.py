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


def _clip_geometry_to_bbox(aoi_geom: dict, bbox: list[float]):
    """
    Recorta la geometría del AOI al bounding box del tile usando shapely.

    Args:
        aoi_geom: Geometría GeoJSON del AOI (dict con 'type' y 'coordinates').
        bbox: Bounding box del tile [minx, miny, maxx, maxy].

    Returns:
        Objeto shapely con la geometría recortada, o None si no hay intersección.
    """
    from shapely.geometry import shape, box

    try:
        aoi_shape = shape(aoi_geom)
        tile_box = box(*bbox)  # box(minx, miny, maxx, maxy)

        if not aoi_shape.intersects(tile_box):
            return None

        clipped = aoi_shape.intersection(tile_box)

        if clipped.is_empty:
            return None

        return clipped
    except Exception as exc:
        logger.error("Error al recortar AOI al bbox del tile: %s", exc)
        return None


def _extract_drawable_coords(geom) -> list[list[tuple]]:
    """
    Extrae listas de coordenadas dibujables desde cualquier tipo de geometría
    resultante de una intersección (Polygon, MultiPolygon, LineString,
    MultiLineString, GeometryCollection).

    Returns:
        Lista de listas de tuplas (lon, lat) — cada sub-lista es una línea/anillo.
    """
    from shapely.geometry import (
        Polygon, MultiPolygon, LineString, MultiLineString, GeometryCollection
    )

    coord_lists = []

    if isinstance(geom, Polygon):
        # Anillo exterior + anillos interiores
        coord_lists.append(list(geom.exterior.coords))
        for interior in geom.interiors:
            coord_lists.append(list(interior.coords))

    elif isinstance(geom, MultiPolygon):
        for poly in geom.geoms:
            coord_lists.extend(_extract_drawable_coords(poly))

    elif isinstance(geom, LineString):
        coord_lists.append(list(geom.coords))

    elif isinstance(geom, MultiLineString):
        for line in geom.geoms:
            coord_lists.append(list(line.coords))

    elif isinstance(geom, GeometryCollection):
        for sub_geom in geom.geoms:
            coord_lists.extend(_extract_drawable_coords(sub_geom))

    return coord_lists


def _draw_aoi_boundary(img: Image.Image, aoi_geom: dict, bbox: list[float]):
    """
    Dibuja el contorno del AOI sobre la imagen PIL, recortando primero
    la geometría al bounding box del tile para evitar artefactos visuales.
    """
    # 1. Recortar la geometría al extent del tile
    clipped = _clip_geometry_to_bbox(aoi_geom, bbox)
    if clipped is None:
        return  # Sin intersección, no dibujar nada

    draw = ImageDraw.Draw(img)
    width, height = img.size
    minx, miny, maxx, maxy = bbox

    # Factores de escala
    scale_x = width / (maxx - minx) if (maxx - minx) != 0 else 1.0
    scale_y = height / (maxy - miny) if (maxy - miny) != 0 else 1.0

    # 2. Extraer coordenadas dibujables
    coord_lists = _extract_drawable_coords(clipped)

    for coords in coord_lists:
        # Proyectar cada punto al espacio de píxeles
        pixel_points = []
        for pt in coords:
            lon, lat = pt[0], pt[1]
            px = (lon - minx) * scale_x
            py = (maxy - lat) * scale_y
            pixel_points.append((px, py))

        # Dibujar el contorno (Rojo puro #FF0000, 2px)
        if len(pixel_points) > 1:
            # Cerrar el polígono si el primer y último punto no coinciden
            if pixel_points[0] != pixel_points[-1]:
                pixel_points.append(pixel_points[0])
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

        # Dibujar contorno del AOI recortado al extent del tile
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
