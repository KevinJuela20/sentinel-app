## MODIFIED Requirements

### Requirement: Descarga Optimizada de Bandas Seleccionadas (RF-04)
El sistema SHALL descargar las bandas B02, B03, B04 y SCL, además del producto True Color (.tif), realizando un recorte (clip) a los polígonos del archivo `Cuadrícula_ARH.geojson` antes de guardar en disco. Los archivos resultantes deben ser GeoTIFF con el CRS correcto.

#### Scenario: Descarga exitosa con recorte
- **WHEN** el usuario inicia el proceso de descarga tras confirmar la selección (UC-03)
- **THEN** el sistema firma las URLs para los assets: B02, B03, B04, SCL y Visual mediante `planetary_computer.sign`
- **AND** descarga las bandas y realiza el recorte (clip) usando los límites de `Cuadrícula_ARH.geojson`
- **AND** crea la estructura de carpetas `Data_Sentinel/[Año]/[Mes]/[Día]`
- **AND** guarda los archivos resultantes con la fecha de adquisición y el nombre de la banda (ej: `20250101_B02.tif`)
- **AND** notifica al usuario que la descarga ha finalizado mediante una barra de progreso al 100%

### Requirement: Estructura de Almacenamiento Jerárquica (RF-07)
El sistema SHALL organizar las descargas en la estructura `Data_Sentinel/[Año]/[Mes]/[Día]/` garantizando que los nombres de carpetas tengan ceros a la izquierda para meses y días (ej: `01` para Enero).

#### Scenario: Creación automática de estructura de carpetas
- **WHEN** se guardan archivos para una fecha nueva
- **THEN** el sistema crea automáticamente la jerarquía `Data_Sentinel/[Año]/[Mes]/[Día]/` en el directorio raíz del proyecto o ruta configurada
- **AND** almacena los archivos recortados en dicha carpeta
