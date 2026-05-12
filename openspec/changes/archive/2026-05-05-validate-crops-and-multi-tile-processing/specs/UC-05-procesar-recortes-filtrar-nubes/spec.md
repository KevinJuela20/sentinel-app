## MODIFIED Requirements

### Requirement: Preprocesamiento de Recortes y Filtrado de Nubes (RF-05)
El sistema SHALL verificar la capa SCL por cada polígono en `Cuadrícula_ARH.geojson`. El sistema SHALL descartar cualquier recorte cuya máscara tenga dimensiones menores a **124x124 píxeles** (recortes de borde de tile). Si el recorte supera la validación de tamaño y el umbral de nubes (5%), el sistema SHALL redimensionarlo a exactamente **128x128 píxeles** antes de guardarlo como .png. El formato de nombre SHALL ser `[id_poligono]_[fecha]_[id_tile].png` para evitar colisiones entre tiles.

#### Scenario: Recorte válido guardado con redimensionamiento
- **WHEN** el sistema analiza un polígono y su intersección con un tile
- **AND** las dimensiones del recorte resultante son mayores o iguales a 124x124 píxeles
- **AND** la proporción de píxeles nublados es igual o menor al 5%
- **THEN** el sistema redimensiona el recorte a exactamente 128x128 píxeles usando interpolación cúbica
- **AND** genera la imagen combinada RGB (PNG)
- **AND** guarda el archivo como `[id_poligono]_[fecha]_[id_tile].png` en la subcarpeta `crops/`

#### Scenario: Recorte descartado por dimensiones insuficientes
- **WHEN** el sistema realiza el recorte de un polígono en los límites de un tile
- **AND** detecta que el ancho o el alto es menor a 124 píxeles
- **THEN** el sistema omite el procesamiento de ese recorte sin guardarlo
- **AND** continúa con el siguiente polígono/tile

#### Scenario: Procesamiento de múltiples tiles por fecha
- **WHEN** existen archivos de múltiples tiles (ej: MPS, MQT, MQS) para una misma fecha
- **THEN** el sistema SHALL iterar sobre cada tile de forma independiente
- **AND** procesar la cuadrícula completa contra cada tile, guardando los recortes válidos diferenciados por su ID de tile en el nombre de archivo
