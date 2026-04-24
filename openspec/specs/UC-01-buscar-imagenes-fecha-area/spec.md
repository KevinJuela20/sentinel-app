## Purpose

Permitir que el analista encuentre imágenes de Sentinel-2 que coincidan con un rango temporal y un área geográfica, consultando el catálogo de Microsoft Planetary Computer mediante la API STAC.

## Requirements

### Requirement: Búsqueda Temporal y Espacial de Imágenes (RF-01)
El sistema SHALL permitir ingresar dos fechas (mes y año) y realizar una consulta a la colección `sentinel-2-l2a` usando la intersección del AOI definido por el archivo KML provisto.

#### Scenario: Búsqueda exitosa con resultados
- **WHEN** el usuario ingresa un rango de fechas válido (mes/año inicio y fin) y el archivo KML está cargado
- **THEN** el sistema extrae las coordenadas del AOI desde el KML
- **AND** construye la consulta STAC con filtros: colección `sentinel-2-l2a`, rango de fechas y geometría
- **AND** devuelve la lista de imágenes con sus metadatos (fecha, cobertura de nubes, assets)

#### Scenario: Búsqueda sin resultados
- **WHEN** el usuario ingresa un rango de fechas para el cual no existen imágenes disponibles
- **THEN** el sistema informa al usuario que no hay resultados
- **AND** solicita ajustar las fechas de búsqueda

#### Scenario: Error de conexión con MPC
- **WHEN** el sistema no puede comunicarse con la API STAC de MPC
- **THEN** el sistema muestra un mensaje de error descriptivo al usuario

## Acceptance Criteria
- El usuario puede ingresar fechas de inicio y fin en la barra lateral
- El sistema extrae correctamente las coordenadas del archivo KML
- La consulta STAC devuelve metadatos válidos de imágenes Sentinel-2 L2A
- Se muestra un mensaje apropiado cuando no hay resultados
- Se muestra un mensaje de error cuando falla la conexión

## Stories
- [ ] Story 1: Crear interfaz de barra lateral para ingreso de fechas (mes/año inicio y fin)
- [ ] Story 2: Implementar la carga y parseo del archivo KML para extraer geometría AOI
- [ ] Story 3: Implementar el Controlador de Búsqueda con `pystac_client` para consultas STAC
- [ ] Story 4: Procesar y preparar los metadatos de los items STAC encontrados
- [ ] Story 5: Manejar errores (sin resultados, fallo de conexión)

## Technical Notes
- Components: Controlador de Búsqueda (Search Controller), UI Barra Lateral
- Dependencies: Ninguna (caso de uso base)
- Algoritmo: `search_images(mes_inicio, año_inicio, mes_fin, año_fin, geom_aoi)` usando `pystac_client.search()`
- Librerías: `pystac-client`, `planetary-computer`, `geopandas`

## Traceability
| Source | Reference |
| ------ | --------- |
| SRS | RF-01 |
| Use Case | UC-01 |
| SDD | Controlador de Búsqueda (sección 5.1) |
