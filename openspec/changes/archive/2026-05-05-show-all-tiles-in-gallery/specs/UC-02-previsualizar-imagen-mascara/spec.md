## MODIFIED Requirements

### Requirement: Previsualización Dinámica con Recorte (RF-02)

#### Scenario: Visualización integral multi-tile por fecha
- **WHEN** se presentan los resultados agrupados por fecha
- **THEN** el sistema SHALL renderizar los tres tiles individuales (MPS, MQT, MQS) asociados a esa fecha en una disposición horizontal
- **AND** cada thumbnail de tile SHALL aplicar su propia máscara de transparencia y contorno del AOI
- **AND** cada tile SHALL mostrar su ID de tile y su porcentaje de cobertura de nubes individual para facilitar la validación selectiva del usuario

#### Scenario: Carga paralela de múltiples tiles
- **WHEN** se inicia la pre-carga de imágenes para una fecha
- **THEN** el sistema SHALL incluir los tres tiles en la cola de procesamiento concurrente
- **AND** asegurar que el cacheo de imágenes funcione de forma única por cada `item_id` (tile) para evitar colisiones
