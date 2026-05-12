## MODIFIED Requirements

### Requirement: Procesamiento y Filtrado de Nubes (RF-05)

#### Scenario: Validación de nubes y alineación espacial a 10m
- **WHEN** se procesa una celda de la cuadrícula sobre un tile de Sentinel-2
- **THEN** el sistema SHALL validar la cobertura de nubes usando la banda SCL en su resolución nativa (20m)
- **AND** si la celda es válida, el sistema SHALL utilizar la banda B04 (10m) como referencia espacial para definir la ventana de recorte
- **AND** el sistema SHALL extraer las bandas B04, B03 y B02 (10m) asegurando una alineación de píxeles perfecta
- **AND** el sistema SHALL descartar cualquier recorte cuya dimensión resultante sea menor a 63 píxeles en cualquiera de sus ejes (evitando bordes incompletos)
- **AND** al guardar el resultado en PNG, el sistema SHALL aplicar un escalado de contraste (percentiles 2% al 98%) para normalizar la visualización

## Acceptance Criteria
- Todos los recortes RGB de una misma fecha/tile tienen dimensiones idénticas
- La validación de nubes se realiza antes de la extracción costosa de las bandas de 10m
- No se generan recortes con "bordes negros" significativos debido a tamaños insuficientes (<63px)
- Las imágenes PNG resultantes presentan un contraste mejorado y consistente
