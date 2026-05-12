"""
file_manager.py
---------------
Gestor del sistema de archivos para descargas de Sentinel-2.

Responsabilidades:
  - Crear la estructura de directorios Data_Sentinel/[Año]/[Mes]/[Día].
  - Generar rutas estandarizadas para archivos de bandas.
"""

import logging
import re
from pathlib import Path

logger = logging.getLogger(__name__)

# Bandas que se descargan por defecto
DEFAULT_BANDS = ["B02", "B03", "B04", "SCL"]


def get_output_dir(base_dir: str, year: int, month: int, day: int) -> Path:
    """
    Genera y crea la ruta de salida jerárquica.

    Args:
        base_dir: Directorio raíz (ej: "Data_Sentinel").
        year: Año de la adquisición.
        month: Mes de la adquisición.
        day: Día de la adquisición.

    Returns:
        Objeto Path del directorio creado.
    """
    path = Path(base_dir) / str(year) / f"{month:02d}" / f"{day:02d}"
    path.mkdir(parents=True, exist_ok=True)
    logger.info("Directorio de salida: %s", path)
    return path


def get_band_filename(item_id: str, band_name: str, date_str: str) -> str:
    """
    Genera un nombre de archivo estandarizado para una banda.

    Args:
        item_id: ID del item STAC.
        band_name: Nombre de la banda (B02, B03, etc.).
        date_str: Fecha de adquisición en formato YYYY-MM-DD.

    Returns:
        Nombre de archivo (ej: "20250101_B02.tif").
    """
    # Convertir date_str a formato compacto: YYYY-MM-DD -> YYYYMMDD
    date_compact = date_str.replace("-", "")
    
    # Extraer el tile ID (MGRS square) del item_id
    tile_id = "TILE"
    match = re.search(r"_T(\d{2})([A-Z]{3})_", item_id)
    if match:
        tile_id = match.group(2)
        
    return f"{date_compact}_{tile_id}_{band_name}.tif"


def get_full_path(base_dir: str, year: int, month: int, day: int,
                  item_id: str, band_name: str, date_str: str) -> Path:
    """
    Genera la ruta completa (directorio + nombre de archivo) para una banda.

    Args:
        base_dir: Directorio raíz.
        year, month, day: Componentes de la fecha.
        item_id: ID del item STAC.
        band_name: Nombre de la banda.
        date_str: Fecha en formato YYYY-MM-DD.

    Returns:
        Ruta completa al archivo de destino.
    """
    output_dir = get_output_dir(base_dir, year, month, day)
    filename = get_band_filename(item_id, band_name, date_str)
    return output_dir / filename


def check_date_data_exists(base_dir: str, year: int, month: int, day: int, 
                           items: list, bands: list, date_str: str) -> bool:
    """
    Verifica si todos los archivos .tif necesarios para una fecha ya existen.
    
    Args:
        base_dir: Directorio raíz.
        year, month, day: Componentes de la fecha.
        items: Lista de STACItems para esa fecha.
        bands: Lista de bandas requeridas (ej: DEFAULT_BANDS).
        date_str: Fecha en formato YYYY-MM-DD.
        
    Returns:
        True si todos los archivos existen, False en caso contrario.
    """
    output_dir = Path(base_dir) / str(year) / f"{month:02d}" / f"{day:02d}"
    if not output_dir.exists():
        return False
        
    for item in items:
        for band in bands:
            filename = get_band_filename(item.item_id, band, date_str)
            if not (output_dir / filename).exists():
                logger.debug("Falta archivo: %s", filename)
                return False
                
    return True
