## MODIFIED Requirements

### Requirement: Descarga Optimizada de Bandas Seleccionadas (RF-04)
El sistema SHALL descargar las bandas B02, B03, B04 y SCL para **cada uno de los tiles** asociados a las fechas seleccionadas. Antes de iniciar la descarga, el sistema SHALL validar si los archivos ya existen localmente para evitar duplicidad. Los archivos resultantes deben ser GeoTIFF con el CRS correcto y almacenarse en la misma carpeta de fecha, diferenciados por el ID del tile.

#### Scenario: Descarga eficiente de bandas espectrales
- **WHEN** el usuario inicia el proceso de descarga para una fecha seleccionada
- **AND** el sistema verifica que la carpeta `Data_Sentinel/[Año]/[Mes]/[Día]` NO contiene los archivos `.tif` correspondientes a las bandas requeridas
- **THEN** el sistema SHALL identificar todos los items (tiles) asociados a esa fecha en la cola de descarga
- **AND** para cada item, firma únicamente los assets esenciales: B02, B03, B04 y SCL
- **AND** EXCLUYE explícitamente el asset `visual` de la lista de descarga para evitar redundancia
- **AND** descarga el archivo `.tif` original completo sin aplicar ningún recorte (no-cropping) ni máscara espacial
- **AND** guarda los archivos resultantes preservando las dimensiones originales del tile de Sentinel-2
- **AND** crea la estructura de carpetas `Data_Sentinel/[Año]/[Mes]/[Día]`
- **AND** guarda los archivos con la fecha de adquisición, el ID del tile y el nombre de la banda (ej: `20250101_MPS_B02.tif`)

#### Scenario: Omisión de descarga por datos existentes
- **WHEN** el usuario inicia el proceso de descarga para una fecha seleccionada
- **AND** el sistema verifica que la carpeta `Data_Sentinel/[Año]/[Mes]/[Día]` YA contiene los archivos `.tif` correspondientes a las bandas requeridas para todos los tiles seleccionados
- **THEN** el sistema SHALL omitir la descarga para esa fecha específica
- **AND** SHALL informar al usuario que los datos ya se encuentran disponibles localmente
