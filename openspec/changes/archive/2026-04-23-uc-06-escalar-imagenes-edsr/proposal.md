## Why

La resolución nativa de Sentinel-2 (10m por píxel) es insuficiente para ciertas tareas de análisis detallado o inspección visual humana. Este cambio introduce técnicas de Inteligencia Artificial de vanguardia para aumentar la resolución de los recortes generados (Super-Resolución). Al aplicar modelos EDSR (Enhanced Deep Residual Networks), transformamos parches de 128x128 píxeles en imágenes de alta fidelidad de 1024x1024 píxeles, facilitando la detección de cambios sutiles en el terreno.

## What Changes

- **Motor de Super-Resolución (AI Engine)**: Implementación de un pipeline basado en redes neuronales residuales profundas (EDSR) optimizadas para el escalado de imágenes satelitales.
- **Pipeline Secuencial de Escalado**: Lógica para redimensionar recortes a 128x128px y aplicar consecutivamente escalados x4 y x2 para alcanzar una resolución final 8 veces superior (1024x1024px).
- **Gestión de Modelos**: Sistema para la carga eficiente de pesos pre-entrenados y ejecución de inferencia, con soporte para aceleración por hardware si está disponible.
- **Módulo de Verificación de Calidad**: Validación automática de las dimensiones finales y guardado en la estructura jerárquica bajo una nueva subcarpeta `super_res/`.

## Capabilities

### New Capabilities
- Ninguna (implementación de capacidad base definida en UC-06).

### Modified Capabilities
- `uc-06-escalar-imagenes-edsr`: Implementación del requisito funcional RF-06 detallado en el baseline spec.

## Impact

- **sentinel-project/src/super_resolution.py**: Nuevo módulo para el manejo de modelos EDSR.
- **sentinel-project/models/**: Directorio para almacenar los pesos de los modelos.
- **sentinel-project/app.py**: Nueva sección de "Super-Resolución IA".
- **Entorno**: Se requiere la instalación de librerías de Deep Learning (ej. `opencv-contrib-python` para el módulo `dnn_superres` o similar).
