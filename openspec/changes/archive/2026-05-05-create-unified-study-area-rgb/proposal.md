## Why

Actualmente, el sistema descarga y procesa múltiples tiles de Sentinel-2 de forma independiente. Para facilitar el análisis visual y la validación cartográfica de la zona de estudio completa, es necesario generar una imagen RGB unificada (mosaico) que combine los tres tiles descargados antes de que los archivos fuente sean eliminados.

## What Changes

- **Generación de Mosaico RGB**: Nueva funcionalidad para unir los componentes visuales de los tres tiles descargados para una fecha específica en un único archivo GeoTIFF.
- **Nomenclatura**: El archivo unificado se guardará como `Color_YYYY-MM-DD.tif` en el directorio de la fecha correspondiente.
- **Flujo de Procesamiento**: La unión de imágenes se ejecutará automáticamente durante la fase de fragmentación, justo antes de la limpieza de archivos temporales.

## Capabilities

### New Capabilities
- None

### Modified Capabilities
- `UC-05-procesar-recortes-filtrar-nubes`: Se añade un nuevo requisito funcional para generar el mosaico RGB de la zona de estudio completa antes de la eliminación de los archivos `.tif` fuente.

## Impact

- **src/processor.py**: Se añade la llamada a la función de mosaico en `process_all_grids`.
- **src/image_utils.py**: Se implementa la lógica de unión (merge) de rasters usando `rasterio.merge`.
- **sentinel-project/Data_Sentinel/**: Aparecerán nuevos archivos `Color_*.tif` en los directorios de descarga.
