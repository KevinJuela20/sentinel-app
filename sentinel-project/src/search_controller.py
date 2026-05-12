"""
search_controller.py
--------------------
Controlador de Búsqueda para el Sentinel Data Downloader.

Responsabilidades:
  - Formatear rangos de fechas para la API STAC.
  - Ejecutar consultas a la colección `sentinel-2-l2a` de Microsoft Planetary Computer.
  - Procesar y normalizar los metadatos de los items STAC encontrados.
  - Manejar errores de conexión y de lógica de negocio.
"""

import calendar
import logging
import re
from dataclasses import dataclass, field
from datetime import date
from typing import Optional


logger = logging.getLogger(__name__)

MPC_STAC_URL = "https://planetarycomputer.microsoft.com/api/stac/v1"
SENTINEL_COLLECTION = "sentinel-2-l2a"
ALLOWED_TILES = ["MPS", "MQT", "MQS"]


# ---------------------------------------------------------------------------
# Data classes
# ---------------------------------------------------------------------------


@dataclass
class STACItem:
    """Metadatos normalizados de un item STAC de Sentinel-2."""

    item_id: str
    datetime: str          # ISO 8601 (e.g. "2026-01-15T10:23:00Z")
    cloud_cover: float     # eo:cloud_cover (0–100)
    bbox: list[float] = field(default_factory=list)  # [minx, miny, maxx, maxy]
    assets: dict = field(default_factory=dict)  # nombre → href


@dataclass
class SearchResult:
    """Resultado de una búsqueda STAC."""

    items: list[STACItem] = field(default_factory=list)
    total: int = 0
    error: Optional[str] = None

    @property
    def success(self) -> bool:
        return self.error is None

    @property
    def has_results(self) -> bool:
        return self.total > 0


# ---------------------------------------------------------------------------
# Date utilities (Task 2.3)
# ---------------------------------------------------------------------------


def format_date_range(
    mes_inicio: int,
    anio_inicio: int,
    mes_fin: int,
    anio_fin: int,
) -> str:
    """
    Construye un string de rango de fechas en formato STAC datetime interval.

    Args:
        mes_inicio: Mes de inicio (1-12).
        anio_inicio: Año de inicio (e.g. 2026).
        mes_fin: Mes de fin (1-12).
        anio_fin: Año de fin (e.g. 2026).

    Returns:
        String con formato "YYYY-MM-DD/YYYY-MM-DD" que cubre el mes completo.

    Example:
        >>> format_date_range(1, 2026, 3, 2026)
        '2026-01-01/2026-03-31'
    """
    start = date(anio_inicio, mes_inicio, 1)
    # Último día del mes de fin
    last_day = calendar.monthrange(anio_fin, mes_fin)[1]
    end = date(anio_fin, mes_fin, last_day)
    return f"{start.isoformat()}/{end.isoformat()}"


def validate_date_range(
    mes_inicio: int,
    anio_inicio: int,
    mes_fin: int,
    anio_fin: int,
) -> Optional[str]:
    """
    Valida que el rango de fechas sea coherente (inicio ≤ fin).

    Returns:
        Mensaje de error si el rango es inválido, None si es correcto.
    """
    start = date(anio_inicio, mes_inicio, 1)
    last_day = calendar.monthrange(anio_fin, mes_fin)[1]
    end = date(anio_fin, mes_fin, last_day)

    if start > end:
        return (
            f"La fecha de inicio ({mes_inicio}/{anio_inicio}) no puede ser "
            f"posterior a la de fin ({mes_fin}/{anio_fin})."
        )
    return None


# ---------------------------------------------------------------------------
# Metadata processing (Task 2.4)
# ---------------------------------------------------------------------------


def _parse_item(item) -> STACItem:
    """
    Convierte un pystac.Item en un STACItem normalizado.

    Extrae:
        - item_id: identificador único del item.
        - datetime: fecha/hora de adquisición en ISO 8601.
        - cloud_cover: porcentaje de cobertura de nubes (eo:cloud_cover).
        - assets: diccionario {nombre: href} de los activos disponibles.
    """
    dt_value = item.datetime or item.properties.get("datetime", "")
    datetime_str = (
        dt_value.isoformat() if hasattr(dt_value, "isoformat") else str(dt_value)
    )
    cloud_cover = float(item.properties.get("eo:cloud_cover", 0.0))
    assets = {name: asset.href for name, asset in item.assets.items()}

    return STACItem(
        item_id=item.id,
        datetime=datetime_str,
        cloud_cover=cloud_cover,
        bbox=item.bbox,
        assets=assets,
    )



# ---------------------------------------------------------------------------
# Tile Filtering (Task 2.1 + 2.2)
# ---------------------------------------------------------------------------


def _extract_tile_id(item_id: str) -> Optional[str]:
    """
    Extrae el código MGRS (los últimos 3 caracteres) del item_id de Sentinel-2.
    
    Formato esperado: ..._T17MPS_... -> retorna "MPS"
    """
    # Patrón: _T seguido de 2 dígitos (zona UTM) y 3 letras (MGRS square)
    match = re.search(r"_T(\d{2})([A-Z]{3})_", item_id)
    if match:
        return match.group(2)
    return None


def _filter_by_tile(items: list[STACItem], allowed: list[str]) -> list[STACItem]:
    """
    Filtra una lista de STACItems conservando solo los tiles permitidos.
    """
    filtered = []
    for item in items:
        tile_id = _extract_tile_id(item.item_id)
        if tile_id is None:
            logger.warning("No se pudo extraer el tile ID de: %s. Se conserva por precaución.", item.item_id)
            filtered.append(item)
        elif tile_id in allowed:
            filtered.append(item)
        else:
            logger.info("Filtrando tile no deseado: %s (ID: %s)", tile_id, item.item_id)
    
    return filtered


def group_by_date(items: list[STACItem]) -> dict[str, list[STACItem]]:
    """
    Agrupa una lista de STACItems por su fecha (YYYY-MM-DD).
    """
    grouped = {}
    for item in items:
        # Extraer fecha YYYY-MM-DD del string ISO 8601
        date_str = item.datetime[:10]
        if date_str not in grouped:
            grouped[date_str] = []
        grouped[date_str].append(item)
    return grouped


# ---------------------------------------------------------------------------
# Search Controller (Tasks 2.2 + 4.1)
# ---------------------------------------------------------------------------


def search_images(
    mes_inicio: int,
    anio_inicio: int,
    mes_fin: int,
    anio_fin: int,
    geom_aoi: dict,
) -> SearchResult:
    """
    Busca imágenes Sentinel-2 L2A en MPC STAC dentro del rango de fechas
    y área de interés especificados.

    Args:
        mes_inicio: Mes de inicio (1-12).
        anio_inicio: Año de inicio.
        mes_fin: Mes de fin (1-12).
        anio_fin: Año de fin.
        geom_aoi: Geometría GeoJSON del área de interés (dict).

    Returns:
        SearchResult con la lista de STACItems y metadatos del resultado.
    """
    date_range = format_date_range(mes_inicio, anio_inicio, mes_fin, anio_fin)
    logger.info(
        "Buscando imágenes: colección=%s, fechas=%s", SENTINEL_COLLECTION, date_range
    )

    try:
        import pystac_client  # lazy import for testability
        import planetary_computer  # lazy import for testability

        catalog = pystac_client.Client.open(
            MPC_STAC_URL,
            modifier=planetary_computer.sign_inplace,
        )

        search = catalog.search(
            collections=[SENTINEL_COLLECTION],
            intersects=geom_aoi,
            datetime=date_range,
            sortby="-properties.datetime",
        )

        item_collection = search.item_collection()
        items = [_parse_item(item) for item in item_collection]

        # Filtrar por tiles permitidos (Task 2.3)
        total_raw = len(items)
        items = _filter_by_tile(items, ALLOWED_TILES)
        total_filtered = len(items)

        logger.info(
            "Búsqueda completada: %d imagen(es) encontradas (filtradas %d de %d)", 
            total_filtered, total_filtered, total_raw
        )
        return SearchResult(items=items, total=total_filtered)

    except Exception as exc:  # noqa: BLE001
        error_msg = _classify_error(exc)
        logger.error("Error durante la búsqueda STAC: %s", exc)
        return SearchResult(error=error_msg)


def _classify_error(exc: Exception) -> str:
    """
    Convierte una excepción técnica en un mensaje de error amigable para el usuario.
    """
    exc_str = str(exc).lower()
    if any(kw in exc_str for kw in ("connection", "timeout", "network", "connect")):
        return (
            "⚠️ No se pudo conectar con Microsoft Planetary Computer. "
            "Verifique su conexión a internet e intente de nuevo."
        )
    if "unauthorized" in exc_str or "403" in exc_str or "401" in exc_str:
        return (
            "⚠️ Error de autenticación con MPC. "
            "Verifique que `planetary-computer` esté correctamente configurado."
        )
    return f"⚠️ Error inesperado durante la búsqueda: {exc}"
