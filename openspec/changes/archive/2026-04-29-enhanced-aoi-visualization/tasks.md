## 1. Refinamiento de la Extensión del Lienzo

- [x] 1.1 Asegurar en `src/preview_engine.py` que `rasterio.mask.mask` se configure para devolver siempre la extensión total del AOI (esto debería ser el comportamiento por defecto con `crop=True` y shapes de AOI, pero se debe verificar el manejo de `nodata`).
- [x] 1.2 Garantizar que el canal Alfa cubra todo el bounding box del AOI, permitiendo que el contorno sea visible incluso donde no hay imagen satelital.

## 2. Mejora Estética de Imágenes

- [x] 2.1 Importar `PIL.ImageEnhance` en `src/preview_engine.py`.
- [x] 2.2 Aplicar un aumento de contraste (factor ~1.3) a la imagen satelital antes de superponer el contorno.
- [x] 2.3 Verificar que el color rojo sea exactamente `#FF0000` y el grosor sea de `2px` para máxima nitidez.

## 3. Verificación

- [x] 3.1 Verificar con un Tile de borde (como MQT) que el contorno rojo se extiende fuera de la imagen y es visible sobre el fondo oscuro de Streamlit.
- [x] 3.2 Validar que el contraste de la vegetación y las nubes sea superior al de la versión anterior.
