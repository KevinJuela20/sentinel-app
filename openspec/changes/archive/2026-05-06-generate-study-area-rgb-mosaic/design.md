## Context

El usuario desea un producto visual de alta resolución que cubra toda el área de estudio definida por un archivo KML (`ARH_ETAPA.kml`). Actualmente el sistema solo genera recortes individuales (crops) y ha desactivado el mosaico visual previo. Esta nueva funcionalidad consolidará los tres tiles descargados en un único archivo RGB georreferenciado recortado por el AOI principal.

## Goals / Non-Goals

**Goals:**
- Generar un mosaico RGB (`.tif`) consolidado de los tres tiles por cada fecha.
- Recortar el mosaico utilizando el polígono de `ARH_ETAPA.kml`.
- Asegurar que el mosaico esté correctamente georreferenciado y alineado.
- Eliminar las bandas originales solo tras el éxito de la generación de recortes y el mosaico.

**Non-Goals:**
- No se generará el mosaico para bandas individuales (SCL, etc.), solo para el producto visual RGB.

## Decisions

### 1. Soporte de Lectura KML
**Decisión**: Habilitar el driver KML en `fiona` dinámicamente mediante `fiona.drvsupport.supported_drivers['KML'] = 'rw'` dentro de una nueva utilidad en `src/geo_utils.py`.
**Racional**: Permite utilizar la potencia de `geopandas` para manejar la geometría del KML sin añadir dependencias externas pesadas.

### 2. Procesamiento de Mosaico RGB
**Decisión**: 
- Para cada tile, se abrirán las bandas B04, B03 y B02.
- Se creará una pila (stack) RGB en memoria.
- Se aplicará `rasterio.mask.mask` usando la geometría del KML transformada al CRS del tile.
- Los resultados parciales se combinarán usando `rasterio.merge`.
**Racional**: Garantiza que el mosaico final solo contenga datos dentro del área de estudio, optimizando el tamaño del archivo resultante.

### 3. Secuencia de Limpieza (Cleanup)
**Decisión**: Mover la lógica de eliminación de archivos al final de `process_all_grids`, condicionada a que tanto el contador de `saved` crops sea mayor a 0 como la existencia del archivo de mosaico generado.
**Racional**: Previene la pérdida de datos crudos si alguna fase del procesamiento falla.

## Risks / Trade-offs

- **[Riesgo] Memoria RAM** → Procesar tres tiles completos de 10m en RGB puede consumir mucha memoria. *Mitigación*: Se utilizará el recorte por KML lo antes posible en el flujo para reducir el tamaño de los arrays en memoria antes del merge.
- **[Trade-off] Tiempo de Procesamiento** → Añade una fase extra de I/O y cómputo. *Racional*: Es necesario para cumplir con el requisito de "producto final unificado".

## Sequence Diagram

1. `process_all_grids` inicia.
2. Genera los `crops` de la cuadrícula.
3. Carga `ARH_ETAPA.kml`.
4. Para cada Tile:
   - Lee B04, B03, B02.
   - Aplica máscara KML.
   - Almacena raster temporal.
5. Ejecuta `merge` de rasters temporales.
6. Guarda `Color_YYYY-MM-DD.tif`.
7. Si éxito, elimina archivos `.tif` originales.
