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
import re
from pathlib import Path
from typing import Optional, List, Dict
import numpy as np
import geopandas as gpd
import rasterio
from rasterio.mask import mask
from rasterio.warp import transform_geom
from rasterio.windows import from_bounds
from rasterio.enums import Resampling
from shapely.geometry import shape

logger = logging.getLogger(__name__)

# Códigos SCL a filtrar (nubes, sombras, etc.)
# 1: Saturated/Defective, 2: Dark Area Pixels, 3: Cloud Shadows
# 8: Cloud Medium Probability, 9: Cloud High Probability, 10: Thin Cirrus
CLOUD_CODES = [1, 2, 3, 8, 9, 10]

# ---------------------------------------------------------------------------
# Asignación fija de IDs de celdas de borde a su tile preferente.
# Las celdas que se ubican en los límites entre tiles solo se recortarán
# desde el tile asignado para evitar duplicados y recortes parciales.
# ---------------------------------------------------------------------------
IDS_POR_TILE = {
    "MPS": ["657", "658", "659", "660", "661", "663", "664", "665", "666", "667", "668",
            "669", "670", "671", "672", "673", "674", "675", "676", "677", "678", "679",
            "680", "681", "682", "683", "684", "685", "686"],

    "MQS": ["722", "763", "804", "845", "886", "927", "944", "945", "946", "959", "960",
            "961", "962", "963", "964", "965", "966", "967", "968", "969", "970", "971",
            "972", "973", "974", "975", "1009", "1050", "1091", "1132", "1255", "1296",
            "1337", "1378"],

    "MQT": ["894", "935", "976", "977", "978", "979", "980", "981", "982", "1017", "1058",
            "1099", "1140", "1181", "1222", "1263", "1304", "1345", "1386", "1427"],
}

# Diccionario invertido: ID → tile asignado (búsqueda O(1))
_TILE_POR_ID: Dict[str, str] = {
    cell_id: tile
    for tile, ids in IDS_POR_TILE.items()
    for cell_id in ids
}


def should_process_cell(cell_id: str, tile_id: str, crops_dir: Path, date_str: str) -> bool:
    """
    Determina si una celda debe procesarse en el tile actual.

    Lógica de deduplicación:
      1. Si el cell_id está en IDS_POR_TILE (borde), solo se procesa
         en el tile asignado.
      2. Si el cell_id NO está en la lista, se verifica si ya existe
         un recorte guardado en disco para esa celda y fecha.

    Args:
        cell_id: Identificador de la celda de la cuadrícula.
        tile_id: Tile que se está procesando actualmente (ej: MPS).
        crops_dir: Directorio donde se guardan los recortes PNG.
        date_str: Fecha compacta (YYYYMMDD) para el nombre del archivo.

    Returns:
        True si la celda debe procesarse, False si debe omitirse.
    """
    assigned_tile = _TILE_POR_ID.get(cell_id)

    if assigned_tile is not None:
        # Caso 1: ID de borde — solo procesar en el tile asignado
        if tile_id != assigned_tile:
            logger.info(
                "Celda %s omitida: asignada al tile %s, tile actual es %s",
                cell_id, assigned_tile, tile_id,
            )
            return False
        return True

    # Caso 2: ID no listado — verificar existencia previa en disco
    existing = list(crops_dir.glob(f"{cell_id}_{date_str}_*.png"))
    if existing:
        logger.info(
            "Celda %s omitida: ya existe recorte previo (%s)",
            cell_id, existing[0].name,
        )
        return False

    return True


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
                      output_dir: Path, date_str: str, tile_id: str) -> Optional[str]:
    """
    Procesa una celda individual: recorta, filtra nubes y guarda PNG si está limpia.
    
    Args:
        tif_paths: Dict con {band_name: path_to_tif} (B02, B03, B04, SCL).
        cell_geom: Geometría de la celda (GeoJSON dict).
        cell_id: Identificador de la celda.
        output_dir: Directorio donde guardar los recortes.
        date_str: Fecha para el nombre del archivo.
        tile_id: Identificador del tile (ej: MPS).
        
    Returns:
        Ruta al PNG generado o None si fue descartado.
    """
    from src.image_utils import save_rgb_png
    
    scl_path = tif_paths.get("SCL")
    b04_path = tif_paths.get("B04")
    
    if not scl_path or not b04_path:
        logger.warning("Faltan bandas esenciales (SCL o B04) para celda %s", cell_id)
        return None

    try:
        # 1. Abrir B04 como referencia (10m)
        with rasterio.open(b04_path) as src_ref:
            ref_crs = src_ref.crs
            ref_transform = src_ref.transform
            
            # Transformar geometría al CRS de referencia (UTM)
            target_geom = transform_geom("EPSG:4326", ref_crs, cell_geom)
            geom_shape = shape(target_geom)
            bounds = geom_shape.bounds
            
            # Calcular ventana de extracción en base a B04
            window = from_bounds(*bounds, transform=ref_transform)
            h_ref, w_ref = int(window.height), int(window.width)
            
            # 1.1 Validación de Dimensiones (Task 2.2 / 3.1)
            # Descartar si es menor a 63 píxeles en cualquier eje (evitar bordes incompletos)
            if h_ref < 63 or w_ref < 63:
                logger.info("Celda %s descartada por tamaño insuficiente: %dx%d", cell_id, w_ref, h_ref)
                return None

            # 2. Validar nubes con SCL en su resolución nativa (20m)
            with rasterio.open(scl_path) as src_scl:
                # Transformar geometría al CRS de SCL (normalmente el mismo UTM)
                target_geom_scl = transform_geom("EPSG:4326", src_scl.crs, cell_geom)
                try:
                    scl_crop, _ = mask(src_scl, [target_geom_scl], crop=True)
                except ValueError:
                    # Si no hay solapamiento, simplemente saltamos la celda sin error
                    return None
                
                clean, perc = is_crop_clean(scl_crop)
                
            if not clean:
                logger.info("Celda %s descartada por nubes (%.1f%%)", cell_id, perc * 100)
                return None

            # 3. Extraer bandas RGB (B04, B03, B02) alineadas a la ventana de B04
            rgb_data = {}
            for band in ["B04", "B03", "B02"]:
                with rasterio.open(tif_paths[band]) as src:
                    # Leer usando la ventana de referencia y resampling bilineal si es necesario
                    rgb_data[band] = src.read(
                        1, 
                        window=window, 
                        out_shape=(h_ref, w_ref),
                        resampling=Resampling.bilinear
                    )

        # 4. Guardar PNG
        output_path = output_dir / f"{cell_id}_{date_str.replace('-', '')}_{tile_id}.png"
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
        
    # 1. Agrupar archivos .tif por Tile ID (Task 2.1)
    # Formato esperado: YYYYMMDD_TILE_BAND.tif
    tiles_data = {} # dict[tile_id -> dict[band_name -> path]]
    
    for t in tifs:
        # Regex para extraer Tile ID y Banda
        match = re.search(r"(\d{8})_([A-Z0-9]{3})_([A-Z0-9]+)\.tif", t.name)
        if match:
            _, tile_id, band = match.groups()
            if tile_id not in tiles_data:
                tiles_data[tile_id] = {}
            tiles_data[tile_id][band] = str(t)
        else:
            # Fallback para el formato antiguo o si falta el tile_id
            band = None
            for b in ["B02", "B03", "B04", "SCL"]:
                if b in t.name:
                    band = b
                    break
            if band:
                if "UNKNOWN" not in tiles_data:
                    tiles_data["UNKNOWN"] = {}
                tiles_data["UNKNOWN"][band] = str(t)

    if not tiles_data:
        return {"error": "No se pudieron organizar los archivos .tif por banda/tile."}

    # 2. Cargar cuadrícula
    grid_gdf = gpd.read_file(grid_path)
    
    # 3. Crear subcarpeta crops
    crops_dir = date_dir / "crops"
    crops_dir.mkdir(exist_ok=True)
    
    # 4. Procesar cada celda
    stats = {"total": len(grid_gdf), "saved": 0, "skipped": 0, "errors": 0, "dedup_skipped": 0}
    # Obtener fecha del path: .../YYYY/MM/DD
    try:
        y, m, d = date_dir.parts[-3:]
        date_str = f"{y}{m}{d}"
    except:
        date_str = date_dir.name
    
    for tile_id, bands_found in tiles_data.items():
        logger.info("Procesando Tile: %s", tile_id)
        for _, row in grid_gdf.iterrows():
            cell_id = str(row.get("id", row.index[0]))
            geom = row.geometry.__geo_interface__
            
            # Filtro de deduplicación: verificar si la celda debe procesarse
            if not should_process_cell(cell_id, tile_id, crops_dir, date_str):
                stats["dedup_skipped"] += 1
                continue
            
            res = process_grid_cell(bands_found, geom, cell_id, crops_dir, date_str, tile_id)
            if res:
                stats["saved"] += 1
            else:
                stats["skipped"] += 1
            
    # 5. Generar Mosaico RGB del Área de Estudio (ARH_ETAPA.kml)
    mosaic_success = False
    try:
        from src.geo_utils import load_kml_geometry
        from rasterio.merge import merge
        import tempfile
        
        # Intentar encontrar el KML en rutas comunes
        possible_kml_paths = [
            Path("external/ARH_ETAPA.kml"),
            Path("sentinel-project/external/ARH_ETAPA.kml"),
            Path(__file__).parent.parent / "external" / "ARH_ETAPA.kml"
        ]
        
        kml_file = None
        for p in possible_kml_paths:
            if p.exists():
                kml_file = p
                break

        if kml_file:
            logger.info("Generando mosaico RGB del área de estudio (AOI) usando %s...", kml_file)
            study_area_geom = load_kml_geometry(str(kml_file))
            
            tile_rgb_crops = []
            temp_paths = []
            
            for tile_id, bands_found in tiles_data.items():
                # Verificar que tengamos las bandas RGB
                if all(b in bands_found for b in ["B04", "B03", "B02"]):
                    with rasterio.open(bands_found["B04"]) as src_b04:
                        # Transformar geometría al CRS del tile para el recorte
                        target_geom = transform_geom("EPSG:4326", src_b04.crs, study_area_geom.__geo_interface__)
                        
                        # 5.1 Leer bandas y aplicar máscara KML
                        # Usamos crop=True para obtener solo el área del KML en este tile
                        try:
                            b04_data, out_transform = mask(src_b04, [target_geom], crop=True)
                        except ValueError:
                            # El AOI no solapa con este tile
                            logger.info("Tile %s no intersecta con el área del KML. Saltando...", tile_id)
                            continue
                        
                        with rasterio.open(bands_found["B03"]) as src_b03:
                            b03_data, _ = mask(src_b03, [target_geom], crop=True)
                        with rasterio.open(bands_found["B02"]) as src_b02:
                            b02_data, _ = mask(src_b02, [target_geom], crop=True)
                        
                        # Combinar en un stack RGB (3, H, W)
                        rgb_stack = np.concatenate([b04_data, b03_data, b02_data])
                        
                        # 5.2 Guardar recorte temporal de este tile para el merge final
                        temp_tif = tempfile.NamedTemporaryFile(suffix=f"_{tile_id}_rgb.tif", delete=False)
                        temp_paths.append(temp_tif.name)
                        
                        out_meta = src_b04.meta.copy()
                        out_meta.update({
                            "driver": "GTiff",
                            "height": rgb_stack.shape[1],
                            "width": rgb_stack.shape[2],
                            "transform": out_transform,
                            "count": 3
                        })
                        
                        with rasterio.open(temp_tif.name, "w", **out_meta) as dest:
                            dest.write(rgb_stack)
                        
                        # Reabrir el archivo temporal para pasarlo a merge
                        tile_rgb_crops.append(rasterio.open(temp_tif.name))
            
            if tile_rgb_crops:
                # 5.3 Realizar el merge de los recortes de cada tile
                mosaic, mosaic_transform = merge(tile_rgb_crops)
                
                # 5.4 Guardar mosaico final al lado de la carpeta crops
                y, m, d = date_dir.parts[-3:]
                final_mosaic_name = f"Color_{y}-{m}-{d}.tif"
                mosaic_path = date_dir / final_mosaic_name
                
                out_meta = tile_rgb_crops[0].meta.copy()
                out_meta.update({
                    "height": mosaic.shape[1],
                    "width": mosaic.shape[2],
                    "transform": mosaic_transform
                })
                
                with rasterio.open(mosaic_path, "w", **out_meta) as dest:
                    dest.write(mosaic)
                
                logger.info("Mosaico RGB del área de estudio creado: %s", mosaic_path)
                mosaic_success = True
                
                # Cerrar y eliminar temporales
                for src in tile_rgb_crops:
                    src.close()
                for tp in temp_paths:
                    try:
                        Path(tp).unlink()
                    except:
                        pass
        else:
            logger.warning("No se encontró el archivo ARH_ETAPA.kml en sentinel-project/external/. Se omite el mosaico.")

    except Exception as exc:
        logger.error("Error durante la generación del mosaico RGB: %s", exc)

    # 6. Limpieza (Task 3.1)
    # Solo eliminar originales si los crops se generaron Y el mosaico fue exitoso
    if delete_originals and stats["saved"] > 0 and mosaic_success:
        logger.info("Limpiando bandas individuales (.tif) tras procesamiento exitoso.")
        for t in tifs:
            try:
                t.unlink()
            except Exception as e:
                logger.error("Error eliminando temporal %s: %s", t, e)
                
    return stats
