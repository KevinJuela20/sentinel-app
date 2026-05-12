## MODIFIED Requirements

### Requirement: Previsualización Dinámica con Recorte (RF-02)
El sistema SHALL mostrar un thumbnail de baja resolución con alto contraste, aplicando una máscara de transparencia y superponiendo el contorno completo del AOI en color rojo vibrante.

#### Scenario: Previsualización de alta visibilidad
- **WHEN** el usuario visualiza los resultados de búsqueda
- **THEN** el sistema aplica un realce de contraste (contrast enhancement) a la imagen satelital para resaltar vegetación y nubes
- **AND** renderiza el contorno del AOI de forma nítida y perfectamente alineada
- **AND** asegura que el fondo sea oscuro/transparente para resaltar el contorno rojo fuera del tile.
