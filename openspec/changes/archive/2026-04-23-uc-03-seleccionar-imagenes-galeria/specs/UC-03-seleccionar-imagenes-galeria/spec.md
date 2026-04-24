## MODIFIED Requirements

### Requirement: Galería de Selección con Metadatos (RF-03)
El sistema SHALL mostrar los resultados en una cuadrícula cronológica con el porcentaje de `eo:cloud_cover` y fecha exacta, permitiendo selección múltiple mediante checkboxes que persisten a través de múltiples búsquedas en la misma sesión.

#### Scenario: Selección exitosa de múltiples imágenes
- **WHEN** el usuario revisa la galería con previsualizaciones y metadatos
- **AND** marca los checkboxes de las imágenes consideradas "limpias"
- **AND** presiona el botón de confirmación de selección
- **THEN** el sistema registra los IDs de items y enlaces de assets en la cola de descarga
- **AND** habilita las opciones de descarga

#### Scenario: Selección de imágenes de múltiples meses
- **WHEN** el usuario realiza una búsqueda para un mes, selecciona imágenes, y luego realiza otra búsqueda para un mes diferente
- **THEN** las imágenes seleccionadas previamente se mantienen en la cola de descarga
- **AND** si el usuario vuelve al mes anterior, las imágenes ya seleccionadas aparecen marcadas en la interfaz

#### Scenario: Ninguna imagen seleccionada
- **WHEN** el usuario presiona confirmar sin haber seleccionado ninguna imagen en la sesión actual
- **THEN** el sistema muestra un mensaje indicando que debe seleccionar al menos una imagen
