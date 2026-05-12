## ADDED Requirements

### Requirement: Filtrado de Items STAC por Tile ID (RF-01)
El sistema SHALL filtrar los items STAC devueltos por la API de MPC para conservar únicamente aquellos cuyo tile MGRS esté incluido en la lista de tiles permitidos (`ALLOWED_TILES`). Los tiles permitidos por defecto SHALL ser: MPS, MQT y MQS.

#### Scenario: Filtrado exitoso de tiles no deseados
- **WHEN** la búsqueda STAC retorna items con tiles MPT, MPS, MQT y MQS
- **THEN** el sistema descarta los items del tile MPT
- **AND** devuelve únicamente los items correspondientes a MPS, MQT y MQS
- **AND** el conteo total (`SearchResult.total`) refleja la cantidad filtrada

#### Scenario: Todos los items pertenecen a tiles permitidos
- **WHEN** la búsqueda STAC retorna items que solo contienen tiles MPS, MQT y MQS
- **THEN** el sistema devuelve todos los items sin modificación
- **AND** no se loguea ningún filtrado

#### Scenario: Item con tile ID no reconocible
- **WHEN** un item STAC tiene un `item_id` del cual no se puede extraer el tile ID
- **THEN** el sistema conserva el item (no lo descarta)
- **AND** loguea un warning indicando que no se pudo extraer el tile ID

### Requirement: Extracción del Tile ID desde Item ID STAC
El sistema SHALL extraer el código MGRS de tile desde el `item_id` de Sentinel-2 usando el patrón de nomenclatura estándar (segmento que comienza con `T` seguido de 5 caracteres alfanuméricos).

#### Scenario: Extracción exitosa del tile ID
- **WHEN** el `item_id` sigue el formato estándar de Sentinel-2 (e.g., `S2B_MSIL2A_20250115T151619_R125_T17MPS_20250115T190440`)
- **THEN** el sistema extrae el sufijo MGRS de 3 caracteres (e.g., `MPS`)

#### Scenario: Formato de item ID no estándar
- **WHEN** el `item_id` no contiene un segmento de tile MGRS reconocible
- **THEN** la función retorna `None`
- **AND** el item no es descartado por el filtro

### Requirement: Configurabilidad de la lista de tiles permitidos
El sistema SHALL definir la lista de tiles permitidos como una constante de módulo (`ALLOWED_TILES`) que pueda ser modificada sin cambiar la interfaz pública de las funciones.

#### Scenario: Modificación de la lista de tiles
- **WHEN** un desarrollador cambia los valores de `ALLOWED_TILES` en `search_controller.py`
- **THEN** el filtrado automáticamente aplica los nuevos tiles sin necesidad de cambios adicionales en el código
