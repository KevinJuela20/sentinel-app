## MODIFIED Requirements

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
- **WHEN** finaliza el procesamiento de los recortes de la cuadrícula (incluyendo deduplicación)
- **THEN** el sistema SHALL cargar la geometría del archivo `ARH_ETAPA.kml`
- **AND** para cada uno de los tres tiles descargados (MPS, MQT, MQS), SHALL generar un producto RGB (B04, B03, B02) recortado por dicha geometría
- **AND** el sistema SHALL unir (merge) los resultados de los tres tiles en un único archivo GeoTIFF de 3 bandas
- **AND** el archivo resultante SHALL guardarse con el nombre `Color_YYYY-MM-DD.tif` en la carpeta de la fecha
- **AND** el sistema SHALL eliminar las bandas individuales descargadas únicamente si la generación del mosaico y los recortes fue exitosa

#### Scenario: Limpieza de archivos temporales
- **WHEN** el mosaico RGB ha sido generado con éxito
- **AND** los recortes PNG han sido guardados
- **THEN** el sistema SHALL eliminar los archivos `.tif` originales (excepto el mosaico `Color_*.tif`) para optimizar espacio
