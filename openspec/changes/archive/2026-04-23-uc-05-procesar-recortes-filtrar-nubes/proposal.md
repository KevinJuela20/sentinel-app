## Why

El objetivo final de este sistema es alimentar modelos de Inteligencia Artificial con datos satelitales de alta calidad. Este cambio implementa el filtrado riguroso por nubosidad (usando la máscara SCL) y la fragmentación de las imágenes descargadas en recortes individuales basados en la cuadrícula de trabajo. Esto asegura que solo las áreas 100% útiles lleguen a la etapa de análisis, optimizando el entrenamiento y la inferencia de modelos posteriores.

## What Changes

- **Motor de Procesamiento por Cuadrícula**: Lógica para iterar sobre los polígonos de `Cuadrícula_ARH.geojson` y extraer recortes locales de las bandas descargadas en UC-04.
- **Filtro de Nubes (SCL Filter)**: Algoritmo que analiza la banda Scene Classification Layer (SCL) y descarta automáticamente recortes con presencia de nubes, sombras o artefactos por encima del 5%.
- **Generador de PNG RGB**: Conversión de las bandas multiespectrales (B04, B03, B02) a imágenes compuestas en formato PNG de 8 bits, listas para consumo por modelos de visión computacional.
- **Gestión de Temporales**: Implementación de limpieza automática de archivos GeoTIFF tras la generación exitosa de los recortes PNG para ahorrar espacio en disco.

## Capabilities

### New Capabilities
- Ninguna (implementación de capacidad base definida en UC-05).

### Modified Capabilities
- `uc-05-procesar-recortes-filtrar-nubes`: Implementación de los requisitos funcionales RF-05 y RF-07 detallados en el baseline spec.

## Impact

- **sentinel-project/src/processor.py**: Nuevo módulo para la fragmentación y filtrado.
- **sentinel-project/src/image_utils.py**: Utilidades para conversión de ráster a PNG RGB.
- **sentinel-project/app.py**: Nueva pestaña o sección de "Procesamiento de Cuadrícula".
- **Dependencias**: Se utilizará el entorno local (`pip`) para las pruebas, evitando `conda` como se solicitó.
