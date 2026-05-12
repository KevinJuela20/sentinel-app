## Purpose

Permitir que el analista encuentre imágenes de Sentinel-2 que coincidan con un rango temporal y un área geográfica, consultando el catálogo de Microsoft Planetary Computer mediante la API STAC.
## Requirements
### Requirement: Búsqueda Temporal y Espacial de Imágenes (RF-01)
El sistema SHALL cargar automáticamente el AOI desde el archivo KML del proyecto (`external/ARH_MAP.kml`) al iniciar la sesión, sin requerir intervención del usuario. El sistema SHALL permitir ingresar dos fechas (mes y año) y realizar una consulta a la colección `sentinel-2-l2a` usando la intersección del AOI cargado automáticamente. Los resultados SHALL ser filtrados para excluir tiles MGRS que no estén en la lista de tiles permitidos (`ALLOWED_TILES`), devolviendo únicamente los items de los tiles MPS, MQT y MQS.

#### Scenario: Búsqueda exitosa con resultados
- **WHEN** el usuario ingresa un rango de fechas válido (mes/año inicio y fin) y la aplicación ha cargado el AOI automáticamente al inicio
- **THEN** el sistema construye la consulta STAC con filtros: colección `sentinel-2-l2a`, rango de fechas y geometría del AOI pre-cargado (`external/ARH_MAP.kml`)
- **AND** filtra los resultados para conservar solo los tiles MPS, MQT y MQS
- **AND** devuelve la lista filtrada de imágenes con sus metadatos (fecha, cobertura de nubes, assets)

#### Scenario: Búsqueda sin resultados
- **WHEN** el usuario ingresa un rango de fechas para el cual no existen imágenes disponibles
- **THEN** el sistema informa al usuario que no hay resultados
- **AND** solicita ajustar las fechas de búsqueda

#### Scenario: Error de conexión con MPC
- **WHEN** el sistema no puede comunicarse con la API STAC de MPC
- **THEN** el sistema muestra un mensaje de error descriptivo al usuario

#### Scenario: Resultados filtrados reducen la cantidad visible
- **WHEN** la API STAC devuelve N items que incluyen tiles MPT, MPS, MQT y MQS
- **THEN** el sistema devuelve aproximadamente 3/4 de los items (excluyendo MPT)
- **AND** la galería muestra únicamente imágenes de tiles relevantes para la zona de estudio

#### Scenario: AOI se carga automáticamente al iniciar la aplicación
- **WHEN** la aplicación Streamlit se inicia por primera vez en una sesión
- **THEN** el sistema carga el archivo KML desde la ruta del proyecto (`external/ARH_MAP.kml`) sin intervención del usuario
- **AND** almacena la geometría del AOI en el estado de sesión
- **AND** muestra un indicador discreto en la barra lateral confirmando la carga exitosa

#### Scenario: Error al cargar el KML automáticamente
- **WHEN** la aplicación intenta cargar el archivo KML al inicio y el archivo no existe o es inválido
- **THEN** el sistema muestra un mensaje de error visible en la barra lateral
- **AND** las búsquedas no pueden ejecutarse hasta que el AOI esté disponible

  - AND las búsquedas no pueden ejecutarse hasta que el AOI esté disponible

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
