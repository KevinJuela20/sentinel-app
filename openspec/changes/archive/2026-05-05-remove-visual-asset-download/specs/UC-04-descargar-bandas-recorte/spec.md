## MODIFIED Requirements

### Requirement: Descarga Optimizada de Bandas Seleccionadas (RF-04)

#### Scenario: Descarga eficiente de bandas espectrales
- **WHEN** el usuario inicia el proceso de descarga para una fecha seleccionada
- **THEN** el sistema SHALL identificar todos los items (tiles) asociados a esa fecha en la cola de descarga
- **AND** para cada item, firma únicamente los assets esenciales: B02, B03, B04 y SCL
- **AND** EXCLUYE explícitamente el asset `visual` de la lista de descarga para evitar redundancia
- **AND** guarda los archivos resultantes siguiendo la estructura jerárquica establecida

## Acceptance Criteria
- Las bandas B02, B03, B04 y SCL se descargan correctamente
- El asset `visual` ya no aparece en la carpeta de descarga ni en el log de archivos guardados
- El sistema es capaz de completar la descarga de una fecha sin errores por falta del asset `visual`
