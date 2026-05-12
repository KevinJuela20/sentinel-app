## Why

Actualmente, cada vez que se inicia la aplicación Streamlit, el usuario debe presionar manualmente el botón "Cargar AOI" en la barra lateral para cargar el archivo KML del Área de Estudio. Esto es un paso innecesario y repetitivo, ya que el archivo KML (`ARH_ETAPA.kml`) está fijo dentro del proyecto en `external/` y no cambia entre sesiones. El AOI debería cargarse automáticamente al iniciar la aplicación, eliminando fricción en el flujo de trabajo diario del analista.

Este cambio impacta directamente a UC-01 (RF-01), ya que la carga del AOI es un prerequisito para cualquier búsqueda.

## What Changes

- **Eliminar** la sección "📍 Área de Estudio" de la barra lateral (text input para la ruta KML + botón "Cargar AOI" + mensajes de estado).
- **Cargar automáticamente** el AOI desde `DEFAULT_KML_PATH` durante la inicialización de la sesión (`_init_session()`), sin intervención del usuario.
- **Simplificar** `_run_search()` para que no necesite recibir ni usar `kml_path` como parámetro — el AOI siempre estará pre-cargado.
- **Mostrar** un indicador discreto en la barra lateral confirmando que el AOI está cargado (o un error si falla).
- **Eliminar** la clave `kml_error` del session_state si ya no es necesaria como estado separado.

## Capabilities

### New Capabilities

_(Ninguna — es una simplificación del flujo existente)_

### Modified Capabilities

- `UC-01-buscar-imagenes-fecha-area`: El requisito de carga del AOI cambia de interacción manual del usuario a carga automática al inicio. Se elimina la UI de carga KML de la barra lateral.

## Impact

- **Código afectado**: `app.py` (funciones `_init_session`, `render_sidebar`, `_run_search`, `_load_aoi_cached`)
- **UI**: Se elimina la sección "Área de Estudio" de la barra lateral (text input, botón, mensajes)
- **APIs**: Sin cambios en `src/geo_utils.py` ni `src/search_controller.py`
- **Dependencias**: Ninguna nueva
- **UC afectados**: UC-01 (directamente), UC-02/UC-03/UC-04 (indirectamente — dependen del AOI cargado)
- **Trazabilidad**: RF-01 → UC-01 → Barra Lateral + Parser KML (SDD sección 5.1, 6.1)
