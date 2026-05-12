## Why

Actualmente, el motor de previsualización descarga y procesa los thumbnails de cada item STAC (Sentinel-2) de forma secuencial. Cuando una búsqueda retorna múltiples resultados, esta operación de red y procesamiento I/O-bound provoca un tiempo de espera significativo antes de que se renderice la galería en la interfaz de Streamlit. Paralelizar esta carga mejorará drásticamente la capacidad de respuesta de la aplicación y la experiencia del usuario.

## What Changes

- Implementación de un proceso de descarga y procesamiento en paralelo para las imágenes de previsualización.
- Utilización de `concurrent.futures.ThreadPoolExecutor` para pre-cargar los thumbnails antes de renderizar la galería.
- Mantenimiento del comportamiento de superposición del AOI, pero ejecutado concurrentemente para múltiples tiles.

## Capabilities

### New Capabilities
*(Ninguna)*

### Modified Capabilities
- `UC-02-previsualizar-imagen-mascara`: Se modifica la especificación técnica subyacente para asegurar el cumplimiento del criterio de aceptación "Los thumbnails se cargan asíncronamente sin bloquear la interfaz", especificando que la carga y procesamiento de la máscara deben realizarse en paralelo para mejorar el rendimiento.

## Impact

- **app.py**: Modificación en el flujo de renderizado de `_render_results` para pre-ejecutar en paralelo la obtención de las imágenes de las tarjetas (`_get_cached_preview`).
- **Rendimiento**: Reducción del tiempo total de renderizado de la galería de O(N) a O(N/T) donde T es el número de hilos.
- **Trazabilidad**: Cumple con mejoras de rendimiento vinculadas a RF-02 / UC-02.
