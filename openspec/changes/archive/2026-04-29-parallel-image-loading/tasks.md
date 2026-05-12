## 1. Implementación de Carga Concurrente

- [x] 1.1 Importar `ThreadPoolExecutor` desde `concurrent.futures` en `app.py`.
- [x] 1.2 En `app.py`, dentro de la función `_render_results`, antes de iterar para crear las columnas y tarjetas, agregar un bloque `with st.spinner("Descargando y procesando previsualizaciones en paralelo..."):`.
- [x] 1.3 Dentro del spinner, inicializar un `ThreadPoolExecutor` con `max_workers=5`.
- [x] 1.4 Utilizar `executor.map` (o submits iterativos) para ejecutar `_get_cached_preview` para todos los elementos en `result.items`, pasando los parámetros correspondientes (`item.item_id`, `preview_url`, `aoi_geom`, `item.bbox`). Solo invocar para aquellos items que tengan `rendered_preview`.
- [x] 1.5 Asegurar que los errores en los hilos (si los hay) no bloqueen silenciosamente el proceso, aunque la función actual ya captura y loguea excepciones.

## 2. Verificación

- [x] 2.1 Ejecutar la aplicación e iniciar una búsqueda temporal que retorne múltiples resultados (ej. > 5).
- [x] 2.2 Observar que el spinner de pre-carga aparece y se mantiene hasta que las imágenes son descargadas en paralelo.
- [x] 2.3 Validar que una vez que el spinner termina, la interfaz se dibuja inmediatamente y todas las tarjetas muestran su imagen correspondiente sin demoras perceptibles adicionales.
