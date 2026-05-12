## MODIFIED Requirements

### Requirement: Previsualización Dinámica con Recorte (RF-02)
El sistema SHALL mostrar un thumbnail de baja resolución con alto contraste, aplicando una máscara de transparencia y superponiendo el contorno completo del AOI en color rojo vibrante. Además, el sistema SHALL descargar y procesar estos thumbnails de forma concurrente para evitar el bloqueo prolongado de la interfaz.

#### Scenario: Previsualización de alta visibilidad
- **WHEN** el usuario visualiza los resultados de búsqueda
- **THEN** el sistema aplica un realce de contraste (contrast enhancement) a la imagen satelital para resaltar vegetación y nubes
- **AND** renderiza el contorno del AOI de forma nítida y perfectamente alineada
- **AND** asegura que el fondo sea oscuro/transparente para resaltar el contorno rojo fuera del tile.

#### Scenario: Carga paralela de previsualizaciones
- **WHEN** la búsqueda retorna múltiples resultados (items STAC)
- **THEN** el sistema inicia un proceso de carga concurrente (ej. ThreadPool) para obtener las imágenes y aplicar las máscaras
- **AND** muestra un indicador visual (spinner) mientras se realiza este proceso I/O-bound
- **AND** al finalizar el proceso concurrente, renderiza la galería de resultados completa de forma casi instantánea usando los datos en caché.
