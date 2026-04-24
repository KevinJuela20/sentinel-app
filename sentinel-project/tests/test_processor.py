"""
test_processor.py
-----------------
Pruebas para el motor de procesamiento y filtrado de nubes.
"""

import unittest
import numpy as np
from src.processor import is_crop_clean
from src.image_utils import normalize_band

class TestCloudFilter(unittest.TestCase):
    def test_clean_image(self):
        # Array de 10x10 ceros (Limpio)
        data = np.zeros((10, 10))
        clean, perc = is_crop_clean(data)
        self.assertTrue(clean)
        self.assertEqual(perc, 0.0)

    def test_cloudy_image(self):
        # Array de 10x10 con códigos de nube (8 = Cloud Medium Prob)
        data = np.full((10, 10), 8)
        clean, perc = is_crop_clean(data)
        self.assertFalse(clean)
        self.assertEqual(perc, 1.0)

    def test_threshold_border(self):
        # 5 píxeles de nube en un área de 100 (5%)
        data = np.zeros(100)
        data[:5] = 9 # Cloud High Prob
        clean, perc = is_crop_clean(data)
        self.assertTrue(clean) # 5% <= 5% umbral
        
        # 6 píxeles (6%)
        data[5] = 9
        clean, perc = is_crop_clean(data)
        self.assertFalse(clean)

class TestImageUtils(unittest.TestCase):
    def test_normalization(self):
        # 0 -> 0, 3000 -> 255
        data = np.array([0, 1500, 3000, 6000], dtype=np.uint16)
        res = normalize_band(data, 0, 3000)
        self.assertEqual(res[0], 0)
        self.assertEqual(res[2], 255)
        self.assertEqual(res[3], 255) # Clipped
        self.assertEqual(res.dtype, np.uint8)

if __name__ == "__main__":
    unittest.main()
