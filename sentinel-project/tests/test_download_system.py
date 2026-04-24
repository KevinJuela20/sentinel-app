"""
test_download_system.py
-----------------------
Pruebas para el sistema de descarga y gestión de archivos.
"""

import unittest
from unittest.mock import MagicMock, patch
from pathlib import Path
from src.file_manager import get_output_dir, get_band_filename, get_full_path
from src.downloader import sign_asset_url, download_item_bands

class TestFileManager(unittest.TestCase):
    def test_get_output_dir(self):
        with patch("src.file_manager.Path.mkdir") as mock_mkdir:
            path = get_output_dir("test_data", 2025, 1, 5)
            self.assertEqual(str(path), "test_data/2025/01/05")
            mock_mkdir.assert_called()

    def test_get_band_filename(self):
        fname = get_band_filename("item123", "B02", "2025-01-05")
        self.assertEqual(fname, "20250105_B02.tif")

class TestDownloader(unittest.TestCase):
    @patch("planetary_computer.sign_url")
    def test_sign_asset_url(self, mock_sign):
        mock_sign.return_value = "https://signed.url"
        res = sign_asset_url("https://orig.url")
        self.assertEqual(res, "https://signed.url")
        mock_sign.assert_called_once_with("https://orig.url")

    @patch("src.downloader.sign_asset_url")
    @patch("src.downloader.download_and_clip")
    def test_download_item_bands_orchestration(self, mock_clip, mock_sign):
        mock_sign.return_value = "signed"
        mock_clip.return_value = True
        
        # Mock item
        item = MagicMock()
        item.item_id = "item1"
        item.assets = {
            "B02": MagicMock(href="h2"),
            "B03": MagicMock(href="h3")
        }
        
        res = download_item_bands(
            item=item,
            bands=["B02", "B03"],
            geom={},
            output_dir=Path("out"),
            date_str="2025-01-01"
        )
        
        self.assertEqual(len(res), 2)
        self.assertEqual(mock_clip.call_count, 2)
        self.assertEqual(mock_sign.call_count, 2)

if __name__ == "__main__":
    unittest.main()
