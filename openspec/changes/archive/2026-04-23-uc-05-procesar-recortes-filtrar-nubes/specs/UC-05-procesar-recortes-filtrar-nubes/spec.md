## MODIFIED Requirements

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
