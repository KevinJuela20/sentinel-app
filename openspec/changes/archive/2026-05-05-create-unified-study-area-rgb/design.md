## Context

Con la implementación de descargas multi-tile, el área de estudio se fragmenta en varios archivos GeoTIFF. Aunque el procesamiento por celdas funciona correctamente, los usuarios necesitan una vista consolidada de la zona para propósitos de control de calidad y visualización rápida sin tener que cargar múltiples archivos en un SIG.

## Goals / Non-Goals

**Goals:**
- Generar un único archivo GeoTIFF RGB de la zona de estudio completa por cada fecha descargada.
- Mantener la georreferenciación correcta en el mosaico resultante.
- Asegurar que la generación ocurra antes de que los archivos fuente sean eliminados.

**Non-Goals:**
- No se busca realizar correcciones de color complejas entre tiles (se confía en el pre-procesamiento de Sentinel-2 L2A).
- No se generarán mosaicos de bandas individuales (B02, B03, etc.) a menos que sea estrictamente necesario. Se prioriza el asset `visual`.

## Decisions

### 1. Uso de `rasterio.merge`
**Decisión**: Utilizar el módulo `merge` de `rasterio` para realizar la unión de los tiles.
**Racional**: Es la herramienta estándar en Python para mosaicos de rasters, maneja automáticamente la alineación de coordenadas y la creación del nuevo encabezado geoespacial.

### 2. Fuente: Asset `visual`
**Decisión**: El mosaico se construirá a partir de los archivos `*_visual.tif` de cada tile.
**Racional**: Estos archivos ya vienen listos en True Color RGB, lo que simplifica enormemente el proceso en comparación con unir bandas individuales y luego apilarlas.

### 3. Ubicación del Archivo Resultante
**Decisión**: Almacenar el archivo `Color_YYYY-MM-DD.tif` directamente en la raíz de la carpeta de la fecha (ej: `Data_Sentinel/2025/01/20/`).
**Racional**: Facilita la localización rápida por parte del usuario, separándolo de los recortes (`crops/`) y los resultados de súper-resolución (`super_res/`).

## Risks / Trade-offs

- **[Riesgo] Consumo de Memoria** → Unir tres tiles completos puede requerir mucha memoria RAM. *Mitigación*: Se procesarán solo los assets `visual` que suelen estar ya optimizados y, si es necesario, se utilizarán métodos de lectura por ventanas si se detectan problemas de escala.
- **[Trade-off] Tiempo de Procesamiento** → Añade un paso extra a la fase de fragmentación. *Racional*: El valor de tener una imagen unificada compensa el ligero retraso en la finalización del proceso.
