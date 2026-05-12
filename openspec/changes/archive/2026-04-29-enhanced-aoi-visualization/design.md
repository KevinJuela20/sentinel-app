## Context

El sistema actual ya realiza un recorte y dibuja un contorno. Sin embargo, para cumplir con el requisito de que el contorno se extienda perfectamente fuera del tile y sea "nítido y vibrante", debemos asegurar que el `rasterio.mask` se ejecute de manera que la imagen de salida tenga las dimensiones de la caja delimitadora (bbox) del AOI completo, no solo de la intersección.

## Goals / Non-Goals

**Goals:**
- El lienzo de la imagen final debe ser el bounding box del AOI.
- El contorno rojo debe ser completo (360 grados del perímetro del AOI).
- Las áreas donde el tile no llega deben ser transparentes (dejando ver el fondo oscuro de la app).
- Mejorar el contraste de la imagen satelital para destacar vegetación y nubes.

**Non-Goals:**
- Procesar imágenes de alta resolución (se sigue trabajando con thumbnails).
- Cambiar el archivo KML de origen (`ARH_ETAPA.kml`).

## Components

### src/preview_engine.py

**Ajuste en `apply_aoi_mask`:**
- Al llamar a `mask(src, [aoi_geom], crop=True)`, rasterio ajusta la salida a la geometría proporcionada. Si el AOI es más grande que el tile, rasterio rellenará con el valor de `nodata` (usualmente 0) las áreas externas al tile pero internas al AOI. 
- Debemos asegurar que el canal Alfa se genere correctamente para todo el lienzo del AOI.
- **Mejora Estética:** Usar `PIL.ImageEnhance.Contrast` para aumentar el contraste de la imagen satelital antes de dibujar el contorno.

### Estética del Contorno
- Color: `#FF0000` (Rojo puro).
- Grosor: `2px` o `3px` según se vea mejor en la UI (se probará `2px` primero por ser más "nítido").
- Estilo: Línea continua.

## Decisions

### Decisión 1: Extensión del Lienzo

**Decision:** Forzar que la previsualización tenga la extensión del AOI.
**Rationale:** Esto garantiza que el contorno rojo sea siempre el mismo tamaño y forma, sirviendo como "marco" constante. El tile "llenará" la parte del marco que le corresponda geográficamente.

### Decisión 2: Realce de Imagen (Enhancement)

**Decision:** Aplicar un factor de contraste de 1.2 o 1.3.
**Rationale:** Las imágenes "rendered_preview" de MPC a veces se ven algo lavadas. Un ligero realce de contraste hará que las nubes sean más blancas y el bosque más verde, cumpliendo con el requisito de "alto contraste".

## Risks / Trade-offs

- **[Caché de Streamlit]** -> Las imágenes anteriores en caché no tendrán el nuevo estilo. **Mitigación:** El cambio en la lógica de `preview_engine` invalidará implícitamente el caché al cambiar el resultado de la función.
- **[AOIs muy grandes]** -> Si el AOI es mucho más grande que el tile, el tile se verá muy pequeño en la card. **Mitigación:** Esto es precisamente lo que el usuario quiere ver para evaluar la cobertura.
