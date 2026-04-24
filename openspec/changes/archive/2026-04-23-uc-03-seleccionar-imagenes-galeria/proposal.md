## Why

Para cumplir con el flujo de trabajo de descarga optimizada, el usuario debe poder filtrar y seleccionar manualmente qué imágenes satelitales son aptas (p. ej. libres de nubes o con el ángulo correcto) antes de proceder a la descarga masiva. Esta funcionalidad permite consolidar una "Cola de Descarga" persistente a través de múltiples búsquedas.

## What Changes

- **Selección Persistente**: Gestión del estado de selección en `st.session_state` para que las imágenes seleccionadas se mantengan al cambiar de parámetros de búsqueda.
- **Botón de Confirmación**: Incorporación de un botón de acción para consolidar la selección.
- **Validación de Selección**: Lógica para asegurar que al menos una imagen ha sido marcada antes de permitir el avance a la fase de descarga.
- **Cola de Descarga**: Estructura de datos interna que almacena los `item_id` y metadatos necesarios para UC-04.

## Capabilities

### New Capabilities
- Ninguna (implementación de capacidad base definida en UC-03).

### Modified Capabilities
- `uc-03-seleccionar-imagenes-galeria`: Implementación de los requisitos funcionales RF-03 detallados en el baseline spec.

## Impact

- **app.py**: Actualización de la lógica de renderizado de la galería y gestión de estados.
- **src/search_controller.py**: Podría requerir una estructura de datos para la cola si se decide separar la lógica de persistencia.
- **Interoperabilidad**: Este cambio es el puente obligatorio entre la visualización (UC-02) y la descarga (UC-04).
