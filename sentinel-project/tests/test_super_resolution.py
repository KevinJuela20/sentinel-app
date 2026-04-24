"""
test_super_resolution.py
------------------------
Pruebas para el motor de super-resolución.
"""

import unittest
from unittest.mock import MagicMock, patch
from pathlib import Path
from src.super_resolution import SuperResEngine

class TestSuperResEngine(unittest.TestCase):
    @patch("cv2.dnn_superres.DnnSuperResImpl_create")
    def test_load_models_missing(self, mock_create):
        # Test cuando no existen los archivos .pb
        engine = SuperResEngine(models_dir="non_existent")
        res = engine.load_models()
        self.assertFalse(res)

    @patch("cv2.dnn_superres.DnnSuperResImpl_create")
    @patch("pathlib.Path.exists")
    def test_load_models_success(self, mock_exists, mock_create):
        mock_exists.return_value = True
        mock_sr = MagicMock()
        mock_create.return_value = mock_sr
        
        engine = SuperResEngine(models_dir="mock_models")
        res = engine.load_models()
        
        self.assertTrue(res)
        self.assertEqual(mock_sr.readModel.call_count, 2)
        self.assertEqual(mock_sr.setModel.call_count, 2)

    @patch("cv2.imread")
    @patch("cv2.imwrite")
    @patch("cv2.dnn_superres.DnnSuperResImpl_create")
    @patch("pathlib.Path.exists")
    def test_upscale_pipeline(self, mock_exists, mock_create, mock_write, mock_read):
        mock_exists.return_value = True
        mock_read.return_value = np.zeros((128, 128, 3), dtype=np.uint8)
        
        mock_sr = MagicMock()
        mock_sr.upsample.side_effect = [
            np.zeros((512, 512, 3), dtype=np.uint8),  # x4
            np.zeros((1024, 1024, 3), dtype=np.uint8) # x2
        ]
        mock_create.return_value = mock_sr
        
        engine = SuperResEngine(models_dir="mock_models")
        engine._models_loaded = True # Saltar carga real
        
        res = engine.upscale("input.png", "output.png")
        
        self.assertTrue(res)
        self.assertEqual(mock_sr.upsample.call_count, 2)
        mock_write.assert_called_once()

import numpy as np # Necesario para los mocks

if __name__ == "__main__":
    unittest.main()
