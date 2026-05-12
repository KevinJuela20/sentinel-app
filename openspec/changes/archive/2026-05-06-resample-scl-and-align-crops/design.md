## Context

El flujo actual de `processor.py` utiliza `rasterio.mask.mask` de forma independiente para cada banda. Esto provoca que, debido a las diferencias de resolución nativa (SCL a 20m vs RGB a 10m), los recortes resultantes puedan tener dimensiones inconsistentes o píxeles ligeramente desplazados. El usuario ha proporcionado un método de referencia que utiliza una banda de alta resolución (B04) como ancla para todas las extracciones.

## Goals / Non-Goals

**Goals:**
- Implementar la alineación de todos los recortes (B02, B03, B04, SCL) a una resolución común de 10 metros.
- Re-muestrear la capa SCL a 10m para que coincida exactamente con la cuadrícula de las bandas visibles.
- Mejorar la calidad visual de los recortes PNG aplicando un estiramiento (stretch) de contraste del 2% al 98%.
- Mantener el umbral de descarte de fragmentos incompletos a 63 píxeles (según ajuste manual del usuario).

**Non-Goals:**
- No se modificará el proceso de descarga (UC-04).
- No se implementarán máscaras de cambio (mencionadas por el usuario como no relevantes para este sistema).

## Decisions

### 1. Uso de B04 como Referencia de Ventana (Window)
**Decisión**: En `process_grid_cell`, primero abriremos B04 para obtener su `transform` y `crs`. Calcularemos la `Window` de rasterio a partir de los `bounds` de la celda proyectados al CRS de B04.
**Racional**: Garantiza que todas las bandas leídas para esa celda compartan exactamente la misma extensión geográfica y dimensiones de píxel.

### 2. Flujo de Validación de Nubes (SCL)
**Decisión**: 
1. Leer la banda SCL en su resolución nativa (20m) usando una máscara geométrica para el chequeo de nubes inicial.
2. Si la celda está limpia, se procede a la extracción de datos RGB.
**Racional**: Realizar el conteo de nubes a 20m es computacionalmente más barato y mantiene la precisión del sensor original antes de cualquier interpolación.

### 3. Re-muestreo Bilineal en Lectura
**Decisión**: Para bandas de resolución inferior a 10m (como SCL si se guardara, aunque aquí se usa principalmente para filtrar), utilizaremos `src.read(out_shape=(h, w), resampling=Resampling.bilinear)`.
**Racional**: Asegura que el dato interpolado coincida con la geometría de 10m.

### 4. Normalización de Imágenes (2% - 98% Stretch)
**Decisión**: Actualizar `save_rgb_png` en `src/image_utils.py` para aplicar una normalización basada en percentiles en lugar de un escalado lineal simple.
**Racional**: Mejora drásticamente la visibilidad de los recortes en condiciones de iluminación variadas.

## Risks / Trade-offs

- **[Riesgo] Desajuste de CRS** → Si las bandas de un mismo tile estuvieran en distintos CRS (poco probable en Sentinel-2 L2A). *Mitigación*: Siempre transformaremos la geometría al CRS de cada banda antes de la lectura.
- **[Trade-off] Memoria RAM** → El cálculo de percentiles requiere cargar el recorte completo en memoria. *Racional*: Dado que los recortes son pequeños (ej. 128x128), el impacto es despreciable.
