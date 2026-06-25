## ADDED Requirements

### Requirement: Filtro de deduplicación de recortes por asignación de tile (RF-05-DEDUP)
El sistema SHALL mantener un diccionario de asignación fija `IDS_POR_TILE` que mapea cada tile (MPS, MQT, MQS) a una lista de IDs de celdas de borde. Antes de procesar cualquier recorte, el sistema SHALL verificar si el ID de la celda pertenece a este diccionario. Si el ID está en la lista de un tile específico, el sistema SHALL procesar el recorte ÚNICAMENTE cuando el tile en curso coincida con el tile asignado. Si el tile no coincide, el sistema SHALL omitir el recorte sin error.

#### Scenario: ID de borde procesado en el tile correcto
- **WHEN** el sistema procesa la celda con ID "894" durante la iteración del tile MQT
- **AND** el ID "894" está asignado al tile MQT en `IDS_POR_TILE`
- **THEN** el sistema SHALL proceder con la validación SCL y el recorte normal
- **AND** si el recorte pasa la validación de nubes, SHALL guardarlo como PNG

#### Scenario: ID de borde omitido en tile incorrecto
- **WHEN** el sistema procesa la celda con ID "894" durante la iteración del tile MPS
- **AND** el ID "894" está asignado al tile MQT en `IDS_POR_TILE`
- **THEN** el sistema SHALL omitir el recorte sin generar error ni log de advertencia
- **AND** SHALL continuar con la siguiente celda

#### Scenario: ID no listado sin recorte previo en disco
- **WHEN** el sistema procesa la celda con ID "15" que NO está en `IDS_POR_TILE`
- **AND** no existe ningún archivo `15_<fecha>_*.png` en la carpeta `crops/`
- **THEN** el sistema SHALL proceder con la validación SCL y el recorte normal

#### Scenario: ID no listado con recorte previo existente en disco
- **WHEN** el sistema procesa la celda con ID "15" que NO está en `IDS_POR_TILE`
- **AND** ya existe un archivo `15_<fecha>_*.png` en la carpeta `crops/`
- **THEN** el sistema SHALL omitir el recorte para evitar duplicación
- **AND** SHALL registrar en los logs la omisión indicando el ID y la razón

### Requirement: Estadísticas de deduplicación en el resultado del procesamiento
El sistema SHALL incluir un contador `dedup_skipped` en el diccionario de estadísticas retornado por `process_all_grids` que indique cuántos recortes fueron omitidos por deduplicación (tanto por asignación de tile como por existencia previa).

#### Scenario: Conteo de omisiones por deduplicación
- **WHEN** el sistema finaliza el procesamiento de una fecha
- **THEN** el diccionario de resultados SHALL incluir la clave `dedup_skipped` con el número total de recortes omitidos por deduplicación
- **AND** los contadores `saved` y `skipped` (por nubes) SHALL mantenerse con su semántica actual
