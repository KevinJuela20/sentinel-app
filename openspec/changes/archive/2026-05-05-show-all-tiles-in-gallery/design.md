## Context

El sistema actual agrupa imágenes por fecha pero solo renderiza una previsualización representativa por cada día. Dado que la zona de estudio (AOI) es cubierta por la intersección de tres tiles diferentes de Sentinel-2, mostrar solo uno deja al usuario con un punto ciego sobre el estado de las otras dos áreas.

## Goals / Non-Goals

**Goals:**
- Mostrar de forma explícita los tres tiles (ej: 17MPS, 17MQT, 17MQS) por cada fecha encontrada.
- Permitir la visualización individual de la cobertura de nubes por tile.
- Mantener la eficiencia de carga mediante el uso de hilos para las previsualizaciones.

**Non-Goals:**
- No se permitirá la selección individual de tiles dentro de una fecha (se mantiene la lógica de "todo o nada" por fecha para asegurar consistencia en el procesamiento posterior).

## Decisions

### 1. Nueva Estructura de la Galería
**Decisión**: Cambiar de una cuadrícula de fechas (3xN) a una lista vertical de fechas. Cada fila de fecha contendrá una sub-cuadrícula de 3 columnas para los tiles.
**Racional**: Proporciona suficiente espacio horizontal para apreciar el detalle de cada tile y su intersección con el AOI sin saturar la pantalla.

### 2. Carga de Previsualizaciones (Multi-item)
**Decisión**: Modificar el bucle de pre-carga paralela para que procese todos los items de cada fecha, no solo el primero.
**Racional**: Asegura que para cuando el usuario llegue a la sección de resultados, las tres imágenes de cada fecha ya estén en la caché de Streamlit.

### 3. Información por Tile
**Decisión**: Cada imagen de tile mostrará un subtítulo con su ID de tile y su porcentaje de nubes específico.
**Racional**: Permite al usuario identificar rápidamente cuál de los tres tiles es el que está obstruido por nubes en caso de que el promedio de la fecha sea engañoso.

## Risks / Trade-offs

- **[Riesgo] Rendimiento de Red** → Solicitar 3x más previsualizaciones puede ralentizar la carga inicial. *Mitigación*: Se mantendrá el `ThreadPoolExecutor` con un límite de hilos adecuado y se utilizará `st.cache_data`.
- **[Trade-off] Altura de Página** → La galería será significativamente más larga verticalmente. *Racional*: Es una compensación aceptable por la transparencia en la calidad de los datos.
