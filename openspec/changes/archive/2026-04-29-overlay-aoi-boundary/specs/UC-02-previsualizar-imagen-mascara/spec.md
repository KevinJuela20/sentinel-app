## MODIFIED Requirements

### Requirement: Previsualización Dinámica con Recorte (RF-02)
El sistema SHALL mostrar un thumbnail de baja resolución renderizado vía el MPC Tiler, aplicando una máscara de transparencia a las zonas fuera del área de estudio y superponiendo el contorno del AOI en color rojo.

#### Scenario: Previsualización exitosa con contorno de AOI
- **WHEN** el usuario visualiza la galería de resultados tras una búsqueda exitosa (UC-01)
- **THEN** el sistema solicita al MPC Tiler una visualización True Color para cada item STAC
- **AND** aplica un recorte dinámico (masking) usando la geometría del AOI para hacer transparente lo exterior
- **AND** dibuja el contorno rojo del AOI sobre la imagen recortada para delimitar la zona de estudio (RF-OVERLAY-01)
- **AND** renderiza el thumbnail resultante en la interfaz

## Acceptance Criteria
- Las imágenes muestran el contorno rojo del área de estudio.
- El contorno es de 2px de grosor y color #FF0000.
