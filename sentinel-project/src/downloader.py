"""
downloader.py
-------------
Motor de descarga y procesamiento para Sentinel-2.

Responsabilidades:
  - Firmar URLs de assets usando planetary_computer.
  - Descargar y recortar rásers usando rasterio y geometries GeoJSON.
"""

import logging
import requests
from typing import Optional

import planetary_computer as pc
import rasterio
from rasterio.mask import mask
from rasterio.warp import transform_geom

logger = logging.getLogger(__name__)


def sign_asset_url(url: str) -> str:
    """
    Firma una URL de asset usando el SDK de Planetary Computer.
    Si la URL ya tiene un token SAS (expirado o no), lo remueve antes de firmar
    para forzar la generación de un nuevo token válido y evitar errores 403.
    """
    try:
        from urllib.parse import urlparse, urlunparse
        
        # Eliminar cualquier query parameter (SAS token) existente
        parsed = urlparse(url)
        clean_url = urlunparse((parsed.scheme, parsed.netloc, parsed.path, parsed.params, '', parsed.fragment))
        
        return pc.sign_url(clean_url)
    except Exception as exc:
        logger.error("Error al firmar URL %s: %s", url, exc)
        raise


def download_full_tile(asset_url: str, output_path: str) -> bool:
    """
    Descarga un asset completo (tile íntegro) desde una URL firmada.
    Utiliza streaming para manejar archivos grandes sin saturar la RAM.
    
    Args:
        asset_url: URL del asset (debe estar firmada).
        output_path: Ruta de destino para el archivo .tif.
        
    Returns:
        True si tuvo éxito, False en caso contrario.
    """
    try:
        logger.info("Iniciando descarga de tile completo: %s", output_path)
        
        with requests.get(asset_url, stream=True, timeout=60) as r:
            r.raise_for_status()
            with open(output_path, 'wb') as f:
                for chunk in r.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
                        
        logger.info("Descarga finalizada: %s", output_path)
        return True

    except Exception as exc:
        logger.error("Error descargando asset %s: %s", asset_url, exc)
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
            # Task 1.3: Ya no usamos geom para recorte durante descarga
            success = download_full_tile(signed_url, output_path)
            if success:
                downloaded.append(output_path)
        except Exception as exc:
            logger.error("Fallo crítico en banda %s: %s", band, exc)
            
        if progress_callback:
            progress_callback(i + 1, total, band)
            
    return downloaded
