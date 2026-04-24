"""
downloader.py
-------------
Motor de descarga y procesamiento para Sentinel-2.

Responsabilidades:
  - Firmar URLs de assets usando planetary_computer.
  - Descargar y recortar rásers usando rasterio y geometries GeoJSON.
"""

import logging
from typing import Optional

import planetary_computer as pc
import rasterio
from rasterio.mask import mask
from rasterio.warp import transform_geom

logger = logging.getLogger(__name__)


def sign_asset_url(url: str) -> str:
    """
    Firma una URL de asset usando el SDK de Planetary Computer.
    """
    try:
        return pc.sign_url(url)
    except Exception as exc:
        logger.error("Error al firmar URL %s: %s", url, exc)
        raise


def download_and_clip(asset_url: str, geom: dict, output_path: str) -> bool:
    """
    Abre un asset remoto, aplica un recorte espacial y guarda el resultado localmente.
    
    Args:
        asset_url: URL del asset (debe estar firmada).
        geom: Geometría GeoJSON para el recorte (EPSG:4326).
        output_path: Ruta de destino para el archivo .tif.
        
    Returns:
        True si tuvo éxito, False en caso contrario.
    """
    try:
        with rasterio.open(asset_url) as src:
            # 1. Transformar geometría al CRS del raster
            # Sentinel-2 suele estar en UTM, el AOI en WGS84
            target_geom = transform_geom(
                src_crs="EPSG:4326",
                dst_crs=src.crs,
                geom=geom
            )

            # 2. Aplicar máscara (clip)
            out_image, out_transform = mask(src, [target_geom], crop=True)
            
            # 3. Copiar metadatos del original y actualizar dimensiones/transformación
            out_meta = src.meta.copy()
            out_meta.update({
                "driver": "GTiff",
                "height": out_image.shape[1],
                "width": out_image.shape[2],
                "transform": out_transform,
                "crs": src.crs
            })
            
            # 4. Escribir archivo local
            with rasterio.open(output_path, "w", **out_meta) as dest:
                dest.write(out_image)
                
        logger.info("Archivo guardado y recortado en: %s", output_path)
        return True

    except ValueError as val_err:
        if "shapes do not overlap" in str(val_err).lower():
            logger.warning("El AOI no se solapa con el tile: %s", asset_url)
        else:
            logger.error("Error de valor en recorte: %s", val_err)
        return False
    except Exception as exc:
        logger.error("Error crítico procesando asset %s: %s", asset_url, exc)
        import traceback
        logger.error(traceback.format_exc())
        return False


def download_item_bands(item, bands: list, geom: dict, output_dir: str, 
                        date_str: str, progress_callback=None) -> list:
    """
    Orquesta la descarga de múltiples bandas para un item STAC.
    
    Args:
        item: Objeto STACItem (o similar con .assets e .item_id).
        bands: Lista de nombres de bandas a descargar (ej: ["B02", "B03"]).
        geom: Geometría para el recorte.
        output_dir: Directorio de salida ya creado.
        date_str: Fecha formateada para el nombre de archivo.
        progress_callback: Función opcional para reportar progreso.
        
    Returns:
        Lista de rutas de archivos descargados exitosamente.
    """
    from src.file_manager import get_band_filename
    
    downloaded = []
    total = len(bands)
    
    for i, band in enumerate(bands):
        asset = item.assets.get(band)
        if not asset:
            logger.warning("Banda %s no encontrada en el item %s", band, item.item_id)
            continue
            
        filename = get_band_filename(item.item_id, band, date_str)
        output_path = str(output_dir / filename)
        
        try:
            # En nuestro STACItem normalizado, asset ya es el href (string)
            asset_url = asset if isinstance(asset, str) else getattr(asset, "href", None)
            
            if not asset_url:
                logger.warning("No se pudo obtener la URL del asset para %s", band)
                continue

            signed_url = sign_asset_url(asset_url)
            success = download_and_clip(signed_url, geom, output_path)
            if success:
                downloaded.append(output_path)
        except Exception as exc:
            logger.error("Fallo crítico en banda %s: %s", band, exc)
            
        if progress_callback:
            progress_callback(i + 1, total, band)
            
    return downloaded
