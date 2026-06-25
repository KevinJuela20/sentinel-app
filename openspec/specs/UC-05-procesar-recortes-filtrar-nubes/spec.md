## Purpose

Generar recortes limpios y organizados para alimentar los modelos de IA. El sistema itera sobre los polígonos de la cuadrícula y las bandas descargadas, utiliza la máscara SCL para descartar áreas con nubes y guarda solo los recortes válidos en formato PNG.

## Requirements

### Requirement: Preprocesamiento de Recortes y Filtrado de Nubes (RF-05)
El sistema SHALL verificar la capa SCL por cada polígono en `Cuadrícula_ARH.geojson`. El sistema SHALL descartar cualquier recorte cuya máscara tenga dimensiones menores a **124x124 píxeles** (recortes de borde de tile). Si el recorte supera la validación de tamaño y el umbral de nubes (5%), el sistema SHALL redimensionarlo a exactamente **128x128 píxeles** antes de guardarlo como .png. El formato de nombre SHALL ser `[id_poligono]_[fecha]_[id_tile].png` para evitar colisiones entre tiles. **Adicionalmente**, antes de la validación de tamaño y SCL, el sistema SHALL aplicar un filtro de deduplicación que verifica si la celda debe procesarse en el tile actual, basándose en la asignación fija de IDs de borde (`IDS_POR_TILE`) y en la existencia previa de recortes en disco.

#### Scenario: Recorte válido guardado con redimensionamiento
- **WHEN** el sistema analiza un polígono y su intersección con un tile
- **AND** el filtro de deduplicación permite el procesamiento de la celda en este tile
- **AND** las dimensiones del recorte resultante son mayores o iguales a 124x124 píxeles
- **AND** la proporción de píxeles nublados es igual o menor al 5%
- **THEN** el sistema redimensiona el recorte a exactamente 128x128 píxeles usando interpolación cúbica
- **AND** genera la imagen combinada RGB (PNG)
- **AND** guarda el archivo como `[id_poligono]_[fecha]_[id_tile].png` en la subcarpeta `crops/`

#### Scenario: Recorte descartado por dimensiones insuficientes
- **WHEN** el sistema realiza el recorte de un polígono en los límites de un tile
- **AND** el filtro de deduplicación permite el procesamiento
- **AND** detecta que el ancho o el alto es menor a 124 píxeles
- **THEN** el sistema omite el procesamiento de ese recorte sin guardarlo
- **AND** continúa con el siguiente polígono/tile

#### Scenario: Procesamiento de múltiples tiles por fecha con deduplicación
- **WHEN** existen archivos de múltiples tiles (MPS, MQT, MQS) para una fecha
- **THEN** el sistema SHALL procesar la cuadrícula completa contra cada tile
- **AND** antes de cada recorte, SHALL aplicar el filtro de deduplicación (`should_process_cell`)
- **AND** SHALL omitir las celdas que ya fueron recortadas por un tile previo o cuya asignación fija no coincida con el tile actual
- **AND** al guardar el resultado en PNG, el sistema SHALL aplicar un escalado de contraste mediante percentiles (2% al 98%) para normalizar la visualización

#### Scenario: Generación de mosaico RGB consolidado del área de estudio
- **WHEN** finaliza el procesamiento de los recortes de la cuadrícula
- **THEN** el sistema SHALL cargar la geometría del archivo `ARH_ETAPA.kml`
- **AND** para cada uno de los tres tiles descargados (MPS, MQT, MQS), SHALL generar un producto RGB (B04, B03, B02) recortado por dicha geometría
- **AND** el sistema SHALL unir (merge) los resultados de los tres tiles en un único archivo GeoTIFF de 3 bandas
- **AND** el sistema SHALL limitar los valores de reflectancia de la imagen a un máximo de 3500 (`np.clip(band, 0, 3500)`)
- **AND** el archivo resultante SHALL guardarse con el nombre `Color_YYYY-MM-DD.tif` en formato `uint16` en la carpeta de la fecha
- **AND** el sistema SHALL eliminar las bandas individuales descargadas únicamente si la generación del mosaico y los recortes fue exitosa

#### Scenario: Generación de mosaico RGB de la zona de estudio
- **WHEN** el procesamiento de recortes para una fecha específica ha finalizado
- **AND** antes de eliminar los archivos temporales
- **THEN** el sistema SHALL identificar todos los archivos `*_visual.tif` de los tiles descargados
- **AND** realizar una unión (mosaico) de estos archivos para cubrir la zona de estudio completa
- **AND** guardar el resultado como `Color_YYYY-MM-DD.tif` en la raíz del directorio de la fecha

#### Scenario: Limpieza de archivos temporales
- **WHEN** el mosaico RGB ha sido generado con éxito
- **AND** los recortes PNG han sido guardados
- **THEN** el sistema SHALL eliminar los archivos `.tif` originales (excepto el mosaico `Color_*.tif`) para optimizar espacio

### Requirement: Estructura de Almacenamiento para Recortes (RF-07)
El sistema SHALL almacenar los recortes limpios en subcarpetas `crops/` dentro de la estructura jerárquica `Data_Sentinel/[Año]/[Mes]/[Día]/`.

#### Scenario: Organización de recortes en subcarpetas
- **WHEN** se generan recortes limpios para una fecha
- **THEN** se almacenan en una subcarpeta dedicada `crops/` dentro de `[Año]/[Mes]/[Día]/`

## Acceptance Criteria
- Todos los recortes RGB de una misma fecha/tile tienen dimensiones idénticas y alineación perfecta
- La validación de nubes se realiza antes de la extracción de las bandas de 10m para optimizar recursos
- Los recortes con dimensiones menores a 63px son descartados automáticamente
- Las imágenes PNG resultantes presentan un contraste mejorado y consistente gracias a la normalización por percentiles
- Se registra en los logs el descarte de celdas por nubes o por tamaño insuficiente

## Stories
- [ ] Story 1: Implementar validación de nubes en resolución nativa SCL (20m)
- [ ] Story 2: Configurar B04 como referencia espacial para la definición de ventanas de recorte
- [ ] Story 3: Extraer bandas RGB (10m) alineadas a la ventana de referencia
- [ ] Story 4: Implementar descarte automático de recortes incompletos (<63px)
- [ ] Story 5: Implementar normalización de contraste 2%-98% en la generación de PNG
- [ ] Story 6: Guardar recortes en la subcarpeta `crops/` de cada fecha
- [ ] Story 7: Generar mosaico RGB consolidado del área de estudio usando `ARH_ETAPA.kml`

## Technical Notes
- Components: Motor de Procesamiento, Gestor del Sistema de Archivos
- Dependencies: Rasterio, Geopandas, Fiona (KML support)
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
