## Purpose

Obtener los archivos de datos (bandas y TIF) guardándolos localmente con nombres estandarizados y recortes precisos. El sistema firma las URLs de descarga, recorta el ráster a la cuadrícula GeoJSON y guarda los archivos en carpetas organizadas jerárquicamente.

## Requirements

### Requirement: Descarga Optimizada de Bandas Seleccionadas (RF-04)
El sistema SHALL descargar las bandas B02, B03, B04 y SCL, además del producto True Color (.tif), realizando un recorte (clip) a los polígonos del archivo `Cuadrícula_ARH.geojson` antes de guardar en disco. Los archivos resultantes deben ser GeoTIFF con el CRS correcto.

#### Scenario: Descarga exitosa con recorte
- **WHEN** el usuario inicia el proceso de descarga tras confirmar la selección (UC-03)
- **THEN** el sistema firma las URLs para los assets: B02, B03, B04, SCL y Visual mediante `planetary_computer.sign`
- **AND** descarga las bandas y realiza el recorte (clip) usando los límites de `Cuadrícula_ARH.geojson`
- **AND** crea la estructura de carpetas `Data_Sentinel/[Año]/[Mes]/[Día]`
- **AND** guarda los archivos resultantes con la fecha de adquisición y el nombre de la banda (ej: `20250101_B02.tif`)
- **AND** notifica al usuario que la descarga ha finalizado mediante una barra de progreso al 100%

#### Scenario: Error durante la descarga de una banda
- **WHEN** una URL firmada expira o falla la descarga de una banda específica
- **THEN** el sistema reintenta la firma y descarga
- **AND** si persiste el error, registra el fallo y continúa con las demás bandas

### Requirement: Estructura de Almacenamiento Jerárquica (RF-07)
El sistema SHALL organizar las descargas en la estructura `Data_Sentinel/[Año]/[Mes]/[Día]/` garantizando que los nombres de carpetas tengan ceros a la izquierda para meses y días (ej: `01` para Enero).

#### Scenario: Creación automática de estructura de carpetas
- **WHEN** se guardan archivos para una fecha nueva
- **THEN** el sistema crea automáticamente la jerarquía `Data_Sentinel/[Año]/[Mes]/[Día]/` en el directorio raíz del proyecto o ruta configurada
- **AND** almacena los archivos recortados en dicha carpeta

## Acceptance Criteria
- Las bandas B02, B03, B04, SCL y Visual se descargan correctamente
- El recorte a `Cuadrícula_ARH.geojson` se aplica antes de guardar
- La estructura de carpetas sigue el patrón `[Año]/[Mes]/[Día]`
- Los archivos se nombran con la fecha de adquisición
- El usuario recibe notificación al completar la descarga
- Se gestionan errores de descarga sin detener el proceso completo

## Stories
- [ ] Story 1: Implementar firma de URLs con `planetary_computer.sign` para los assets
- [ ] Story 2: Descargar bandas B02, B03, B04, SCL y Visual
- [ ] Story 3: Implementar recorte (clip) de ráster con `rasterio` y geometría GeoJSON
- [ ] Story 4: Crear la estructura de carpetas jerárquica `Data_Sentinel/[Año]/[Mes]/[Día]`
- [ ] Story 5: Nombrar archivos con fecha de adquisición
- [ ] Story 6: Implementar barra de progreso y notificación de finalización
- [ ] Story 7: Manejar errores de descarga con reintentos

## Technical Notes
- Components: Motor de Procesamiento, Gestor del Sistema de Archivos
- Dependencies: UC-03 (requiere selección confirmada)
- Archivo requerido: `Cuadrícula_ARH.geojson`
- Rutas de almacenamiento: `/Desktop/Download Data`, `/Desktop/Data_Sentinel`
- Librerías: `rasterio`, `geopandas`, `planetary-computer`

## Traceability
| Source | Reference |
| ------ | --------- |
| SRS | RF-04, RF-07 |
| Use Case | UC-04 |
| SDD | Motor de Procesamiento + Gestor FileSys (secciones 3.2, 5.1) |
