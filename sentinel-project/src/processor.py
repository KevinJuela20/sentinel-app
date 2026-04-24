"""
processor.py
------------
Motor de fragmentación y filtrado de nubes para Sentinel-2.

Responsabilidades:
  - Iterar sobre polígonos de una cuadrícula GeoJSON.
  - Aplicar filtro de nubes basado en la banda SCL.
  - Orquestar la generación de recortes PNG.
"""

import logging
from pathlib import Path
from typing import Optional
import numpy as np
import geopandas as gpd
import rasterio
from rasterio.mask import mask
from rasterio.warp import transform_geom

logger = logging.getLogger(__name__)

# Códigos SCL a filtrar (nubes, sombras, etc.)
# 1: Saturated/Defective, 2: Dark Area Pixels, 3: Cloud Shadows
# 8: Cloud Medium Probability, 9: Cloud High Probability, 10: Thin Cirrus
CLOUD_CODES = [1, 2, 3, 8, 9, 10]


def is_crop_clean(scl_data: np.ndarray, threshold: float = 0.05) -> tuple[bool, float]:
    """
    Analiza la banda SCL para determinar si el recorte está limpio de nubes.

    Args:
        scl_data: Array 2D/3D con los datos de la banda SCL.
        threshold: Porcentaje máximo de píxeles nublados permitidos (0.0 a 1.0).

    Returns:
        (is_clean, cloud_percentage)
    """
    # Asegurar que es 2D
    if scl_data.ndim == 3:
        scl_data = scl_data[0]
        
    total_pixels = scl_data.size
    if total_pixels == 0:
        return False, 0.0
        
    cloud_pixels = np.isin(scl_data, CLOUD_CODES).sum()
    cloud_percentage = cloud_pixels / total_pixels
    
    return cloud_percentage <= threshold, cloud_percentage


def process_grid_cell(tif_paths: dict, cell_geom: dict, cell_id: str, 
                      output_dir: Path, date_str: str) -> Optional[str]:
    """
    Procesa una celda individual: recorta, filtra nubes y guarda PNG si está limpia.
    
    Args:
        tif_paths: Dict con {band_name: path_to_tif} (B02, B03, B04, SCL).
        cell_geom: Geometría de la celda (GeoJSON dict).
        cell_id: Identificador de la celda.
        output_dir: Directorio donde guardar los recortes.
        date_str: Fecha para el nombre del archivo.
        
    Returns:
        Ruta al PNG generado o None si fue descartado.
    """
    from src.image_utils import save_rgb_png
    
    scl_path = tif_paths.get("SCL")
    if not scl_path or not Path(scl_path).exists():
        logger.warning("No se encontró banda SCL para celda %s", cell_id)
        return None

    try:
        # 1. Verificar nubes con SCL
        with rasterio.open(scl_path) as src:
            # Transformar geometría al CRS del raster (UTM)
            target_geom = transform_geom("EPSG:4326", src.crs, cell_geom)
            
            scl_image, _ = mask(src, [target_geom], crop=True)
            clean, perc = is_crop_clean(scl_image)
            
        if not clean:
            logger.info("Celda %s descartada por nubes (%.1f%%)", cell_id, perc * 100)
            return None

        # 2. Extraer B04, B03, B02 para RGB
        rgb_data = {}
        for band in ["B04", "B03", "B02"]:
            with rasterio.open(tif_paths[band]) as src:
                img, _ = mask(src, [target_geom], crop=True)
                rgb_data[band] = img[0] # Usar primer canal

        # 3. Guardar PNG
        output_path = output_dir / f"{cell_id}_{date_str.replace('-', '')}.png"
        save_rgb_png(rgb_data["B04"], rgb_data["B03"], rgb_data["B02"], str(output_path))
        
        return str(output_path)

    except Exception as exc:
        logger.error("Error procesando celda %s: %s", cell_id, exc)
        return None


def process_all_grids(date_dir: Path, grid_path: Path, delete_originals: bool = False) -> dict:
    """
    Orquesta el procesamiento de todas las celdas para una fecha específica.
    
    Args:
        date_dir: Directorio de la fecha (ej: Data_Sentinel/2025/01/01).
        grid_path: Ruta al archivo cuadricula_arh.geojson.
        delete_originals: Si es True, elimina los .tif tras procesar.
        
    Returns:
        Dict con estadísticas del proceso.
    """
    # 1. Buscar archivos .tif
    tifs = list(date_dir.glob("*.tif"))
    if not tifs:
        return {"error": "No se encontraron archivos .tif"}
        
    # Organizar por item_id y banda
    # Supone formato YYYYMMDD_BAND.tif o similar
    # Realmente en UC-04 los nombramos YYYYMMDD_BAND.tif. 
    # Pero si hay varios items el mismo día, necesitamos discriminarlos.
    # El FileManager usa: f"{date_compact}_{band_name}.tif"
    # Ajustamos para encontrar las bandas necesarias:
    bands_found = {}
    for t in tifs:
        band = None
        for b in ["B02", "B03", "B04", "SCL", "visual"]:
            if b in t.name:
                band = b
                break
        if band:
            bands_found[band] = str(t)

    # 2. Cargar cuadrícula
    grid_gdf = gpd.read_file(grid_path)
    
    # 3. Crear subcarpeta crops
    crops_dir = date_dir / "crops"
    crops_dir.mkdir(exist_ok=True)
    
    # 4. Procesar cada celda
    stats = {"total": len(grid_gdf), "saved": 0, "skipped": 0, "errors": 0}
    # Obtener fecha del path: .../YYYY/MM/DD
    try:
        y, m, d = date_dir.parts[-3:]
        date_str = f"{y}{m}{d}"
    except:
        date_str = date_dir.name
    
    for _, row in grid_gdf.iterrows():
        cell_id = str(row.get("id", row.index[0]))
        geom = row.geometry.__geo_interface__
        
        res = process_grid_cell(bands_found, geom, cell_id, crops_dir, date_str)
        if res:
            stats["saved"] += 1
        else:
            stats["skipped"] += 1
            
    # 5. Limpieza (Task 2.2)
    if delete_originals and stats["saved"] > 0:
        for t in tifs:
            try:
                t.unlink()
            except Exception as e:
                logger.error("Error eliminando temporal %s: %s", t, e)
                
    return stats
