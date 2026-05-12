"""
geo_utils.py
------------
Utilidades geoespaciales para el Sentinel Data Downloader.

Responsabilidades:
  - Cargar y parsear archivos KML para extraer la geometría del AOI.
  - Convertir geometrías a formato GeoJSON para consultas STAC.
"""

import json
import logging
from pathlib import Path
from typing import Optional

logger = logging.getLogger(__name__)


def mapping(geom):  # pragma: no cover — replaced by shapely.geometry.mapping at runtime
    """Thin wrapper around shapely.geometry.mapping, patchable in tests."""
    from shapely.geometry import mapping as _mapping
    return _mapping(geom)


def load_aoi(kml_path: str) -> Optional[dict]:
    """
    Carga un archivo KML y retorna la geometría del área de interés (AOI)
    como un objeto GeoJSON (dict).

    Args:
        kml_path: Ruta al archivo KML (e.g. "external/ARH_MAP.kml").

    Returns:
        Diccionario GeoJSON con la geometría unida de todas las features,
        o None si el archivo no existe o no puede leerse.

    Raises:
        FileNotFoundError: Si el archivo KML no existe.
        ValueError: Si el archivo KML no contiene geometrías válidas.
    """
    path = Path(kml_path)
    if not path.exists():
        raise FileNotFoundError(f"Archivo KML no encontrado: {kml_path}")

    try:
        import geopandas as gpd  # lazy import
        import fiona  # lazy import

        # fiona necesita el driver KML habilitado
        fiona.drvsupport.supported_drivers["KML"] = "rw"
        fiona.drvsupport.supported_drivers["LIBKML"] = "rw"

        gdf = gpd.read_file(kml_path, driver="KML")

        if gdf.empty:
            raise ValueError(f"El archivo KML no contiene geometrías: {kml_path}")

        # Unir todas las geometrías en un solo polígono/multipolígono
        union_geom = gdf.geometry.union_all()
        geojson_geom = mapping(union_geom)  # module-level, patchable in tests

        logger.info(
            "AOI cargado desde '%s': %d feature(s), tipo=%s",
            kml_path,
            len(gdf),
            geojson_geom.get("type", "desconocido"),
        )
        return dict(geojson_geom)

    except Exception as exc:
        logger.error("Error al parsear el archivo KML '%s': %s", kml_path, exc)
        raise


def load_kml_geometry(kml_path: str):
    """
    Carga un archivo KML y retorna la geometría unificada de todas las features
    como un objeto de Shapely.

    Args:
        kml_path: Ruta al archivo KML.

    Returns:
        Objeto de Shapely (Polygon o MultiPolygon).
    """
    path = Path(kml_path)
    if not path.exists():
        raise FileNotFoundError(f"Archivo KML no encontrado: {kml_path}")

    import geopandas as gpd
    import fiona

    fiona.drvsupport.supported_drivers["KML"] = "rw"
    fiona.drvsupport.supported_drivers["LIBKML"] = "rw"

    gdf = gpd.read_file(kml_path, driver="KML")
    if gdf.empty:
        raise ValueError(f"El archivo KML no contiene geometrías: {kml_path}")

    return gdf.geometry.union_all()


def load_geojson(geojson_path: str):
    """
    Carga un archivo GeoJSON y retorna un GeoDataFrame.

    Args:
        geojson_path: Ruta al archivo GeoJSON.

    Returns:
        GeoDataFrame con las features del archivo.

    Raises:
        FileNotFoundError: Si el archivo no existe.
    """
    import geopandas as gpd  # lazy import

    path = Path(geojson_path)
    if not path.exists():
        raise FileNotFoundError(f"Archivo GeoJSON no encontrado: {geojson_path}")

    gdf = gpd.read_file(geojson_path)
    logger.info(
        "GeoJSON cargado desde '%s': %d feature(s)", geojson_path, len(gdf)
    )
    return gdf
