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

    def test_apply_aoi_mask_without_rasterio(self):
        """Si rasterio no está disponible, debe retornar la imagen original convertida a RGBA."""
        # Forzar que rasterio parezca no estar disponible
        with patch("src.preview_engine.rasterio", None):
            # Crear una imagen PIL pequeña en bytes
            img = Image.new("RGB", (10, 10), color="red")
            img_byte_arr = io.BytesIO()
            img.save(img_byte_arr, format='PNG')
            img_bytes = img_byte_arr.getvalue()
            
            result = apply_aoi_mask(img_bytes, {"type": "Point", "coordinates": [0,0]})
            assert result.mode == "RGBA"
            assert result.size == (10, 10)

    def test_apply_aoi_mask_with_rasterio_mock(self):
        """Verifica que se llame a la lógica de masking de rasterio usando inyección de sys.modules."""
        import sys
        from unittest.mock import MagicMock, patch
        
        # Mocks para rasterio
        mock_rasterio = MagicMock()
        mock_mask_mod = MagicMock()
        mock_memfile_mod = MagicMock()
        
        fake_out_image = np.zeros((3, 5, 5), dtype=np.uint8)
        mock_mask_mod.mask.return_value = (fake_out_image, MagicMock())
        
        modules = {
            "rasterio": mock_rasterio,
            "rasterio.mask": mock_mask_mod,
            "rasterio.memoryfile": mock_memfile_mod
        }
        
        with patch.dict(sys.modules, modules):
            # Re-parchear los nombres que se importaron dentro del módulo
            # Usar create=True porque estos nombres pueden no existir si rasterio no está instalado
            with patch("src.preview_engine.rasterio", mock_rasterio, create=True), \
                 patch("src.preview_engine.mask", mock_mask_mod.mask, create=True), \
                 patch("src.preview_engine.MemoryFile", mock_memfile_mod.MemoryFile, create=True):
                
                img = Image.new("RGB", (10, 10))
                img_bytes = io.BytesIO()
                img.save(img_bytes, format='PNG')
                
                # Ejecutar
                result = apply_aoi_mask(img_bytes.getvalue(), {"type": "Polygon", "coordinates": []})
                
                assert mock_mask_mod.mask.called
                assert isinstance(result, Image.Image)
                assert result.mode == "RGBA"

    @patch("src.preview_engine.download_image")
    @patch("src.preview_engine.apply_aoi_mask")
    def test_get_masked_preview_orchestration(self, mock_apply, mock_download):
        """Verifica que el orquestador llame a descarga y máscara."""
        mock_download.return_value = b"bytes"
        mock_apply.return_value = MagicMock(spec=Image.Image)
        
        result = get_masked_preview("http://url", {})
        
        mock_download.assert_called_with("http://url")
        mock_apply.assert_called_with(b"bytes", {})
        assert result is not None
