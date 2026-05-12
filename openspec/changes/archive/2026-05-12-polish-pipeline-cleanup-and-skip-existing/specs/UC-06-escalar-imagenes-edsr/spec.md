## MODIFIED Requirements

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
