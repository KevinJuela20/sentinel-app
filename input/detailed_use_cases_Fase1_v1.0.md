# Casos de Uso Detallados - Sentinel Data Downloader (Fase 1)

**Basado en SRS:** `SRS_SentinelDataDownloader_v1.0.md`
**Fecha:** 21 de abril de 2026

## Casos de Uso

### Buscar imágenes por fecha y área
**Code**: UC-01
**Actors**: Usuario (Analista), MPC STAC API
**Purpose**: Permitir que el analista encuentre imágenes de Sentinel-2 que coincidan con un rango temporal y un área geográfica.
**Priority**: High
**Overview**: El usuario ingresa parámetros de fecha y el sistema consulta el catálogo de Microsoft Planetary Computer para obtener metadatos de imágenes que se intersecten con el área definida en el archivo KML.
**Preconditions**: 
- El sistema tiene acceso a internet.
- El archivo `ARH_ETAPA.kml` es válido y está cargado o accesible.
**Postconditions**: Se muestra una lista o referencia a las imágenes encontradas para su posterior visualización.
**Reference**: RF-01

#### Flujo Primario

| Usuario (Analista) | Sistema | MPC STAC API |
| :----------------- | :------ | :----------- |
| 1. Ingresa las fechas de inicio y fin (Mes/Año) en la barra lateral. | | |
| | 2. Extrae las coordenadas del área de estudio desde el archivo KML. | |
| | 3. Construye la consulta STAC con los filtros: colección `sentinel-2-l2a`, rango de fechas y geometría. | |
| | 4. Envía la solicitud de búsqueda. | 5. Recibe la solicitud y busca en el catálogo. |
| | 7. Recibe los metadatos de los items STAC encontrados. | 6. Devuelve la lista de imágenes con sus metadatos (fecha, cobertura de nubes, assets). |
| | 8. Valida si hay resultados y los prepara para la galería. | |

#### Flujos Secundarios

| Usuario (Analista) | Sistema | MPC STAC API |
| :----------------- | :------ | :----------- |
| | 8. El sistema no encuentra imágenes para el rango dado. | |
| | 9. Informa al usuario que no hay resultados y solicita ajustar las fechas. | |

---

### Previsualizar imagen con máscara de área
**Code**: UC-02
**Actors**: Usuario (Analista), MPC Tiler
**Purpose**: Evaluar visualmente la calidad de la imagen y la cobertura de nubes dentro del área de estudio específica.
**Priority**: Medium
**Overview**: Por cada imagen encontrada en la búsqueda, el sistema solicita un tile renderizado y le aplica una máscara de transparencia basada en el área de estudio del usuario.
**Preconditions**: 
- UC-01 completado exitosamente.
- El servicio MPC Tiler está disponible.
**Postconditions**: El usuario ve una previa de la imagen recortada visualmente.
**Reference**: RF-02

#### Flujo Primario

| Usuario (Analista) | Sistema | MPC Tiler |
| :----------------- | :------ | :----------- |
| 1. El usuario visualiza la galería de resultados. | | |
| | 2. Solicita al Tiler una visualización True Color para el item STAC actual. | |
| | | 3. Genera el tile de baja resolución para las coordenadas solicitadas. |
| | 5. Recibe el tile de imagen. | 4. Devuelve el tile al sistema. |
| | 6. Aplica un recorte dinámico (masking) usando la geometría del área de interés para hacer transparente lo exterior. | |
| | 7. Renderiza el mini-mapa o thumbnail en la interfaz. | |

---

### Seleccionar imágenes de la galería
**Code**: UC-03
**Actors**: Usuario (Analista)
**Purpose**: Marcar las imágenes que el usuario considera aptas para procesos posteriores de descarga y análisis.
**Priority**: High
**Overview**: El analista revisa los metadatos y la previsualización visual para marcar una o más imágenes como "seleccionadas".
**Preconditions**: 
- La galería de imágenes está desplegada (UC-02).
**Postconditions**: El sistema mantiene una lista temporal de IDs de imágenes para la descarga.
**Reference**: RF-03

#### Flujo Primario

| Usuario (Analista) | Sistema |
| :----------------- | :------ |
| 1. Revisa el porcentaje de nubosidad y la fecha debajo de cada imagen. | |
| 2. Marca el checkbox de selección para las imágenes que considera "limpias". | |
| | 3. Registra el ID del item y sus enlaces de assets en la lista de descarga. |
| 4. Repite el proceso para múltiples meses si es necesario. | |
| 5. Presiona el botón de confirmación de selección. | |
| | 6. Habilita las opciones de descarga. |

---

### Descargar bandas seleccionadas con recorte
**Code**: UC-04
**Actors**: Usuario (Analista), MPC STAC API, Sistema de Archivos
**Purpose**: Obtener los archivos de datos (bandas y TIF) guardándolos localmente con nombres estandarizados y recortes precisos.
**Priority**: High
**Overview**: El sistema firma las URLs de descarga, opcionalmente recorta el ráster a la cuadrícula GeoJSON y guarda los archivos en carpetas organizadas.
**Preconditions**: 
- Selección confirmada (UC-03).
- Archivo `Cuadrícula_ARH.geojson` disponible.
**Postconditions**: Archivos `.tif` guardados en `/Desktop/Download Data`.
**Reference**: RF-04, RF-07

#### Flujo Primario

| Usuario (Analista) | Sistema | MPC STAC API |
| :----------------- | :------ | :----------- |
| 1. Inicia el proceso de descarga. | | |
| | 2. Para cada una de las imágenes seleccionadas: | |
| | 3. Solicita la firma de las URLs para los assets: B02, B03, B04, SCL y Visual. | |
| | | 4. Genera y firma los tokens SAS de acceso. |
| | 5. Recibe las URLs firmadas. | |
| | 6. Descarga las bandas y realiza el recorte (clip) usando los límites de `Cuadrícula_ARH.geojson`. | |
| | 7. Crea la estructura de carpetas `[Año]/[Mes]/[Día]` en el escritorio. | |
| | 8. Guarda los archivos resultantes con la fecha de adquisición en el nombre. | |
| | 9. Notifica al usuario que la descarga ha finalizado. | |
