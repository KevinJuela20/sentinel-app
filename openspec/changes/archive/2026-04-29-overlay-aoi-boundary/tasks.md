## 1. Utilidades de Proyección

- [x] 1.1 Implementar función helper en `src/preview_engine.py` para proyectar coordenadas lon/lat a píxeles usando la transformación de rasterio (inversa de `out_transform`)

## 2. Lógica de Dibujo del AOI

- [x] 2.1 Modificar `apply_aoi_mask` en `src/preview_engine.py` para importar `PIL.ImageDraw`
- [x] 2.2 Integrar el dibujo del contorno rojo (#FF0000) de 2px de grosor después del recorte y antes de retornar la imagen PIL
- [x] 2.3 Manejar el dibujo de múltiples anillos (exteriors e interiors) para soportar MultiPolygons o agujeros

## 3. Tests Unitarios

- [x] 3.1 Crear test en `tests/test_preview_engine.py` para verificar que la imagen resultante tiene píxeles rojos en el contorno esperado (mock de la imagen y transformación)

## 4. Verificación

- [x] 4.1 Ejecutar suite de tests completa (`python -m pytest tests/`)
- [x] 4.2 Verificar manualmente en la UI de Streamlit que las imágenes de la galería muestran el contorno rojo superpuesto y alineado correctamente
