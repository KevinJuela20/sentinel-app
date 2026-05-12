"""
tests/test_geo_utils.py
-----------------------
Unit tests para el módulo src.geo_utils.
Cobertura objetivo: >= 80%
"""

import json
import pytest
from pathlib import Path
from unittest.mock import MagicMock, patch

from src.geo_utils import load_aoi, load_geojson


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

KML_PATH = str(Path(__file__).parent.parent / "external" / "ARH_MAP.kml")
GEOJSON_PATH = str(Path(__file__).parent.parent / "external" / "cuadricula_arh.geojson")


# ---------------------------------------------------------------------------
# load_aoi
# ---------------------------------------------------------------------------

class TestLoadAoi:
    def test_raises_file_not_found_for_missing_kml(self):
        """Debe lanzar FileNotFoundError si el archivo no existe."""
        with pytest.raises(FileNotFoundError, match="no encontrado"):
            load_aoi("/ruta/inexistente/archivo.kml")

    def test_returns_geojson_dict(self):
        """Debe retornar un dict GeoJSON cuando el archivo es válido."""
        import sys

        mock_gpd = MagicMock()
        mock_fiona = MagicMock()
        mock_shapely_mapping = MagicMock(return_value={"type": "Polygon", "coordinates": []})

        fake_gdf = MagicMock()
        fake_gdf.empty = False
        fake_gdf.__len__ = lambda self: 1
        fake_gdf.geometry.union_all.return_value = MagicMock()

        mock_gpd.read_file.return_value = fake_gdf

        with patch.dict(sys.modules, {"geopandas": mock_gpd, "fiona": mock_fiona}):
            with patch("src.geo_utils.Path.exists", return_value=True):
                with patch("src.geo_utils.mapping", mock_shapely_mapping):
                    result = load_aoi("fake.kml")

        assert isinstance(result, dict)
        assert "type" in result

    def test_raises_value_error_for_empty_kml(self):
        """Debe lanzar ValueError si el KML no tiene geometrías."""
        import sys

        mock_gpd = MagicMock()
        mock_fiona = MagicMock()
        empty_gdf = MagicMock()
        empty_gdf.empty = True
        mock_gpd.read_file.return_value = empty_gdf

        with patch.dict(sys.modules, {"geopandas": mock_gpd, "fiona": mock_fiona}):
            with patch("src.geo_utils.Path.exists", return_value=True):
                with pytest.raises(Exception):
                    load_aoi("fake_empty.kml")

    def test_load_real_kml_if_exists(self):
        """Prueba de integración: carga el KML real si existe en external/."""
        pytest.importorskip("geopandas", reason="geopandas no instalado en este entorno")
        if not Path(KML_PATH).exists():
            pytest.skip("Archivo KML real no disponible en external/")
        result = load_aoi(KML_PATH)
        assert isinstance(result, dict)
        assert "type" in result


# ---------------------------------------------------------------------------
# load_geojson
# ---------------------------------------------------------------------------

class TestLoadGeojson:
    def test_raises_file_not_found_for_missing_geojson(self):
        """Debe lanzar FileNotFoundError si el archivo no existe."""
        pytest.importorskip("geopandas", reason="geopandas no instalado en este entorno")
        with pytest.raises(FileNotFoundError, match="no encontrado"):
            load_geojson("/ruta/inexistente/archivo.geojson")

    def test_load_real_geojson_if_exists(self):
        """Prueba de integración: carga el GeoJSON real si existe en external/."""
        pytest.importorskip("geopandas", reason="geopandas no instalado en este entorno")
        if not Path(GEOJSON_PATH).exists():
            pytest.skip("Archivo GeoJSON real no disponible en external/")
        gdf = load_geojson(GEOJSON_PATH)
        assert len(gdf) > 0
