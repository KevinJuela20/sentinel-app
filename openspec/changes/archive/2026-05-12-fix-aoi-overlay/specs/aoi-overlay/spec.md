## MODIFIED Requirements

### Requirement: Superposición Vectorial del AOI (RF-OVERLAY-01)
El sistema SHALL dibujar el contorno **completo** del AOI sobre las imágenes de previsualización, independientemente de si el tile cubre la totalidad del área.

#### Scenario: Cobertura parcial del AOI por el Tile
- **GIVEN** un AOI cuya extensión es mayor a la del Tile renderizado (ej. Tile MQT)
- **WHEN** el sistema genera la previsualización para la galería
- **THEN** SHALL recortar (clip) la geometría del AOI al bounding box del tile usando intersección geométrica
- **AND** SHALL dibujar únicamente la porción del contorno que cae dentro del tile
- **AND** SHALL usar un contorno rojo vibrante (#FF0000) de 2px
- **AND** el polígono SHALL cerrarse visualmente (el último punto conectado al primero)

#### Scenario: AOI completamente dentro del Tile
- **GIVEN** un AOI cuya extensión cabe completamente dentro del Tile (ej. Tile MPS)
- **WHEN** el sistema genera la previsualización
- **THEN** SHALL dibujar el contorno completo del AOI sobre la imagen del tile
- **AND** la geometría recortada SHALL ser idéntica a la geometría original

#### Scenario: Tile sin intersección con el AOI
- **GIVEN** un Tile cuyo bounding box no intersecta la geometría del AOI
- **WHEN** el sistema genera la previsualización
- **THEN** SHALL mostrar la imagen del tile sin contorno superpuesto
- **AND** SHALL no generar errores ni excepciones

#### Scenario: Geometría del AOI con coordenadas 3D
- **GIVEN** un archivo KML con coordenadas en formato `lon,lat,alt`
- **WHEN** el sistema procesa la geometría para la superposición
- **THEN** SHALL usar únicamente las componentes `lon,lat` (descartar altitud)

## ADDED Requirements

### Requirement: Fuente de datos KML correcta (RF-OVERLAY-02)
El sistema SHALL cargar la geometría del AOI desde el archivo `ARH_ETAPA.kml` que contiene el polígono detallado de la zona de estudio (cuenca MACHANGARA).

#### Scenario: Carga del polígono real de estudio
- **GIVEN** el archivo `external/ARH_ETAPA.kml` existe y contiene geometría válida
- **WHEN** el sistema inicializa la sesión
- **THEN** SHALL cargar la geometría del polígono detallado (~150 vértices)
- **AND** SHALL almacenarla en `session_state["aoi_geom"]` como diccionario GeoJSON

#### Scenario: Archivo KML no encontrado
- **GIVEN** el archivo `external/ARH_ETAPA.kml` no existe
- **WHEN** el sistema intenta cargar el AOI
- **THEN** SHALL mostrar un mensaje de error indicando la ruta esperada
- **AND** SHALL permitir al usuario continuar sin AOI superpuesto
