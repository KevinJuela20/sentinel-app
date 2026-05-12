## 1. Carga automática del AOI

- [x] 1.1 Modificar `_init_session()` en `app.py` para que cargue automáticamente el AOI llamando a `_load_aoi_cached(DEFAULT_KML_PATH)` cuando `aoi_geom` no esté en el session_state
- [x] 1.2 Eliminar la clave `kml_error` del session_state si ya no se usa como estado independiente (integrar el manejo de error en el indicador de la barra lateral)

## 2. Simplificar la barra lateral

- [x] 2.1 Eliminar la sección "📍 Área de Estudio" completa de `render_sidebar()`: el `st.text_input` para la ruta KML, el `st.button("📂 Cargar AOI")`, y los bloques de mensajes `st.error`/`st.success` asociados
- [x] 2.2 Agregar un indicador discreto del estado del AOI en la barra lateral (e.g., `st.caption("✅ AOI cargado")` o `st.error("⚠️ AOI no disponible")`) que refleje el estado de `session_state["aoi_geom"]`
- [x] 2.3 Eliminar la clave `kml_path` del diccionario de retorno de `render_sidebar()` (ya no se necesita)

## 3. Simplificar _run_search

- [x] 3.1 Modificar `_run_search()` para que ya no use `params["kml_path"]` al intentar cargar el AOI como fallback — en su lugar usar `DEFAULT_KML_PATH` directamente si `aoi_geom` es None

## 4. Verificación

- [x] 4.1 Ejecutar la suite de tests existente (`python -m pytest tests/`) y verificar que todos los tests pasan
- [x] 4.2 Verificar manualmente en la UI de Streamlit que el AOI se carga automáticamente al abrir la aplicación y que la sección de carga KML ya no aparece en la barra lateral
