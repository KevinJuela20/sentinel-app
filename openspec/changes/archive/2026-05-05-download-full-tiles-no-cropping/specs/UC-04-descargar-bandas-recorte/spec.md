## MODIFIED Requirements

### Requirement: Descarga Optimizada de Bandas Seleccionadas (RF-04)

#### Scenario: Descarga íntegra de los tres tiles por fecha
- **WHEN** el usuario inicia el proceso de descarga para una fecha seleccionada
- **THEN** el sistema SHALL identificar todos los items (tiles) asociados a esa fecha en la cola de descarga
- **AND** para cada item, firma las URLs de los assets: B02, B03, B04, SCL y Visual mediante `planetary_computer.sign`
- **AND** descarga el archivo `.tif` original completo sin aplicar ningún recorte (no-cropping) ni máscara espacial
- **AND** guarda los archivos resultantes preservando las dimensiones originales del tile de Sentinel-2
- **AND** crea la estructura de carpetas `Data_Sentinel/[Año]/[Mes]/[Día]`
- **AND** guarda los archivos con la fecha de adquisición, el ID del tile y el nombre de la banda (ej: `20250101_MPS_B02.tif`)

## Acceptance Criteria
- Las bandas B02, B03, B04, SCL y Visual se descargan en su totalidad (100km x 100km)
- Se elimina el paso de recorte (cropping) durante la fase de descarga física
- Los archivos resultantes mantienen la resolución y cobertura original del tile STAC
