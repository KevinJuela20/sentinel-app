## ADDED Purpose

Proporcionar una capa visual vectorial sobre las previsualizaciones de imágenes para facilitar la contextualización geográfica del Área de Interés (AOI) dentro de los tiles de Sentinel-2.

## ADDED Requirements

### Requirement: Superposición Vectorial del AOI (RF-OVERLAY-01)
El sistema SHALL dibujar el contorno del AOI sobre las imágenes de previsualización procesadas.

#### Scenario: Dibujo exitoso del contorno
- **GIVEN** una imagen recortada por el AOI y su correspondiente transformación afín
- **WHEN** el sistema procesa la imagen para la galería
- **THEN** extrae las coordenadas de los límites del AOI
- **AND** proyecta dichas coordenadas al espacio de píxeles de la imagen
- **AND** dibuja una línea roja continua de 2px de grosor siguiendo el contorno del AOI
- **AND** la imagen resultante conserva la transparencia original del fondo

#### Scenario: AOI con múltiples anillos o huecos
- **GIVEN** un AOI de tipo MultiPolygon o con agujeros (interiors)
- **WHEN** se genera la superposición
- **THEN** el sistema dibuja el contorno de cada parte y cada agujero de forma independiente para asegurar la representación fiel del área de estudio.

## Acceptance Criteria
- El contorno rojo coincide exactamente con los bordes de la imagen recortada (donde termina la imagen y empieza la transparencia).
- La línea es claramente visible sobre fondos oscuros y claros.
- No hay desplazamiento (offset) entre la imagen satelital y el vector superpuesto.
