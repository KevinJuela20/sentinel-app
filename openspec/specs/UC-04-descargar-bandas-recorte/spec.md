## Purpose

Obtener los archivos de datos (bandas y TIF) guardándolos localmente con nombres estandarizados y recortes precisos. El sistema firma las URLs de descarga, recorta el ráster a la cuadrícula GeoJSON y guarda los archivos en carpetas organizadas jerárquicamente.
## Requirements
### Requirement: Descarga Optimizada de Bandas Seleccionadas (RF-04)
El sistema SHALL descargar las bandas B02, B03, B04 y SCL para **cada uno de los tiles** asociados a las fechas seleccionadas. Antes de iniciar la descarga, el sistema SHALL validar si los archivos ya existen localmente para evitar duplicidad. Los archivos resultantes deben ser GeoTIFF con el CRS correcto y almacenarse en la misma carpeta de fecha, diferenciados por el ID del tile.

#### Scenario: Descarga eficiente de bandas espectrales
- **WHEN** el usuario inicia el proceso de descarga para una fecha seleccionada
- **AND** el sistema verifica que la carpeta `~/Documents/Data_Sentinel/[Año]/[Mes]/[Día]` NO contiene los archivos `.tif` correspondientes a las bandas requeridas
- **THEN** el sistema SHALL identificar todos los items (tiles) asociados a esa fecha en la cola de descarga
- **AND** para cada item, firma únicamente los assets esenciales: B02, B03, B04 y SCL
- **AND** EXCLUYE explícitamente el asset `visual` de la lista de descarga para evitar redundancia
- **AND** descarga el archivo `.tif` original completo sin aplicar ningún recorte (no-cropping) ni máscara espacial
- **AND** guarda los archivos resultantes preservando las dimensiones originales del tile de Sentinel-2
- **AND** crea la estructura de carpetas `~/Documents/Data_Sentinel/[Año]/[Mes]/[Día]`
- **AND** guarda los archivos con la fecha de adquisición, el ID del tile y el nombre de la banda (ej: `20250101_MPS_B02.tif`)

#### Scenario: Omisión de descarga por datos existentes
- **WHEN** el usuario inicia el proceso de descarga para una fecha seleccionada
- **AND** el sistema verifica que la carpeta `~/Documents/Data_Sentinel/[Año]/[Mes]/[Día]` YA contiene los archivos `.tif` correspondientes a las bandas requeridas para todos los tiles seleccionados
- **THEN** el sistema SHALL omitir la descarga para esa fecha específica
- **AND** SHALL informar al usuario que los datos ya se encuentran disponibles localmente

### Requirement: Estructura de Almacenamiento Jerárquica (RF-07)
El sistema SHALL organizar las descargas en la estructura `~/Documents/Data_Sentinel/[Año]/[Mes]/[Día]/` garantizando que los nombres de carpetas tengan ceros a la izquierda para meses y días (ej: `01` para Enero).

#### Scenario: Creación automática de estructura de carpetas
- **WHEN** se guardan archivos para una fecha nueva
- **THEN** el sistema crea automáticamente la jerarquía `~/Documents/Data_Sentinel/[Año]/[Mes]/[Día]/` en el directorio de documentos del usuario
- **AND** almacena los archivos completos en dicha carpeta

## Acceptance Criteria
- Las bandas B02, B03, B04 y SCL se descargan en su totalidad (100km x 100km)
- El asset `visual` ya no aparece en la carpeta de descarga ni en el log de archivos guardados
- Se elimina el paso de recorte (cropping) durante la fase de descarga física
- Los archivos resultantes mantienen la resolución y cobertura original del tile STAC
- La estructura de carpetas sigue el patrón `[Año]/[Mes]/[Día]`
- El usuario recibe notificación al completar la descarga
- Se gestionan errores de descarga sin detener el proceso completo

## Stories
- [ ] Story 1: Implementar firma de URLs con `planetary_computer.sign` para los assets
- [ ] Story 2: Descargar bandas B02, B03, B04 y SCL completas (full tile) excluyendo visual
- [ ] Story 3: Implementar descarga directa por bloques (stream download) con `requests`
- [ ] Story 4: Crear la estructura de carpetas jerárquica `Data_Sentinel/[Año]/[Mes]/[Día]`
- [ ] Story 5: Nombrar archivos con fecha de adquisición
- [ ] Story 6: Implementar barra de progreso y notificación de finalización
- [ ] Story 7: Manejar errores de descarga con reintentos

## Technical Notes
- Components: Motor de Procesamiento, Gestor del Sistema de Archivos
- Dependencies: UC-03 (requiere selección confirmada)
- Archivo requerido: `Cuadrícula_ARH.geojson`
- Rutas de almacenamiento: `/Desktop/Download Data`, `/Desktop/Data_Sentinel`
- Librerías: `rasterio`, `geopandas`, `planetary-computer`

## Traceability
| Source | Reference |
| ------ | --------- |
| SRS | RF-04, RF-07 |
| Use Case | UC-04 |
| SDD | Motor de Procesamiento + Gestor FileSys (secciones 3.2, 5.1) |
