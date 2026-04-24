"""
verify_sr.py
------------
Script de verificación para el motor de super-resolución.
"""

import os
import sys
from pathlib import Path
import cv2

# Agregar src al path
sys.path.append(str(Path(__file__).parent.parent / "src"))

from super_resolution import SuperResEngine

def verify():
    base_dir = Path(__file__).parent
    sample_input = base_dir / "Data_Sentinel/2025/08/08/crops/1051_20250808.png"
    sample_output = base_dir / "Data_Sentinel/2025/08/08/super_res/1051_20250808_SR.png"
    
    if not sample_input.exists():
        print(f"❌ No se encontró la imagen de prueba: {sample_input}")
        return

    print(f"🚀 Iniciando super-resolución para: {sample_input.name}")
    
    engine = SuperResEngine()
    
    # Asegurar carpeta super_res
    sample_output.parent.mkdir(exist_ok=True)
    
    success = engine.upscale(str(sample_input), str(sample_output))
    
    if success and sample_output.exists():
        img = cv2.imread(str(sample_output))
        h, w = img.shape[:2]
        print(f"✅ ÉXITO: Imagen escalada generada.")
        print(f"   - Dimensiones: {w}x{h}")
        print(f"   - Ruta: {sample_output}")
        if w == 1024 and h == 1024:
            print("   - Resolución correcta (1024x1024)")
        else:
            print(f"   - ⚠️ Resolución inesperada: {w}x{h}")
    else:
        print("❌ FALLO: No se pudo generar la imagen escalada.")

if __name__ == "__main__":
    verify()
