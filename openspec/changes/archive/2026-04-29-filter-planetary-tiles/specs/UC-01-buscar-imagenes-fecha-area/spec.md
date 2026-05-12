## MODIFIED Requirements

### Requirement: Búsqueda Temporal y Espacial de Imágenes (RF-01)
El sistema SHALL permitir ingresar dos fechas (mes y año) y realizar una consulta a la colección `sentinel-2-l2a` usando la intersección del AOI definido por el archivo KML provisto. Los resultados SHALL ser filtrados para excluir tiles MGRS que no estén en la lista de tiles permitidos (`ALLOWED_TILES`), devolviendo únicamente los items de los tiles MPS, MQT y MQS.

#### Scenario: Búsqueda exitosa con resultados
- **WHEN** el usuario ingresa un rango de fechas válido (mes/año inicio y fin) y el archivo KML está cargado
- **THEN** el sistema extrae las coordenadas del AOI desde el KML
- **AND** construye la consulta STAC con filtros: colección `sentinel-2-l2a`, rango de fechas y geometría
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
