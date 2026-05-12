## Purpose

Evaluar visualmente la calidad de la imagen y la cobertura de nubes dentro del área de estudio específica. Por cada imagen encontrada en la búsqueda, el sistema solicita un tile renderizado al MPC Tiler y le aplica una máscara de transparencia basada en el área de estudio del usuario.
## Requirements
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

#### Scenario: Visualización integral multi-tile por fecha
- **WHEN** se presentan los resultados agrupados por fecha
- **THEN** el sistema SHALL renderizar los tres tiles individuales (MPS, MQT, MQS) asociados a esa fecha en una disposición horizontal
- **AND** cada thumbnail de tile SHALL aplicar su propia máscara de transparencia y contorno del AOI
- **AND** cada tile SHALL mostrar su ID de tile y su porcentaje de cobertura de nubes individual para facilitar la validación selectiva del usuario

#### Scenario: Carga paralela de múltiples tiles
- **WHEN** se inicia la pre-carga de imágenes para una fecha
- **THEN** el sistema SHALL incluir los tres tiles en la cola de procesamiento concurrente
- **AND** asegurar que el cacheo de imágenes funcione de forma única por cada `item_id` (tile) para evitar colisiones

## Acceptance Criteria
- Las imágenes se previsualizan con la máscara del AOI aplicada
- Las zonas fuera del área de estudio se muestran transparentes
- Los thumbnails se cargan asíncronamente sin bloquear la interfaz
- Se muestra un placeholder si el Tiler no está disponible

## Stories
- [ ] Story 1: Implementar solicitud de tiles True Color al MPC Tiler
- [ ] Story 2: Aplicar máscara de transparencia basada en geometría del AOI
- [ ] Story 3: Renderizar thumbnails en la interfaz de la galería
- [ ] Story 4: Implementar carga asíncrona de previsualizaciones
- [ ] Story 5: Manejar caso de Tiler no disponible con placeholder

## Technical Notes
- Components: UI Principal + MPC Tiler, Galería de Imágenes
- Dependencies: UC-01 (requiere resultados de búsqueda)
- Librerías: `leafmap`, `rasterio` para masking

## Traceability
| Source | Reference |
| ------ | --------- |
| SRS | RF-02 |
| Use Case | UC-02 |
| SDD | UI Principal + Tiler (sección 6) |
