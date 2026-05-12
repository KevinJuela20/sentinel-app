## Context

En el sistema actual (`app.py`), los resultados de la búsqueda STAC se muestran en una galería usando `st.columns`. Durante el renderizado, para cada item de la galería se llama secuencialmente a `_get_cached_preview` (que a su vez descarga la imagen del MPC Tiler y procesa la superposición del contorno AOI). Como la descarga de cada imagen requiere una petición HTTP, el tiempo de carga total crece linealmente con la cantidad de resultados encontrados (Ej: 10 resultados = 10 peticiones secuenciales), bloqueando la UI de Streamlit mientras se procesa.

## Goals / Non-Goals

**Goals:**
- Reducir significativamente el tiempo percibido para renderizar la galería de previsualizaciones.
- Ejecutar la obtención y procesamiento I/O-bound (descarga + PIL mapping) de manera concurrente.
- Proveer retroalimentación visual al usuario mientras las imágenes se están descargando.

**Non-Goals:**
- No se modificará el mecanismo base de la caché (`st.cache_data`).
- No se cambiará la lógica geométrica para dibujar el contorno (se reutiliza el trabajo previo).
- No se implementará "lazy loading" infinito (se pre-cargarán todos los resultados devueltos por la búsqueda actual, que típicamente son manejables).

## Decisions

**1. Uso de `concurrent.futures.ThreadPoolExecutor` para pre-calentamiento (Pre-warming) de la Caché**
- *Rationale*: En Streamlit, interactuar con elementos visuales de la UI (como `st.image` o `st.progress`) desde múltiples hilos es propenso a errores y race conditions. Sin embargo, llamar a una función decorada con `@st.cache_data` desde un ThreadPool es seguro, ya que Streamlit maneja la concurrencia interna de su sistema de caché.
- *Implementación*: Antes del bucle principal de renderizado de la galería (en `_render_results`), iteraremos sobre todos los `result.items` usando `ThreadPoolExecutor.map` para invocar `_get_cached_preview`.
- *Resultado esperado*: Las descargas ocurrirán en paralelo. Cuando finalice el ThreadPool, el bucle secuencial que dibuja la UI encontrará todas las imágenes ya en caché y las renderizará casi instantáneamente.

**2. Retroalimentación Visual (UX)**
- *Rationale*: Las peticiones en paralelo aún toman algo de tiempo. Para evitar que la app parezca "congelada", se usará un bloque `with st.spinner("Descargando previsualizaciones...")` envolviendo la ejecución del `ThreadPoolExecutor`.

## Risks / Trade-offs

- **[Risk] Limitaciones de red y Rate Limiting de MPC**: Hacer 20 peticiones HTTP concurrentes podría disparar el rate-limiting del servidor de Microsoft Planetary Computer o saturar el ancho de banda del usuario.
  - *Mitigación*: Se configurará `max_workers` en el `ThreadPoolExecutor` a un valor conservador (e.g., `5` o `10`) para equilibrar velocidad y respeto a los límites de la API.
- **[Risk] Thread Safety en funciones de Streamlit**: Invocar APIs exclusivas de renderizado de Streamlit desde hilos paralelos puede causar crashes (MissingScriptRunContext).
  - *Mitigación*: El ThreadPool **solo** llamará a `_get_cached_preview`, que es una función pura decorada con `@st.cache_data` (sin llamadas a `st.write` o `st.image`). La UI seguirá renderizándose en el hilo principal.
