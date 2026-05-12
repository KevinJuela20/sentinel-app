## Why

El objetivo es maximizar la utilidad visual de las previsualizaciones de Sentinel-2 para el analista. Al superponer el contorno completo de la zona de estudio (AOI) sobre cada tile, incluso si el tile solo cubre una parte, el usuario puede identificar instantáneamente qué fracción de su área de interés está capturada en esa fecha y tile ID específicos. Esto evita descargas innecesarias de imágenes con cobertura parcial insuficiente. Además, se busca una estética de "alto contraste" y "nitidez profesional" que destaque la vegetación y las nubes contra el fondo oscuro de la interfaz.

## What Changes

- **Optimizar** `src/preview_engine.py` para asegurar que el lienzo de la imagen generada siempre abarque la extensión total del AOI, independientemente del tamaño del tile.
- **Mejorar** la estética del contorno: asegurar un rojo vibrante (#FF0000) y un grosor constante que se mantenga nítido.
- **Aplicar** un ligero ajuste de contraste/brillo opcional a los thumbnails para que los detalles de nubes y vegetación sean más "vibrantes".
- **Asegurar** que las partes del AOI no cubiertas por el tile sean visibles como un contorno rojo sobre el fondo oscuro (transparente en el PNG resultante).

## Capabilities

### Modified Capabilities

- `aoi-overlay`: Refinamiento de la capacidad existente para garantizar la visibilidad total del contorno del AOI y mejorar el contraste visual de la previsualización.
- `UC-02-previsualizar-imagen-mascara`: Se eleva el estándar de calidad visual del thumbnail renderizado.

## Impact

- **Código**: `src/preview_engine.py` (ajustes en `apply_aoi_mask` y lógica de extensión).
- **UX**: Mayor claridad sobre la cobertura espacial de los resultados de búsqueda.
- **Rendimiento**: Mínimo impacto, ya que la mayoría del procesamiento se realiza sobre thumbnails de baja resolución.
