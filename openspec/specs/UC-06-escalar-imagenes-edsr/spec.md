## Purpose

Aumentar la resolución de los recortes limpios para permitir una mejor detección de cambios. Los archivos PNG generados en UC-05 se redimensionan a 128x128 y luego se aplican modelos de super-resolución EDSR para obtener imágenes de 1024x1024.
## Requirements
### Requirement: Super-resolución con Modelos EDSR (RF-06)
El sistema SHALL redimensionar los recortes limpios a exactamente 128x128 píxeles antes de procesar. El pipeline de super-resolución debe consistir en la aplicación secuencial de dos modelos: EDSR x4 (resultando en 512x512) y EDSR x2 (resultando en 1024x1024). El sistema SHALL asegurar la estabilidad del pipeline mediante el uso de la versión de biblioteca `opencv-contrib-python-headless==4.12.0.88` para garantizar la disponibilidad del módulo `dnn_superres`. El sistema SHALL manejar correctamente la carga de modelos DNN para evitar errores de biblioteca (`AttributeError`) y garantizando que el resultado final sea exactamente 1024x1024 píxeles. Las imágenes resultantes deben guardarse en formato PNG de 8 bits con el sufijo `_SR`. Tras completar el proceso con éxito, el sistema SHALL eliminar los archivos temporales de recortes (`crops/`) y reiniciar el estado de la aplicación.

#### Scenario: Escalado exitoso de un recorte limpio con estabilidad de biblioteca y limpieza
- **WHEN** el sistema identifica un archivo `.png` en la subcarpeta `crops/` de una fecha (independientemente del tile de origen)
- **THEN** redimensiona la imagen a 128x128 píxeles usando interpolación bicúbica si es necesario
- **AND** inicializa el motor DNN y carga el modelo `EDSR_x4.pb` obteniendo una resolución de 512x512
- **AND** reconfigura el motor DNN para el modelo `EDSR_x2.pb` obteniendo una resolución de 1024x1024
- **AND** guarda el archivo en la subcarpeta `super_res/` con el nombre `[original]_SR.png` (manteniendo la referencia al tile)
- **AND** verifica que el tamaño del archivo final sea exactamente 1024x1024 píxeles
- **AND** maneja cualquier excepción de biblioteca de forma que no se interrumpa el flujo del proceso
- **AND** una vez procesadas todas las imágenes de la fecha, ELIMINA la carpeta `crops/` correspondiente
- **AND** REINICIA las variables de sesión de búsqueda y selección para permitir un nuevo ciclo de trabajo

## Acceptance Criteria
- Los recortes se redimensionan correctamente a 128x128 antes del escalado
- EDSRx4 produce imágenes de 512x512
- EDSRx2 produce imágenes finales de 1024x1024
- El tamaño final verificado es exactamente 1024x1024 píxeles
- El usuario recibe notificación al completar el proceso
- Los errores de modelo no detienen el proceso completo

## Stories
- [ ] Story 1: Identificar y listar recortes limpios (.png) en subcarpetas
- [ ] Story 2: Redimensionar imágenes a tamaño base de 128x128
- [ ] Story 3: Cargar e integrar modelo EDSRx4 pre-entrenado
- [ ] Story 4: Cargar e integrar modelo EDSRx2 pre-entrenado
- [ ] Story 5: Aplicar pipeline de escalado secuencial (128→512→1024)
- [ ] Story 6: Verificar tamaño final y guardar en carpeta de procesados
- [ ] Story 7: Implementar notificación y resumen de resultados
- [ ] Story 8: Manejar errores de modelo con logging

## Technical Notes
- Components: Escalador EDSR
- Dependencies: UC-05 (requiere recortes limpios generados)
- Modelos: EDSRx4 (128→512), EDSRx2 (512→1024)
- Entrada: 128x128px PNG de 8 bits
- Salida: 1024x1024px PNG de 8 bits
- Requiere capacidad de cómputo para modelos de IA (GPU recomendada)

## Traceability
| Source | Reference |
| ------ | --------- |
| SRS | RF-06 |
| Use Case | UC-06 |
| SDD | Escalador EDSR (sección 3.2, apéndice 8.2) |
