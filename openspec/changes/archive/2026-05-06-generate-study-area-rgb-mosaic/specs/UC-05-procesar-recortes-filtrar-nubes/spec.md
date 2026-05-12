## MODIFIED Requirements

### Requirement: Procesamiento y Filtrado de Nubes (RF-05)

#### Scenario: Generación de mosaico RGB consolidado del área de estudio
- **WHEN** finaliza el procesamiento de los recortes de la cuadrícula
- **THEN** el sistema SHALL cargar la geometría del archivo `ARH_ETAPA.kml`
- **AND** para cada uno de los tres tiles descargados (MPS, MQT, MQS), SHALL generar un producto RGB (B04, B03, B02) recortado por dicha geometría
- **AND** el sistema SHALL unir (merge) los resultados de los tres tiles en un único archivo GeoTIFF de 3 bandas
- **AND** el archivo resultante SHALL guardarse con el nombre `Color_YYYY-MM-DD.tif` en la carpeta de la fecha
- **AND** el sistema SHALL eliminar las bandas individuales descargadas únicamente si la generación del mosaico y los recortes fue exitosa

## Acceptance Criteria
- Se genera un archivo `Color_YYYY-MM-DD.tif` que cubre toda el área del KML
- El archivo resultante es RGB (3 bandas) y está georreferenciado
- Las bandas originales (B02, B03, B04, SCL) se eliminan tras el proceso para ahorrar espacio
- El sistema maneja correctamente el caso donde un tile no intersecta con el área del KML
