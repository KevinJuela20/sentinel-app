## Purpose

Evaluar visualmente la calidad de la imagen y la cobertura de nubes dentro del área de estudio específica. Por cada imagen encontrada en la búsqueda, el sistema solicita un tile renderizado al MPC Tiler y le aplica una máscara de transparencia basada en el área de estudio del usuario.

## Requirements

### Requirement: Previsualización Dinámica con Recorte (RF-02)
El sistema SHALL mostrar un thumbnail de baja resolución renderizado vía el MPC Tiler, aplicando una máscara de transparencia a las zonas fuera del área de estudio.

#### Scenario: Previsualización exitosa de una imagen
- **WHEN** el usuario visualiza la galería de resultados tras una búsqueda exitosa (UC-01)
- **THEN** el sistema solicita al MPC Tiler una visualización True Color para cada item STAC
- **AND** aplica un recorte dinámico (masking) usando la geometría del AOI para hacer transparente lo exterior
- **AND** renderiza el mini-mapa o thumbnail en la interfaz

#### Scenario: Servicio MPC Tiler no disponible
- **WHEN** el servicio MPC Tiler está caído o inaccesible
- **THEN** el sistema muestra un placeholder indicando que la previa no está disponible
- **AND** permite al usuario continuar con la selección basándose en metadatos

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
