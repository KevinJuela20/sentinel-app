# Casos de Uso Detallados - Sentinel Data Downloader (Fase 2)

**Basado en SRS:** `SRS_SentinelDataDownloader_v1.0.md`
**Fecha:** 21 de abril de 2026

## Casos de Uso

### Procesar recortes y filtrar nubes
**Code**: UC-05
**Actors**: Sistema, Sistema de Archivos
**Purpose**: Generar recortes limpios y organizados para alimentar los modelos de IA.
**Priority**: High
**Overview**: El sistema itera sobre los polígonos de la cuadrícula y las bandas descargadas. Utiliza la máscara SCL para descartar áreas con nubes y guarda solo los recortes válidos en formato PNG.
**Preconditions**: 
- Datos de la Fase 1 descargados en carpetas (UC-04).
- Archivo `Cuadrícula_ARH.geojson` cargado.
**Postconditions**: Subcarpetas creadas con archivos `.png` de recortes sin nubes.
**Reference**: RF-05, RF-07

#### Flujo Primario

| Sistema | Sistema de Archivos |
| :------ | :------------------ |
| 1. Inicia el escaneo de la carpeta `Data_Sentinel`. | |
| 2. Carga los polígonos de `Cuadrícula_ARH.geojson`. | |
| 3. Para cada fecha descargada: | |
| 4. Por cada polígono en la cuadrícula: | |
| 5. Realiza el recorte (crop) de las bandas B02, B03, B04 y SCL para ese polígono. | |
| 6. Analiza los píxeles de la capa SCL recortada. | |
| 7. ¿Existen píxeles con códigos 1, 2, 3, 8, 9 o 10? | |
| 8. No (Limpio): Genera una imagen combinada RGB (PNG). | |
| | 9. Guarda el archivo como `[id_poligono]_[fecha].png` en la subcarpeta del día. |
| 10. Elimina archivos ráster temporales (.tif) marcados para limpieza. | 11. Elimina los archivos especificados para liberar espacio. |

#### Flujos Secundarios

| Sistema | Sistema de Archivos |
| :------ | :------------------ |
| 8. Sí (Nubes detectadas): Descarta el recorte. | |
| 9. Registra en el log que el polígono X fue omitido por nubosidad. | |

---

### Escalar imágenes con modelos EDSR
**Code**: UC-06
**Actors**: Sistema, Sistema de Archivos
**Purpose**: Aumentar la resolución de los recortes limpios para permitir una mejor detección de cambios.
**Priority**: Medium
**Overview**: Toma los archivos PNG generados en el UC-05, los redimensiona a 128x128 y luego aplica modelos de super-resolución EDSR para obtener imágenes de 1024x1024.
**Preconditions**: 
- Recortes limpios generados (UC-05).
- Modelos EDSR cargados en el sistema.
**Postconditions**: Archivos PNG escalados a 1024x1024 píxeles.
**Reference**: RF-06

#### Flujo Primario

| Sistema | Sistema de Archivos |
| :------ | :------------------ |
| 1. Identifica los recortes limpios (.png) en las subcarpetas del día. | |
| 2. Redimensiona cada imagen a un tamaño base de 128x128 píxeles. | |
| 3. Aplica el modelo EDSRx4 a la imagen de 128x128 para llegar a 512x512. | |
| 4. Aplica el modelo EDSRx2 a la imagen de 512x512 para llegar a 1024x1024. | |
| | 5. Sobrescribe o guarda el nuevo archivo escalado en la carpeta de procesados. |
| 6. Verifica que el tamaño final sea exactamente 1024x1024. | |
| 7. Notifica al usuario que el proceso de super-resolución ha concluido. | |
