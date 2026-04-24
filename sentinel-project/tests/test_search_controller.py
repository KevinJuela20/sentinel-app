"""
tests/test_search_controller.py
-------------------------------
Unit tests para el módulo src.search_controller.
Cobertura objetivo: >= 80%
"""

import pytest
from datetime import date
from unittest.mock import MagicMock, patch

from src.search_controller import (
    STACItem,
    SearchResult,
    _classify_error,
    _parse_item,
    format_date_range,
    search_images,
    validate_date_range,
)


# ---------------------------------------------------------------------------
# format_date_range (Task 2.3)
# ---------------------------------------------------------------------------

class TestFormatDateRange:
    def test_same_month(self):
        """Un solo mes debe abarcar del día 1 al último día del mes."""
        result = format_date_range(1, 2026, 1, 2026)
        assert result == "2026-01-01/2026-01-31"

    def test_multi_month_range(self):
        """Rango de 3 meses."""
        result = format_date_range(1, 2026, 3, 2026)
        assert result == "2026-01-01/2026-03-31"

    def test_february_non_leap_year(self):
        """Febrero en año no bisiesto debe terminar el 28."""
        result = format_date_range(2, 2025, 2, 2025)
        assert result == "2025-02-01/2025-02-28"

    def test_february_leap_year(self):
        """Febrero en año bisiesto debe terminar el 29."""
        result = format_date_range(2, 2024, 2, 2024)
        assert result == "2024-02-01/2024-02-29"

    def test_cross_year_range(self):
        """Rango que cruza dos años."""
        result = format_date_range(11, 2025, 2, 2026)
        assert result == "2025-11-01/2026-02-28"

    def test_december(self):
        """Diciembre debe terminar el 31."""
        result = format_date_range(12, 2025, 12, 2025)
        assert result == "2025-12-01/2025-12-31"


# ---------------------------------------------------------------------------
# validate_date_range (Task 4.2)
# ---------------------------------------------------------------------------

class TestValidateDateRange:
    def test_valid_range_returns_none(self):
        """Un rango válido debe retornar None (sin errores)."""
        result = validate_date_range(1, 2026, 3, 2026)
        assert result is None

    def test_same_month_valid(self):
        """Mismo mes y año debe ser válido."""
        result = validate_date_range(6, 2025, 6, 2025)
        assert result is None

    def test_invalid_range_returns_message(self):
        """Si inicio > fin, debe retornar un mensaje de error."""
        result = validate_date_range(6, 2026, 1, 2026)
        assert result is not None
        assert isinstance(result, str)
        assert len(result) > 0

    def test_invalid_range_message_contains_dates(self):
        """El mensaje de error debe mencionar las fechas problemáticas."""
        result = validate_date_range(12, 2026, 1, 2026)
        assert "12" in result
        assert "2026" in result


# ---------------------------------------------------------------------------
# _parse_item (Task 2.4)
# ---------------------------------------------------------------------------

class TestParseItem:
    def _make_mock_item(self, item_id="S2A_001", cloud_cover=12.5, dt="2026-01-15"):
        """Crea un mock de pystac.Item."""
        item = MagicMock()
        item.id = item_id
        item.datetime = date.fromisoformat(dt)
        item.properties = {
            "eo:cloud_cover": cloud_cover,
            "datetime": dt,
        }
        # assets
        asset_b02 = MagicMock()
        asset_b02.href = "https://example.com/B02.tif"
        asset_b04 = MagicMock()
        asset_b04.href = "https://example.com/B04.tif"
        item.assets = {"B02": asset_b02, "B04": asset_b04}
        return item

    def test_parses_item_id(self):
        item = _parse_item(self._make_mock_item(item_id="S2A_TEST"))
        assert item.item_id == "S2A_TEST"

    def test_parses_cloud_cover(self):
        item = _parse_item(self._make_mock_item(cloud_cover=23.7))
        assert item.cloud_cover == pytest.approx(23.7)

    def test_parses_assets(self):
        item = _parse_item(self._make_mock_item())
        assert "B02" in item.assets
        assert "B04" in item.assets
        assert item.assets["B02"] == "https://example.com/B02.tif"

    def test_parses_datetime_string(self):
        item = _parse_item(self._make_mock_item(dt="2026-03-20"))
        assert "2026-03-20" in item.datetime


# ---------------------------------------------------------------------------
# search_images (Task 2.2 + 4.1)
# ---------------------------------------------------------------------------

class TestSearchImages:
    DUMMY_AOI = {"type": "Polygon", "coordinates": [[[0, 0], [1, 0], [1, 1], [0, 0]]]}

    def _make_mock_modules(self):
        """Crea mocks de pystac_client y planetary_computer para inyectar en sys.modules."""
        mock_pc = MagicMock()
        mock_pc.sign_inplace = lambda x: x

        mock_pystac = MagicMock()
        return mock_pystac, mock_pc

    def test_returns_items_on_success(self):
        """Debe retornar SearchResult con items cuando la búsqueda funciona."""
        import sys
        mock_pystac, mock_pc = self._make_mock_modules()

        mock_item = MagicMock()
        mock_item.id = "S2A_001"
        mock_item.datetime = date(2026, 1, 15)
        mock_item.properties = {"eo:cloud_cover": 5.0}
        mock_item.assets = {}

        mock_search = MagicMock()
        mock_search.item_collection.return_value = [mock_item]
        mock_pystac.Client.open.return_value.search.return_value = mock_search

        with patch.dict(sys.modules, {"pystac_client": mock_pystac, "planetary_computer": mock_pc}):
            result = search_images(1, 2026, 1, 2026, self.DUMMY_AOI)

        assert result.success
        assert result.total == 1
        assert result.items[0].item_id == "S2A_001"

    def test_returns_empty_result_when_no_images(self):
        """Debe retornar SearchResult con 0 items cuando no hay resultados."""
        import sys
        mock_pystac, mock_pc = self._make_mock_modules()

        mock_search = MagicMock()
        mock_search.item_collection.return_value = []
        mock_pystac.Client.open.return_value.search.return_value = mock_search

        with patch.dict(sys.modules, {"pystac_client": mock_pystac, "planetary_computer": mock_pc}):
            result = search_images(1, 2000, 1, 2000, self.DUMMY_AOI)

        assert result.success
        assert result.total == 0
        assert not result.has_results

    def test_returns_error_on_connection_failure(self):
        """Debe retornar SearchResult con error cuando falla la conexión."""
        import sys
        mock_pystac, mock_pc = self._make_mock_modules()
        mock_pystac.Client.open.side_effect = ConnectionError("connection refused")

        with patch.dict(sys.modules, {"pystac_client": mock_pystac, "planetary_computer": mock_pc}):
            result = search_images(1, 2026, 1, 2026, self.DUMMY_AOI)

        assert not result.success
        assert result.error is not None
        assert "conectar" in result.error.lower() or "connection" in result.error.lower()


# ---------------------------------------------------------------------------
# _classify_error
# ---------------------------------------------------------------------------

class TestClassifyError:
    def test_connection_error_message(self):
        exc = ConnectionError("connection timeout")
        msg = _classify_error(exc)
        assert "Planetary Computer" in msg

    def test_auth_error_message(self):
        exc = Exception("unauthorized 401")
        msg = _classify_error(exc)
        assert "autenticación" in msg.lower() or "mpc" in msg.lower()

    def test_unknown_error_message(self):
        exc = RuntimeError("algo raro pasó")
        msg = _classify_error(exc)
        assert "⚠️" in msg


# ---------------------------------------------------------------------------
# SearchResult
# ---------------------------------------------------------------------------

class TestSearchResult:
    def test_success_true_when_no_error(self):
        r = SearchResult(items=[], total=0, error=None)
        assert r.success is True

    def test_success_false_when_error(self):
        r = SearchResult(error="algo falló")
        assert r.success is False

    def test_has_results_true_when_items(self):
        r = SearchResult(items=[MagicMock()], total=1)
        assert r.has_results is True

    def test_has_results_false_when_empty(self):
        r = SearchResult(items=[], total=0)
        assert r.has_results is False
