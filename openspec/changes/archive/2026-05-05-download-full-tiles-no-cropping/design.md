## Context

La descarga de datos de Sentinel-2 se realiza actualmente mediante el acceso a los assets de Microsoft Planetary Computer (MPC). Para optimizar el ancho de banda y el almacenamiento, el sistema aplica un recorte en tiempo real (clipping) utilizando la geometría del área de estudio (AOI). El usuario ha solicitado desactivar este comportamiento para obtener los archivos GeoTIFF originales completos.

## Goals / Non-Goals

**Goals:**
- Descargar el archivo `.tif` completo para cada banda seleccionada.
- Eliminar cualquier dependencia del AOI (KML/GeoJSON) durante la descarga física de los archivos.
- Preservar la integridad del tile original (aprox. 10980x10980 píxeles para bandas de 10m).

**Non-Goals:**
- No se modificará la lógica de búsqueda (UC-01), que seguirá filtrando tiles basados en la intersección con el AOI.
- No se modificará la previsualización (UC-02), que seguirá mostrando el recorte para facilitar la evaluación rápida.

## Decisions

### 1. Eliminación del Cropping en la Descarga
**Decisión**: Modificar la función de descarga para realizar un "stream download" directo de la URL del asset firmado, en lugar de abrir el archivo con `rioxarray` o `rasterio` para aplicar una máscara/ventana.
**Racional**: Es el método más rápido y robusto para asegurar que se obtiene el archivo íntegro sin reproyecciones ni recortes accidentales.

### 2. Manejo de Memoria
**Decisión**: Utilizar descargas por bloques (chunks) para evitar cargar el tile completo en RAM antes de escribirlo en disco.
**Racional**: Un tile completo de Sentinel-2 puede pesar cientos de megabytes; la descarga por bloques asegura estabilidad en el sistema.

### 3. Impacto en el Procesamiento Posterior
**Decisión**: El paso de "Generar Recortes Limpios" (UC-05) seguirá existiendo y es ahí donde se realizará el recorte final a la cuadrícula del proyecto.
**Racional**: Esto permite al usuario tener el tile completo como "materia prima" y aún así generar los datasets optimizados para IA posteriormente.

## Risks / Trade-offs

- **[Riesgo] Espacio en Disco** → Descargar tiles completos aumentará drásticamente el uso de almacenamiento (de ~5-10MB por recorte a ~100-150MB por tile/banda). *Mitigación*: Se informará al usuario que requiere más espacio disponible.
- **[Trade-off] Tiempo de Espera** → La descarga será más lenta. *Racional*: Es aceptable dado el requerimiento de disponer de los datos originales completos.
