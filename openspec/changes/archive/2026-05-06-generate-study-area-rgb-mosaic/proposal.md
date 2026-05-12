## Why

Para facilitar la validación visual del área de estudio completa y consolidar la información descargada antes de su eliminación, se requiere un producto unificado (mosaico) en color verdadero (RGB) que cubra exactamente la extensión definida por el proyecto (`ARH_ETAPA.kml`).

## What Changes

- **Generación de Mosaico RGB Consolidado**: Implementación de un flujo que combina las bandas B04, B03 y B02 de los tres tiles (MPS, MQT, MQS) en un solo archivo georreferenciado.
- **Recorte por AOI (KML)**: Aplicación del archivo `ARH_ETAPA.kml` para recortar el área de estudio exacta de cada tile antes de la unión.
- **Limpieza de Datos Cruda**: Los archivos `.tif` originales por banda serán eliminados solo después de haber generado exitosamente tanto los recortes de la cuadrícula (crops) como el mosaico RGB consolidado.
- **Ubicación de Salida**: El mosaico final se guardará en la carpeta de la fecha correspondiente (ej. `Data_Sentinel/2025/01/01/Color_2025-01-01.tif`).

## Capabilities

### New Capabilities
- None

### Modified Capabilities
- `UC-05-procesar-recortes-filtrar-nubes`: Se expande la responsabilidad del procesador para incluir la creación del mosaico RGB del área de estudio antes de la limpieza de archivos.

## Impact

- **src/processor.py**: Modificación de `process_all_grids` para integrar el flujo de mosaico RGB basado en KML.
- **src/geo_utils.py**: Posible necesidad de utilidades para leer archivos KML (usando `fiona` o `geopandas`).
- **Almacenamiento**: Mejora en la gestión de espacio al eliminar bandas individuales tras consolidar el área de interés.
