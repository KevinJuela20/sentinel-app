## MODIFIED Requirements

### Requirement: Super-resolución con Modelos EDSR (RF-06)

#### Scenario: Dependencia de interfaz respecto a procesamiento de cuadrícula
- **WHEN** el usuario accede a la sección de Super-Resolución
- **AND** no se ha completado el procesamiento de cuadrícula (UC-05) para ninguna fecha seleccionada
- **THEN** el sistema SHALL ocultar el botón de "Aumento de Resolución"
- **AND** mostrar un mensaje informativo indicando que el procesamiento de cuadrícula es un requisito previo

#### Scenario: Habilitación de Super-Resolución
- **WHEN** el sistema detecta que al menos una fecha seleccionada ha completado exitosamente la fase de procesamiento de cuadrícula
- **OR** el sistema detecta físicamente la existencia de carpetas `crops/` con archivos PNG
- **THEN** el sistema SHALL mostrar y habilitar el botón de "Aumento de Resolución"
