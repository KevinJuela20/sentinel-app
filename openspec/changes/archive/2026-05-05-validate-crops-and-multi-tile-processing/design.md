## Context

El sistema actual fragmenta un área de estudio (AOI) en una cuadrícula de celdas y genera recortes PNG para el entrenamiento de modelos de IA. Con la reciente integración de descargas multi-tile (MPS, MQT, MQS), el motor de procesamiento debe evolucionar para manejar múltiples archivos fuente por fecha y filtrar recortes incompletos que ocurren en las fronteras de los tiles.

## Goals / Non-Goals

**Goals:**
- Validar que cada recorte tenga dimensiones mínimas de 124x124 píxeles antes de ser procesado.
- Redimensionar todos los recortes válidos a un tamaño estándar de 128x128 píxeles.
- Procesar todos los tiles disponibles en una carpeta de fecha.
- Evitar colisiones de nombres de archivos cuando una celda es cubierta por múltiples tiles.

**Non-Goals:**
- No se busca fusionar (mosaicing) recortes de diferentes tiles para completar celdas de borde.
- No se modificará la lógica de detección de nubes existente (umbral SCL).

## Decisions

### 1. Validación de Dimensiones en el Origen
**Decisión**: Realizar la validación de tamaño ($W \ge 124$ y $H \ge 124$) inmediatamente después de la operación `mask` en `src/processor.py`.
**Racional**: Descartar fragmentos de borde lo antes posible ahorra recursos computacionales y evita guardar archivos inútiles.
**Alternativa**: Validar en el motor de súper-resolución. *Rechazada* porque generaría archivos PNG basura en disco.

### 2. Normalización de Tamaño en `image_utils`
**Decisión**: Integrar el redimensionamiento a 128x128 usando interpolación cúbica en la función `save_rgb_png`.
**Racional**: Centraliza la responsabilidad de formato de salida en la utilidad de imagen, garantizando que el pipeline EDSR reciba siempre la entrada esperada.

### 3. Orquestación Multi-tile
**Decisión**: Modificar `process_all_grids` para agrupar los archivos `.tif` por su identificador de Tile (MGRS).
**Racional**: Permite ejecutar el procesamiento de la cuadrícula de forma independiente para cada tile, maximizando la recolección de datos en áreas de solapamiento.

### 4. Nomenclatura de Recortes
**Decisión**: Cambiar el formato de nombre de `cellID_date.png` a `cellID_date_tileID.png`.
**Racional**: Previene la sobreescritura de archivos y permite trazar el origen de cada recorte.

## Risks / Trade-offs

- **[Riesgo] Reducción de Datos** → El filtro de 124x124 eliminará recortes en las fronteras de los tiles. *Mitigación*: Como ahora descargamos los 3 tiles, muchas de esas zonas "de borde" en un tile estarán completas en el tile adyacente.
- **[Trade-off] Distorsión por Redimensionamiento** → Pasar de 124 a 128 píxeles implica una ligera interpolación. *Racional*: Es necesaria para la compatibilidad con la arquitectura del modelo EDSR que espera potencias de 2 o tamaños fijos.
