## MODIFIED Requirements

### Requirement: Galería de Selección con Metadatos (RF-03)
El sistema SHALL mostrar los resultados agrupados por **Fecha de Adquisición**. Cada entrada en la galería representará un día único. El sistema SHALL permitir la selección de una fecha completa mediante un único checkbox. Al seleccionar una fecha, el sistema SHALL incluir automáticamente todos los tiles disponibles para ese día (MPS, MQT, MQS) en la cola de descarga.

#### Scenario: Selección exitosa de una fecha completa
- **WHEN** el usuario revisa la galería con previsualizaciones agrupadas por fecha
- **AND** marca el checkbox de una fecha específica
- **AND** presiona el botón de confirmación de selección
- **THEN** el sistema registra todos los items STAC (hasta 3 tiles) correspondientes a esa fecha en la cola de descarga
- **AND** habilita las opciones de descarga

#### Scenario: Visualización de nubosidad por fecha
- **WHEN** el sistema agrupa los tiles por fecha
- **THEN** muestra el promedio de `eo:cloud_cover` de los tiles disponibles para ese día (o el valor máximo) para informar al usuario sobre la calidad general de la fecha
