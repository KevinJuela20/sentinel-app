## MODIFIED Requirements

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
