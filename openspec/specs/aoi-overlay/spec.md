# aoi-overlay Specification

## Purpose
TBD - created by archiving change overlay-aoi-boundary. Update Purpose after archive.
## Requirements
### Requirement: Superposición Vectorial del AOI (RF-OVERLAY-01)
El sistema SHALL dibujar el contorno **completo** del AOI sobre las imágenes de previsualización, independientemente de si el tile cubre la totalidad del área.

#### Scenario: Cobertura parcial del AOI por el Tile
- **GIVEN** un AOI cuya extensión es mayor a la del Tile renderizado (ej. Tile MQT)
- **WHEN** el sistema genera la previsualización para la galería
- **THEN** crea un lienzo (canvas) que abarca el bounding box total del AOI
- **AND** posiciona el tile en su ubicación geográfica correcta dentro de ese lienzo
- **AND** dibuja el contorno rojo vibrante (#FF0000) de 2px en el perímetro total del AOI
- **AND** las áreas del contorno no cubiertas por el tile permanecen visibles sobre el fondo oscuro de la aplicación.

