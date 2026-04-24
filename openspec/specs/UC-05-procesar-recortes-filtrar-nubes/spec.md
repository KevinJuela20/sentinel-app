## Purpose

Generar recortes limpios y organizados para alimentar los modelos de IA. El sistema itera sobre los polígonos de la cuadrícula y las bandas descargadas, utiliza la máscara SCL para descartar áreas con nubes y guarda solo los recortes válidos en formato PNG.

## Requirements

### Requirement: Preprocesamiento de Recortes y Filtrado de Nubes (RF-05)
El sistema SHALL verificar la capa SCL por cada polígono en `Cuadrícula_ARH.geojson`. Si los píxeles indican presencia de nubes (códigos 1, 2, 3, 8, 9, 10) superando el umbral del 5% del área del recorte, el sistema debe descartar el recorte. Si está limpio, se guarda como .png con el formato `[id_poligono]_[fecha].png`.

#### Scenario: Recorte limpio guardado exitosamente
- **WHEN** el sistema analiza la capa SCL de un polígono
- **AND** la proporción de píxeles con códigos de nubes (1, 2, 3, 8, 9, 10) es igual o menor al 5%
- **THEN** genera una imagen combinada RGB (PNG) de 8 bits a partir de las bandas B04, B03, B02
- **AND** guarda el archivo como `[id_poligono]_[fecha].png` en la subcarpeta `crops/` dentro de la carpeta del día

#### Scenario: Recorte con nubes descartado
- **WHEN** el sistema analiza la capa SCL de un polígono
- **AND** detecta que la proporción de píxeles con códigos de nubes (1, 2, 3, 8, 9, 10) es mayor al 5%
- **THEN** omite la generación del PNG para ese polígono
- **AND** registra el evento en los logs indicando el ID del polígono y el porcentaje de nubosidad detectado

#### Scenario: Limpieza de archivos temporales
- **WHEN** el procesamiento de todos los polígonos de la cuadrícula para una fecha específica ha finalizado
- **THEN** el sistema SHALL eliminar los archivos `.tif` originales de esa fecha para optimizar espacio
- **AND** solo conserva los recortes PNG generados

### Requirement: Estructura de Almacenamiento para Recortes (RF-07)
El sistema SHALL almacenar los recortes limpios en subcarpetas `crops/` dentro de la estructura jerárquica `Data_Sentinel/[Año]/[Mes]/[Día]/`.

#### Scenario: Organización de recortes en subcarpetas
- **WHEN** se generan recortes limpios para una fecha
- **THEN** se almacenan en una subcarpeta dedicada `crops/` dentro de `[Año]/[Mes]/[Día]/`

## Acceptance Criteria
- Los polígonos de la cuadrícula se procesan correctamente
- Los recortes con nubes se descartan con registro en log
- Los recortes limpios se guardan como PNG con nombre `[id]_[fecha]`
- Los archivos temporales se eliminan tras el procesamiento
- Los recortes se organizan en subcarpetas por fecha

## Stories
- [ ] Story 1: Implementar escaneo de la carpeta `Data_Sentinel` para encontrar datos descargados
- [ ] Story 2: Cargar y iterar sobre polígonos de `Cuadrícula_ARH.geojson`
- [ ] Story 3: Implementar recorte (crop) de bandas B02, B03, B04 y SCL por polígono
- [ ] Story 4: Implementar filtro de nubes basado en capa SCL (códigos 1,2,3,8,9,10)
- [ ] Story 5: Generar imagen RGB combinada (PNG) para recortes limpios
- [ ] Story 6: Implementar limpieza de archivos temporales .tif
- [ ] Story 7: Agregar logging de polígonos omitidos por nubosidad

## Technical Notes
- Components: Motor de Procesamiento, Gestor del Sistema de Archivos
- Dependencies: UC-04 (requiere datos descargados de Fase 1)
- Algoritmo: `filter_clouds(raster_scl)` — umbral de 5% de píxeles nublados
- Códigos SCL a filtrar: 1 (Saturado), 2 (Sombra oscura), 3 (Sombra nube), 8 (Nube media), 9 (Nube alta), 10 (Cirrus)
- Librerías: `rasterio`, `numpy`, `geopandas`

## Traceability
| Source | Reference |
| ------ | --------- |
| SRS | RF-05, RF-07 |
| Use Case | UC-05 |
| SDD | Motor de Procesamiento + Filtro de Nubes (sección 5.2) |
