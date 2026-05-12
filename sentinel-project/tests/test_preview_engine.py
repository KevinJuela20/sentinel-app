"""
tests/test_preview_engine.py
----------------------------
Unit tests para el módulo src.preview_engine.
"""

import io
import pytest
from unittest.mock import MagicMock, patch
from PIL import Image
import numpy as np

from src.preview_engine import download_image, apply_aoi_mask, get_masked_preview


class TestPreviewEngine:
    
    @patch("src.preview_engine.requests.get")
    def test_download_image_success(self, mock_get):
        """Debe retornar bytes si la descarga es exitosa."""
        mock_response = MagicMock()
        mock_response.content = b"fake_image_bytes"
        mock_response.status_code = 200
        mock_get.return_value = mock_response
        
        result = download_image("https://example.com/image.jpg")
        assert result == b"fake_image_bytes"

    @patch("src.preview_engine.requests.get")
    def test_download_image_failure(self, mock_get):
        """Debe retornar None si la descarga falla."""
        mock_get.side_effect = Exception("Network error")
        result = download_image("https://example.com/image.jpg")
        assert result is None

    def test_apply_aoi_mask_draws_boundary_with_bbox(self):
        """Verifica que se dibujen píxeles rojos usando mapeo lineal por bbox."""
        # Crear una imagen PIL 100x100
        img = Image.new("RGB", (100, 100), color="black")
        img_bytes = io.BytesIO()
        img.save(img_bytes, format='PNG')
        
        aoi_geom = {
            "type": "Polygon",
            "coordinates": [[[10, 10], [90, 10], [90, 90], [10, 90], [10, 10]]]
        }
        # Bbox que cubre el área (0,0) a (100,100)
        bbox = [0, 0, 100, 100]
        
        # Ejecutar
        result = apply_aoi_mask(img_bytes.getvalue(), aoi_geom, bbox)
        
        # Convertir a numpy para buscar el color rojo (255, 0, 0)
        data = np.array(result)
        has_red = np.any((data[:, :, 0] == 255) & (data[:, :, 1] == 0) & (data[:, :, 2] == 0))
        assert has_red, "No se encontró el contorno rojo en la imagen resultante"
        assert result.size == (100, 100)

    @patch("src.preview_engine.download_image")
    @patch("src.preview_engine.apply_aoi_mask")
    def test_get_masked_preview_orchestration(self, mock_apply, mock_download):
        """Verifica que el orquestador llame a descarga y procesamiento con bbox."""
        mock_download.return_value = b"bytes"
        mock_apply.return_value = MagicMock(spec=Image.Image)
        bbox = [0, 0, 1, 1]
        
        result = get_masked_preview("http://url", {}, bbox)
        
        mock_download.assert_called_with("http://url")
        mock_apply.assert_called_with(b"bytes", {}, bbox)
        assert result is not None
