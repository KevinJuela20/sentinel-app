## Purpose

Marcar las imágenes que el usuario considera aptas para procesos posteriores de descarga y análisis. El analista revisa los metadatos y la previsualización visual para marcar una o más imágenes como "seleccionadas".
## Requirements
### Requirement: Galería de Selección con Metadatos (RF-03)
El sistema SHALL mostrar los resultados agrupados por **Fecha de Adquisición**. Cada entrada en la galería representará un día único. El sistema SHALL permitir la selección de una fecha completa mediante un único checkbox. Al seleccionar una fecha, el sistema SHALL incluir automáticamente todos los tiles disponibles para ese día (MPS, MQT, MQS) en la cola de descarga. **Para garantizar la estabilidad de la interfaz y la integridad de los datos procesados, el sistema SHALL mostrar únicamente las fechas que cuenten con exactamente 3 tiles.**

#### Scenario: Selección exitosa de una fecha completa
- **WHEN** el usuario revisa la galería con previsualizaciones agrupadas por fecha
- **AND** el sistema filtra y muestra solo las fechas con exactamente 3 tiles
- **AND** marca el checkbox de una fecha específica
- **AND** presiona el botón de confirmación de selección
- **THEN** el sistema registra todos los items STAC (exactamente 3 tiles) correspondientes a esa fecha en la cola de descarga
- **AND** habilita las opciones de descarga

#### Scenario: Omisión de fechas incompletas o excedentes
- **WHEN** el resultado de la búsqueda STAC devuelve una fecha con menos de 3 tiles o más de 3 tiles
- **THEN** el sistema SHALL omitir dicha fecha de la galería de visualización
- **AND** NO permitirá su selección para procesos posteriores

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
