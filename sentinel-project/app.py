"""
app.py  —  Sentinel Data Downloader
=====================================
Aplicación Streamlit principal para la búsqueda, visualización y descarga
de imágenes satelitales Sentinel-2 L2A desde Microsoft Planetary Computer.

UC-01: Búsqueda temporal y espacial de imágenes (RF-01)
UC-02: Previsualización con máscara AOI (RF-02)
UC-03: Selección de imágenes y cola de descarga (RF-03)
"""

import logging
import os
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import streamlit as st

from src.geo_utils import load_aoi
from src.search_controller import SearchResult, STACItem, search_images, validate_date_range, group_by_date
from src.preview_engine import get_masked_preview
from src.downloader import download_item_bands
from src.file_manager import get_output_dir, DEFAULT_BANDS, check_date_data_exists, get_data_root
from src.processor import process_all_grids
from src.super_resolution import process_super_res_batch

# ---------------------------------------------------------------------------
# Configuración de la aplicación
# ---------------------------------------------------------------------------

st.set_page_config(
    page_title="Sentinel Data Downloader",
    page_icon="🛰️",
    layout="wide",
    initial_sidebar_state="expanded",
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Ruta por defecto al archivo KML
DEFAULT_KML_PATH = str(Path(__file__).parent / "external" / "ARH_ETAPA.kml")

MESES = {
    1: "Enero", 2: "Febrero", 3: "Marzo", 4: "Abril",
    5: "Mayo", 6: "Junio", 7: "Julio", 8: "Agosto",
    9: "Septiembre", 10: "Octubre", 11: "Noviembre", 12: "Diciembre",
}


# ---------------------------------------------------------------------------
# Inicialización del estado de sesión
# ---------------------------------------------------------------------------

def _init_session():
    defaults = {
        "search_result": None,       # SearchResult | None
        "aoi_geom": None,            # GeoJSON dict | None
        "download_queue": {},        # dict[date_str -> list[STACItem]] — persistent across searches
        "selection_confirmed": False, # True after user confirms selection
        "grid_processed": False,     # True if crops/ folder is found or after processing
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value
    
    # Auto-load AOI at startup (Task 1.1)
    if st.session_state["aoi_geom"] is None:
        _load_aoi_cached(DEFAULT_KML_PATH)


def _reset_app_state():
    """Limpia el estado de la aplicación para permitir una nueva búsqueda limpia."""
    logger.info("Reiniciando estado de la aplicación...")
    st.session_state["search_result"] = None
    st.session_state["download_queue"] = {}
    st.session_state["selection_confirmed"] = False
    st.session_state["grid_processed"] = False
    # No limpiamos el AOI ya que suele ser el mismo para el proyecto


# ---------------------------------------------------------------------------
# Carga del AOI (KML)
# ---------------------------------------------------------------------------

def _load_aoi_cached(kml_path: str):
    """Carga el AOI desde el KML y cachea el resultado en session_state."""
    try:
        geom = load_aoi(kml_path)
        st.session_state["aoi_geom"] = geom
        return geom
    except FileNotFoundError:
        logger.error("Archivo KML no encontrado: %s", kml_path)
        st.session_state["aoi_geom"] = None
        return None
    except Exception as exc:  # noqa: BLE001
        logger.error("Error al leer el KML: %s", exc)
        st.session_state["aoi_geom"] = None
        return None


# ---------------------------------------------------------------------------
# Barra lateral (Task 3.1 + 4.2)
# ---------------------------------------------------------------------------

def render_sidebar() -> dict | None:
    """
    Renderiza la barra lateral con los controles de búsqueda.

    Returns:
        Diccionario con los parámetros de búsqueda si el usuario presionó
        'Buscar', o None si aún no se ha iniciado la búsqueda.
    """
    with st.sidebar:
        st.title("🛰️ Sentinel Data Downloader")
        st.caption("Descarga y procesa imágenes Sentinel-2 L2A")
        st.divider()

        # --- KML / AOI Indicator (Task 2.2) ---
        if st.session_state.get("aoi_geom"):
            geom_type = st.session_state["aoi_geom"].get("type", "?")
            st.success(f"✅ AOI cargado (**{geom_type}**)")
        else:
            st.error("⚠️ AOI no disponible. Verifique `external/ARH_MAP.kml`")

        st.divider()

        # --- Rango de fechas (Task 3.1) ---
        st.subheader("📅 Rango de Fechas")

        col_ini, col_fin = st.columns(2)

        with col_ini:
            st.markdown("**Inicio**")
            mes_inicio = st.selectbox(
                "Mes inicio",
                options=list(MESES.keys()),
                format_func=lambda m: MESES[m],
                index=0,
                key="mes_inicio",
                label_visibility="collapsed",
            )
            anio_inicio = st.number_input(
                "Año inicio",
                min_value=2015,
                max_value=2030,
                value=2025,
                step=1,
                key="anio_inicio",
                label_visibility="collapsed",
            )

        with col_fin:
            st.markdown("**Fin**")
            mes_fin = st.selectbox(
                "Mes fin",
                options=list(MESES.keys()),
                format_func=lambda m: MESES[m],
                index=2,
                key="mes_fin",
                label_visibility="collapsed",
            )
            anio_fin = st.number_input(
                "Año fin",
                min_value=2015,
                max_value=2030,
                value=2025,
                step=1,
                key="anio_fin",
                label_visibility="collapsed",
            )

        st.divider()

        # --- Botón de búsqueda (Task 3.2) ---
        buscar = st.button(
            "🔍 Buscar Imágenes",
            width="stretch",
            type="primary",
            key="btn_buscar",
        )

        if buscar:
            return {
                "mes_inicio": int(mes_inicio),
                "anio_inicio": int(anio_inicio),
                "mes_fin": int(mes_fin),
                "anio_fin": int(anio_fin),
            }

    return None


# ---------------------------------------------------------------------------
# Área principal
# ---------------------------------------------------------------------------

def render_main(search_params: dict | None):
    """Renderiza el contenido principal de la aplicación."""

    st.title("🛰️ Sentinel Data Downloader")
    st.markdown(
        "Busca, previsualiza y descarga imágenes satelitales **Sentinel-2 L2A** "
        "desde Microsoft Planetary Computer."
    )

    if search_params is None and st.session_state["search_result"] is None:
        # Estado inicial: instrucciones
        st.info(
            "👈 **Comience configurando el Área de Estudio y las fechas** en la "
            "barra lateral, luego presione **Buscar Imágenes**."
        )
        return

    # Hay parámetros de búsqueda nuevos → ejecutar búsqueda
    if search_params is not None:
        _run_search(search_params)

    # Mostrar resultados
    result: SearchResult | None = st.session_state["search_result"]
    if result is not None:
        _render_results(result)


def _run_search(params: dict):
    """
    Valida parámetros y ejecuta la búsqueda STAC. (Tasks 3.2 + 4.1 + 4.2)
    """
    # Task 4.2: Validar rango de fechas
    date_error = validate_date_range(
        params["mes_inicio"], params["anio_inicio"],
        params["mes_fin"], params["anio_fin"],
    )
    if date_error:
        st.error(f"⚠️ **Fechas inválidas:** {date_error}")
        return

    # Cargar AOI si no está en sesión (Task 3.1)
    aoi_geom = st.session_state.get("aoi_geom")
    if aoi_geom is None:
        aoi_geom = _load_aoi_cached(DEFAULT_KML_PATH)
        if aoi_geom is None:
            st.error("⚠️ **No se pudo cargar el AOI.**")
            st.info(f"Verifique que el archivo `{DEFAULT_KML_PATH}` existe.")
            return

    # Task 3.2 + Task 2.2: Ejecutar búsqueda con spinner
    with st.spinner("🔍 Consultando Microsoft Planetary Computer…"):
        result = search_images(
            mes_inicio=params["mes_inicio"],
            anio_inicio=params["anio_inicio"],
            mes_fin=params["mes_fin"],
            anio_fin=params["anio_fin"],
            geom_aoi=aoi_geom,
        )

    st.session_state["search_result"] = result
    st.session_state["grid_processed"] = False # Reset on new search (Task 1.3)
    # NOTE: download_queue is NOT cleared here — selections persist across searches (RF-03)


def _render_results(result: SearchResult):
    """
    Muestra los resultados de la búsqueda o mensajes de error/vacío.
    (Tasks 3.3 + 4.1)
    """
    # Task 4.1: Error de conexión
    if not result.success:
        st.error(result.error)
        st.markdown(
            "**Sugerencias:**\n"
            "- Verifique su conexión a internet.\n"
            "- Compruebe que el servicio MPC esté disponible.\n"
            "- Intente reducir el rango de fechas."
        )
        return

    # Task 3.3: Sin resultados
    if not result.has_results:
        st.warning(
            "🔍 **No se encontraron imágenes** para el rango de fechas y área "
            "especificados. Pruebe ajustando las fechas o el área de estudio."
        )
        return

    # Task 3.3: Mostrar resultados
    st.success(f"✅ **{result.total} imagen(es) encontrada(s)**")

    st.divider()
    st.subheader("📋 Galería de Imágenes")

    # --- Pre-carga de imágenes en paralelo (parallel-image-loading) ---
    aoi_geom = st.session_state.get("aoi_geom")
    grouped_items = group_by_date(result.items)
    # Filtrar fechas que tengan exactamente 3 tiles para evitar IndexError y asegurar cobertura (Task 1.1)
    dates = sorted([d for d, items in grouped_items.items() if len(items) == 3], reverse=True)

    if aoi_geom and dates:
        with st.spinner("Descargando y procesando previsualizaciones en paralelo..."):
            with ThreadPoolExecutor(max_workers=5) as executor:
                # Incluir todos los tiles de cada fecha para la previsualización (Task 1.1)
                items_to_load = []
                for d in dates:
                    day_items = grouped_items[d]
                    for it in day_items:
                        if it.assets.get("rendered_preview"):
                            items_to_load.append(it)

                # Pre-calentar la caché (pre-warm cache)
                list(executor.map(
                    lambda it: _get_cached_preview(it.item_id, it.assets["rendered_preview"], aoi_geom, it.bbox),
                    items_to_load
                ))

    # Lista vertical de fechas (Task 2.1)
    for d in dates:
        _render_date_section(d, grouped_items[d])

    # --- Resumen de Selección (UC-03: Tasks 2.1 + 2.2 + 2.3) ---
    st.divider()
    _render_selection_summary()


@st.cache_data(show_spinner="Renderizando previa...")
def _get_cached_preview(item_id: str, preview_url: str, aoi_geom: dict, bbox: list[float]):
    """Wrapper para cachear la generación de previas con contorno."""
    return get_masked_preview(preview_url, aoi_geom, bbox)


def _render_date_section(date_str: str, items: list[STACItem]):
    """Renderiza una sección por fecha mostrando sus tres tiles (Task 2.2, 2.3, 2.4)."""
    with st.container(border=True):
        # 1. Cabecera con Selección
        col_title, col_check = st.columns([3, 1])
        with col_title:
            avg_clouds = sum(it.cloud_cover for it in items) / len(items)
            cloud_color = "green" if avg_clouds < 10 else "orange" if avg_clouds < 30 else "red"
            st.markdown(f"### 📅 Fecha: `{date_str}` (☁️ {avg_clouds:.1f}%)")
        
        with col_check:
            queue = st.session_state["download_queue"]
            is_selected = date_str in queue
            if st.checkbox("Seleccionar Fecha", key=f"sel_{date_str}", value=is_selected):
                if date_str not in queue:
                    queue[date_str] = items
            else:
                queue.pop(date_str, None)

        # 2. Visualización de los 3 Tiles (Task 2.3)
        cols = st.columns(3)
        # Ordenar tiles para consistencia (ej: MPS, MQT, MQS)
        sorted_items = sorted(items, key=lambda it: it.item_id.split("_")[-1])
        
        for i, it in enumerate(sorted_items):
            with cols[i]:
                tile_id = it.item_id.split("_")[-1]
                preview_url = it.assets.get("rendered_preview")
                
                if preview_url and st.session_state["aoi_geom"]:
                    img = _get_cached_preview(it.item_id, preview_url, st.session_state["aoi_geom"], it.bbox)
                    if img:
                        st.image(img, width="stretch", caption=f"Tile: {tile_id}")
                    else:
                        st.warning(f"⚠️ Previa {tile_id} no disponible")
                else:
                    st.info(f"ℹ️ Sin asset para {tile_id}")
                
                # Metadatos del tile (Task 2.4)
                cloud_val = it.cloud_cover
                c_color = "green" if cloud_val < 10 else "orange" if cloud_val < 30 else "red"
                st.markdown(f"**{tile_id}**: :{c_color}[☁️ {cloud_val:.1f}%]")


# ---------------------------------------------------------------------------
# Resumen de selección y confirmación (UC-03)
# ---------------------------------------------------------------------------

def _check_if_crops_exist():
    """Verifica si existen recortes en disco para habilitar SR (Task 2.1)."""
    sentinel_data_path = get_data_root()
    if sentinel_data_path.exists():
        has_crops = any(sentinel_data_path.rglob("crops/*.png"))
        if has_crops:
            st.session_state["grid_processed"] = True
        return has_crops
    return False


def _render_selection_summary():
    """Muestra el resumen de fechas seleccionadas y el botón de confirmación."""
    queue = st.session_state["download_queue"]
    count_dates = len(queue)
    total_tiles = sum(len(items) for items in queue.values())

    st.subheader("📦 Cola de Descarga")

    if count_dates == 0:
        st.info(
            "💡 **Seleccione fechas** de la galería marcando los checkboxes. "
            "Se descargarán automáticamente los 3 tiles correspondientes por cada día."
        )
        return

    # Feedback visual
    st.success(f"📌 **{count_dates} fecha(s)** seleccionada(s) (Total: **{total_tiles} tiles**)")

    with st.expander("Ver detalle de fechas", expanded=False):
        for date_str, items in list(queue.items()):
            col_date, col_tiles, col_cloud, col_rm = st.columns([3, 2, 2, 1])
            with col_date:
                st.markdown(f"📅 **{date_str}**")
            with col_tiles:
                st.text(f"Tiles: {len(items)}")
            with col_cloud:
                avg_clouds = sum(it.cloud_cover for it in items) / len(items)
                st.text(f"☁️ Prom: {avg_clouds:.0f}%")
            with col_rm:
                if st.button("❌", key=f"rm_{date_str}", help="Quitar fecha"):
                    queue.pop(date_str, None)
                    st.rerun()

    # Botón de confirmación (Task 2.2)
    st.divider()
    col_confirm, col_clear = st.columns([3, 1])
    with col_confirm:
        if st.button(
            f"✅ Confirmar Selección ({total_tiles} tiles en {count_dates} días)",
            width="stretch",
            type="primary",
            key="btn_confirmar_seleccion",
        ):
            st.session_state["selection_confirmed"] = True
            st.success(
                f"✅ **Selección confirmada.** {total_tiles} tiles listos para descarga. "
            )

    # --- Ejecución de Descarga (UC-04: Tasks 3.1 + 3.2 + 3.3) ---
    if st.session_state.get("selection_confirmed") and count_dates > 0:
        st.divider()
        st.subheader("🚀 Ejecutar Descarga")
        st.info("Se descargarán las bandas: " + ", ".join(DEFAULT_BANDS))
        
        if st.button("📥 Iniciar Procesamiento y Descarga", width="stretch", type="primary"):
            _run_download_process(queue)

            st.session_state["selection_confirmed"] = False
            st.rerun()

    # --- Procesamiento de Cuadrícula (UC-05: Tasks 3.1 + 3.2 + 3.3) ---
    # Solo si hay archivos en Data_Sentinel
    sentinel_data_path = get_data_root()
    if sentinel_data_path.exists() and any(sentinel_data_path.rglob("*.tif")):
        st.divider()
        st.subheader("🤖 Preparación para IA (Recortes y Filtrado)")
        st.info(
            "Este proceso fragmentará las imágenes descargadas en la cuadrícula del proyecto, "
            "descartando áreas con nubes y convirtiendo los resultados a PNG RGB de 8 bits."
        )
        
        col_proc, col_clean = st.columns([2, 1])
        with col_proc:
            do_cleanup = st.checkbox("Limpiar archivos .tif temporales al finalizar", value=True)
            if st.button("🏗️ Generar Recortes Limpios", width="stretch"):
                _run_grid_processing(do_cleanup)
                st.rerun()

    # --- Super-Resolución IA (UC-06: Tasks 3.1 + 3.2 + 3.3) ---
    # Task 2.2 + 2.3: Solo mostrar si la cuadrícula ha sido procesada
    _check_if_crops_exist()
    
    if st.session_state.get("grid_processed"):
        st.divider()
        st.subheader("✨ Super-Resolución IA (EDSR x8)")
        st.info(
            "Este proceso aplica modelos de Deep Learning para aumentar la resolución "
            "de los recortes de 128x128 a 1024x1024 píxeles."
        )
        
        if st.button("🚀 Iniciar Super-Resolución", width="stretch", type="primary"):
            _run_super_res_process()
    elif sentinel_data_path.exists() and any(sentinel_data_path.rglob("*.tif")):
        # Mostrar mensaje guía si hay datos pero no han sido procesados (Task 2.3)
        st.divider()
        st.subheader("✨ Super-Resolución IA")
        st.info("💡 **Paso previo requerido:** Debe generar los recortes limpios en la sección superior antes de iniciar el aumento de resolución.")


def _run_download_process(queue: dict):
    """Ejecuta el proceso de descarga con barra de progreso."""
    count_dates = len(queue)
    total_tiles = sum(len(items) for items in queue.values())
    total_bands_overall = total_tiles * len(DEFAULT_BANDS)
    
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    # Directorio base de descarga
    base_dir = get_data_root()
    downloaded_files = []
    
    # AOI detallado para el recorte
    mask_geom = st.session_state.get("aoi_geom")
    
    current_band_count = 0
    
    for date_idx, (date_str, items) in enumerate(queue.items()):
        # Parsear fecha
        y, m, d = map(int, date_str.split("-"))
        
        # Validar si ya existen los datos para esta fecha
        if check_date_data_exists(str(base_dir), y, m, d, items, DEFAULT_BANDS, date_str):
            status_text.info(f"⏭️ Omitiendo fecha `{date_str}`: Datos ya existentes localmente.")
            # Actualizar progreso para las bandas omitidas
            current_band_count += len(items) * len(DEFAULT_BANDS)
            progress_bar.progress(min(current_band_count / total_bands_overall, 1.0))
            continue

        # Crear directorio de salida una sola vez por fecha
        output_dir = get_output_dir(base_dir, y, m, d)
        
        for tile_idx, item in enumerate(items):
            status_text.markdown(f"📦 Fecha {date_idx+1}/{count_dates} | Tile {tile_idx+1}/{len(items)}: `{item.item_id[:20]}...`")
            
            # Callback para progreso interno de bandas
            def _update_band_progress(b_idx, b_total, b_name):
                nonlocal current_band_count
                current_band_count += 1
                progress_bar.progress(min(current_band_count / total_bands_overall, 1.0))
                status_text.markdown(f"⏳ Descargando banda **{b_name}** para `{item.item_id[:20]}`")

            results = download_item_bands(
                item=item,
                bands=DEFAULT_BANDS,
                geom=mask_geom,
                output_dir=output_dir,
                date_str=date_str,
                progress_callback=_update_band_progress
            )
            
            if results:
                downloaded_files.extend(results)
            else:
                st.error(f"❌ No se pudo descargar ninguna banda para el tile `{item.item_id}`.")
        
    progress_bar.progress(1.0)
    status_text.success(f"✅ **Descarga completada con éxito.**")
    st.balloons()
    
    st.write(f"📂 Archivos guardados en: `{os.path.abspath(base_dir)}`")
    with st.expander("Ver lista de archivos"):
        for f in downloaded_files:
            st.code(f)


def _run_grid_processing(delete_originals: bool):
    """Ejecuta el procesamiento de la cuadrícula con logs en tiempo real."""
    grid_path = Path(__file__).parent / "external" / "cuadricula_arh.geojson"
    if not grid_path.exists():
        st.error(f"❌ No se encontró la cuadrícula en: `{grid_path}`")
        return

    base_dir = get_data_root()
    # Buscar carpetas de días (YYYY/MM/DD) que tengan .tif pendientes
    all_date_dirs = [d for d in base_dir.rglob("*") if d.is_dir() and any(d.glob("*.tif"))]
    all_date_dirs.pop("DC_Layers")

    # Filtrar fechas que ya fueron procesadas (tienen crops/*.png en disco)
    date_dirs = [d for d in all_date_dirs if not any((d / "super_res").glob("*.png"))]
    already_done = len(all_date_dirs) - len(date_dirs)

    if already_done > 0:
        st.info(f"⏭️ Se omiten **{already_done} fecha(s)** ya procesadas (tienen recortes en disco).")

    if not date_dirs:
        st.success("✅ Todas las fechas descargadas ya han sido procesadas.")
        st.session_state["grid_processed"] = True
        return

    st.write(f"🔍 Encontradas **{len(date_dirs)} fecha(s) nuevas** para procesar.")
    
    overall_stats = {"saved": 0, "skipped": 0, "dedup_skipped": 0}
    
    for ddir in date_dirs:
        with st.status(f"⚡ Procesando fecha: `{ddir.relative_to(base_dir)}`", expanded=True) as status:
            st.write("Cargando bandas y aplicando filtros...")
            res = process_all_grids(ddir, grid_path, delete_originals)
            
            if "error" in res:
                st.error(res["error"])
                continue
                
            st.write(
                f"✅ Guardados: **{res['saved']}** | "
                f"☁️ Omitidos: **{res['skipped']}** | "
                f"🔁 Deduplicados: **{res.get('dedup_skipped', 0)}**"
            )
            overall_stats["saved"] += res["saved"]
            overall_stats["skipped"] += res["skipped"]
            overall_stats["dedup_skipped"] += res.get("dedup_skipped", 0)
            status.update(label=f"✅ Fecha completada: {ddir.name}", state="complete")

    st.session_state["grid_processed"] = True # Task 1.2

    st.divider()
    st.success(
        f"🎯 **Procesamiento finalizado.**\n"
        f"- Total recortes generados: **{overall_stats['saved']}**\n"
        f"- Total áreas nubladas descartadas: **{overall_stats['skipped']}**\n"
        f"- Total celdas deduplicadas (borde/existente): **{overall_stats['dedup_skipped']}**"
    )
    
    if delete_originals:
        st.info("🧹 Los archivos temporales `.tif` han sido eliminados para ahorrar espacio.")


def _run_super_res_process():
    """Ejecuta el escalado IA con feedback visual."""
    base_dir = get_data_root()
    crops_dirs = [d for d in base_dir.rglob("crops") if d.is_dir() and any(d.glob("*.png"))]
    
    if not crops_dirs:
        st.warning("⚠️ No se encontraron carpetas `crops/` con imágenes para escalar.")
        return

    progress_bar = st.progress(0)
    status_text = st.empty()
    
    last_processed = None
    
    for cdir in crops_dirs:
        def _update_sr_progress(current, total, name):
            progress_bar.progress(current / total)
            status_text.markdown(f"🧠 Escalando: `{name}` ({current}/{total})")

        res = process_super_res_batch(cdir, progress_callback=_update_sr_progress)
        
        if "error" in res:
            st.error(res["error"])
            continue
        
        # Guardar una referencia para la comparativa
        sr_files = list((cdir.parent / "super_res").glob("*_SR.png"))
        if sr_files:
            last_processed = sr_files[-1]

    progress_bar.progress(1.0)
    status_text.success("✅ **Proceso de Super-Resolución completado.**")
    st.balloons()
    
    # Reiniciar estado para permitir nuevo proceso (Task 3.2)
    _reset_app_state()
    
    # --- Galería de Comparación (Task 3.3) ---
    # if last_processed:
    #     st.divider()
    #     st.subheader("🔍 Comparativa Antes vs Después")
    #     original_path = Path(str(last_processed).replace("_SR.png", ".png").replace("super_res", "crops"))
        
    #     col_orig, col_sr = st.columns(2)
    #     with col_orig:
    #         st.image(str(original_path), caption="Original (128x128)", width="stretch")
    #     with col_sr:
    #         st.image(str(last_processed), caption="Super-Resolución (1024x1024)", width="stretch")


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def main():
    _init_session()
    search_params = render_sidebar()
    render_main(search_params)


if __name__ == "__main__":
    main()