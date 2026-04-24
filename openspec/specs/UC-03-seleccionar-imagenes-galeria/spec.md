## Purpose

Marcar las imágenes que el usuario considera aptas para procesos posteriores de descarga y análisis. El analista revisa los metadatos y la previsualización visual para marcar una o más imágenes como "seleccionadas".

## Requirements

### Requirement: Galería de Selección con Metadatos (RF-03)
El sistema SHALL mostrar los resultados en una cuadrícula cronológica con el porcentaje de `eo:cloud_cover` y fecha exacta, permitiendo selección múltiple mediante checkboxes.

#### Scenario: Selección exitosa de múltiples imágenes
- **WHEN** el usuario revisa la galería con previsualizaciones y metadatos
- **AND** marca los checkboxes de las imágenes consideradas "limpias"
- **AND** presiona el botón de confirmación de selección
- **THEN** el sistema registra los IDs de items y enlaces de assets en la cola de descarga
- **AND** habilita las opciones de descarga

#### Scenario: Selección de imágenes de múltiples meses
- **WHEN** el usuario repite el proceso de selección para diferentes períodos temporales
- **THEN** el sistema acumula todas las imágenes seleccionadas en la misma cola de descarga

#### Scenario: Ninguna imagen seleccionada
- **WHEN** el usuario presiona confirmar sin haber seleccionado ninguna imagen
- **THEN** el sistema muestra un mensaje indicando que debe seleccionar al menos una imagen

## Acceptance Criteria
- Los resultados se muestran en cuadrícula cronológica
- Cada imagen muestra el porcentaje de nubosidad y la fecha
- El usuario puede seleccionar/deseleccionar imágenes con checkboxes
- El botón de confirmación habilita la descarga
- Se muestra un mensaje si no hay selección al confirmar

## Stories
- [ ] Story 1: Crear layout de cuadrícula cronológica para la galería
- [ ] Story 2: Mostrar metadatos (% nubosidad, fecha) debajo de cada imagen
- [ ] Story 3: Implementar checkboxes de selección múltiple
- [ ] Story 4: Implementar botón de confirmación y cola de descarga
- [ ] Story 5: Validar que al menos una imagen esté seleccionada antes de confirmar

## Technical Notes
- Components: Galería de Imágenes (Gal), UI Principal
- Dependencies: UC-02 (requiere galería con previsualizaciones)
- Streamlit widgets: `st.checkbox`, `st.columns`, `st.button`

## Traceability
| Source | Reference |
| ------ | --------- |
| SRS | RF-03 |
| Use Case | UC-03 |
| SDD | Galería + UI (sección 6) |
