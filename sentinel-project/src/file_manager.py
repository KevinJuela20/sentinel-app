"""
file_manager.py
---------------
Gestor del sistema de archivos para descargas de Sentinel-2.

Responsabilidades:
  - Crear la estructura de directorios Data_Sentinel/[Año]/[Mes]/[Día].
  - Generar rutas estandarizadas para archivos de bandas.
"""

import logging
from pathlib import Path

logger = logging.getLogger(__name__)

# Bandas que se descargan por defecto
DEFAULT_BANDS = ["B02", "B03", "B04", "SCL", "visual"]


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
    return f"{date_compact}_{band_name}.tif"


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
