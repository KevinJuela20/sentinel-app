## MODIFIED Requirements

### Requirement: Ruta de salida de descargas
El sistema SHALL utilizar `~/Documents/Data_Sentinel` como directorio raíz para almacenar las bandas descargadas, en lugar del directorio relativo al proyecto. La estructura interna de subdirectorios (`YYYY/MM/DD/`) y la convención de nombres de archivo (`YYYYMMDD_TILE_BAND.tif`) MUST permanecer sin cambios.

#### Scenario: Descarga de bandas a nueva ruta
- **WHEN** el usuario selecciona fechas e imágenes y ejecuta la descarga
- **THEN** los archivos GeoTIFF se guardan en `~/Documents/Data_Sentinel/YYYY/MM/DD/` con el mismo esquema de nombres actual

#### Scenario: Verificación de datos existentes en nueva ruta
- **WHEN** el sistema verifica si los datos de una fecha ya fueron descargados (`check_date_data_exists`)
- **THEN** la verificación se realiza contra `~/Documents/Data_Sentinel/YYYY/MM/DD/` y no contra la ruta antigua dentro del proyecto

#### Scenario: Mensaje de confirmación muestra nueva ruta
- **WHEN** la descarga finaliza exitosamente
- **THEN** el mensaje `📂 Archivos guardados en:` muestra la ruta absoluta bajo `~/Documents/Data_Sentinel/`
