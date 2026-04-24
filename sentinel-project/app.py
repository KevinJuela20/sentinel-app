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
from pathlib import Path

import streamlit as st

from src.geo_utils import load_aoi
from src.search_controller import SearchResult, STACItem, search_images, validate_date_range
from src.preview_engine import get_masked_preview
from src.downloader import download_item_bands
from src.file_manager import get_output_dir, DEFAULT_BANDS
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
        "kml_error": None,           # str | None
        "download_queue": {},        # dict[item_id -> STACItem]  — persistent across searches
        "selection_confirmed": False, # True after user confirms selection
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


# ---------------------------------------------------------------------------
# Carga del AOI (KML)
# ---------------------------------------------------------------------------

def _load_aoi_cached(kml_path: str):
    """Carga el AOI desde el KML y cachea el resultado en session_state."""
    try:
        geom = load_aoi(kml_path)
        st.session_state["aoi_geom"] = geom
        st.session_state["kml_error"] = None
        return geom
    except FileNotFoundError:
        msg = f"Archivo KML no encontrado: `{kml_path}`"
        st.session_state["kml_error"] = msg
        st.session_state["aoi_geom"] = None
        return None
    except Exception as exc:  # noqa: BLE001
        msg = f"Error al leer el KML: {exc}"
        st.session_state["kml_error"] = msg
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

        # --- KML / AOI ---
        st.subheader("📍 Área de Estudio")

        kml_path = st.text_input(
            "Ruta al archivo KML",
            value=DEFAULT_KML_PATH,
            help="Archivo KML que define el Área de Interés (AOI).",
            key="kml_path_input",
        )

        if st.button("📂 Cargar AOI", use_container_width=True, key="btn_load_aoi"):
            with st.spinner("Cargando AOI…"):
                _load_aoi_cached(kml_path)

        if st.session_state["kml_error"]:
            st.error(st.session_state["kml_error"])
        elif st.session_state["aoi_geom"]:
            geom_type = st.session_state["aoi_geom"].get("type", "?")
            st.success(f"✅ AOI cargado — tipo: **{geom_type}**")

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
            use_container_width=True,
            type="primary",
            key="btn_buscar",
        )

        if buscar:
            return {
                "mes_inicio": int(mes_inicio),
                "anio_inicio": int(anio_inicio),
                "mes_fin": int(mes_fin),
                "anio_fin": int(anio_fin),
                "kml_path": kml_path,
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

    # Cargar AOI si no está en sesión
    aoi_geom = st.session_state.get("aoi_geom")
    if aoi_geom is None:
        aoi_geom = _load_aoi_cached(params["kml_path"])
        if aoi_geom is None:
            err_msg = st.session_state.get("kml_error", "Error desconocido")
            st.error(f"⚠️ **No se pudo cargar el AOI:** {err_msg}")
            st.info("Verifique la ruta al archivo KML en la barra lateral.")
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

    # Contenedor para la galería
    grid_cols = 3
    rows = [result.items[i : i + grid_cols] for i in range(0, len(result.items), grid_cols)]

    for row in rows:
        cols = st.columns(grid_cols)
        for i, item in enumerate(row):
            with cols[i]:
                _render_item_card(item)

    # --- Resumen de Selección (UC-03: Tasks 2.1 + 2.2 + 2.3) ---
    st.divider()
    _render_selection_summary()


@st.cache_data(show_spinner="Renderizando previa...")
def _get_cached_preview(item_id: str, preview_url: str, aoi_geom: dict):
    """Wrapper para cachear la generación de previas recortadas."""
    return get_masked_preview(preview_url, aoi_geom)


def _render_item_card(item: STACItem):
    """Renderiza una card individual para un item STAC."""
    # Contenedor con borde (simulado con div)
    with st.container(border=True):
        # 1. Imagen recortada
        preview_url = item.assets.get("rendered_preview")
        if preview_url and st.session_state["aoi_geom"]:
            img = _get_cached_preview(item.item_id, preview_url, st.session_state["aoi_geom"])
            if img:
                st.image(img, use_container_width=True)
            else:
                st.warning("⚠️ Previa no disponible")
        else:
            st.info("ℹ️ Sin asset de previsualización")

        # 2. Metadatos
        col_meta1, col_meta2 = st.columns([2, 1])
        with col_meta1:
            st.markdown(f"**Fecha:** `{item.datetime[:10]}`")
            st.caption(f"ID: {item.item_id[:15]}...")
        with col_meta2:
            # Color de nubes
            cloud_color = "green" if item.cloud_cover < 10 else "orange" if item.cloud_cover < 30 else "red"
            st.markdown(f":{cloud_color}[☁️ {item.cloud_cover:.1f}%]")

        # 3. Selección — lee/escribe en download_queue (UC-03 Task 1.2)
        queue = st.session_state["download_queue"]
        is_selected = item.item_id in queue
        if st.checkbox("Seleccionar", key=f"sel_{item.item_id}", value=is_selected):
            if item.item_id not in queue:
                queue[item.item_id] = item
        else:
            queue.pop(item.item_id, None)


# ---------------------------------------------------------------------------
# Resumen de selección y confirmación (UC-03)
# ---------------------------------------------------------------------------

def _render_selection_summary():
    """Muestra el resumen de imágenes seleccionadas y el botón de confirmación."""
    queue = st.session_state["download_queue"]
    count = len(queue)

    st.subheader("📦 Cola de Descarga")

    if count == 0:
        st.info(
            "💡 **Seleccione imágenes** de la galería marcando los checkboxes. "
            "Las selecciones se mantienen aunque cambie de búsqueda."
        )
        return

    # Feedback visual: chips con los IDs seleccionados (Task 2.3)
    st.success(f"📌 **{count} imagen(es) en la cola de descarga**")

    with st.expander("Ver imágenes seleccionadas", expanded=False):
        for item_id, item in list(queue.items()):
            col_id, col_date, col_cloud, col_rm = st.columns([3, 2, 1, 1])
            with col_id:
                st.text(item.item_id[:25])
            with col_date:
                st.text(item.datetime[:10] if item.datetime else "—")
            with col_cloud:
                st.text(f"☁️ {item.cloud_cover:.0f}%")
            with col_rm:
                if st.button("❌", key=f"rm_{item_id}", help="Quitar de la cola"):
                    queue.pop(item_id, None)
                    st.rerun()

    # Botón de confirmación (Task 2.2)
    st.divider()
    col_confirm, col_clear = st.columns([3, 1])
    with col_confirm:
        if st.button(
            f"✅ Confirmar Selección ({count} imágenes)",
            use_container_width=True,
            type="primary",
            key="btn_confirmar_seleccion",
        ):
            if count == 0:
                st.error("⚠️ Debe seleccionar al menos una imagen antes de confirmar.")
            else:
                st.session_state["selection_confirmed"] = True
                st.success(
                    f"✅ **Selección confirmada.** {count} imagen(es) listas para descarga. "
                )

    # --- Ejecución de Descarga (UC-04: Tasks 3.1 + 3.2 + 3.3) ---
    if st.session_state.get("selection_confirmed") and count > 0:
        st.divider()
        st.subheader("🚀 Ejecutar Descarga")
        st.info("Se descargarán las bandas: " + ", ".join(DEFAULT_BANDS))
        
        if st.button("📥 Iniciar Procesamiento y Descarga", use_container_width=True, type="primary"):
            _run_download_process(queue)

            st.session_state["selection_confirmed"] = False
            st.rerun()

    # --- Procesamiento de Cuadrícula (UC-05: Tasks 3.1 + 3.2 + 3.3) ---
    # Solo si hay archivos en Data_Sentinel
    sentinel_data_path = Path(__file__).parent / "Data_Sentinel"
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
            if st.button("🏗️ Generar Recortes Limpios", use_container_width=True):
                _run_grid_processing(do_cleanup)

    # --- Super-Resolución IA (UC-06: Tasks 3.1 + 3.2 + 3.3) ---
    if os.path.exists("Data_Sentinel") and any(Path("Data_Sentinel").rglob("crops/*.png")):
        st.divider()
        st.subheader("✨ Super-Resolución IA (EDSR x8)")
        st.info(
            "Este proceso aplica modelos de Deep Learning para aumentar la resolución "
            "de los recortes de 128x128 a 1024x1024 píxeles."
        )
        
        if st.button("🚀 Iniciar Super-Resolución", use_container_width=True, type="primary"):
            _run_super_res_process()


def _run_download_process(queue: dict):
    """Ejecuta el proceso de descarga con barra de progreso."""
    total_items = len(queue)
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    # Directorio base de descarga
    base_dir = Path(__file__).parent / "Data_Sentinel"
    downloaded_files = []
    
    # AOI detallado para el recorte (preferir Cuadrícula_ARH si existe)
    # Por ahora usamos el aoi_geom cargado del KML
    mask_geom = st.session_state.get("aoi_geom")
    
    for idx, (item_id, item) in enumerate(queue.items()):
        # Parsear fecha
        dt = item.datetime[:10]  # YYYY-MM-DD
        y, m, d = map(int, dt.split("-"))
        
        status_text.markdown(f"📦 Procesando item {idx+1}/{total_items}: `{item_id[:20]}...`")
        
        # Crear directorio de salida
        output_dir = get_output_dir(base_dir, y, m, d)
        
        # Callback para progreso interno de bandas
        def _update_band_progress(b_idx, b_total, b_name):
            sub_prog = (idx / total_items) + (b_idx / b_total / total_items)
            progress_bar.progress(sub_prog)
            status_text.markdown(f"⏳ Descargando banda **{b_name}** ({b_idx}/{b_total}) para `{item_id[:20]}`")

        results = download_item_bands(
            item=item,
            bands=DEFAULT_BANDS,
            geom=mask_geom,
            output_dir=output_dir,
            date_str=dt,
            progress_callback=_update_band_progress
        )
        
        if results:
            downloaded_files.extend(results)
        else:
            st.error(f"❌ No se pudo descargar ninguna banda para el item `{item_id}`. Verifique su conexión y permisos.")
        
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

    base_dir = Path(__file__).parent / "Data_Sentinel"
    # Buscar carpetas de días (YYYY/MM/DD)
    date_dirs = [d for d in base_dir.rglob("*") if d.is_dir() and any(d.glob("*.tif"))]
    
    if not date_dirs:
        st.warning("⚠️ No se encontraron carpetas con archivos `.tif` para procesar.")
        return

    st.write(f"🔍 Encontradas **{len(date_dirs)} fechas** para procesar.")
    
    overall_stats = {"saved": 0, "skipped": 0}
    
    for ddir in date_dirs:
        with st.status(f"⚡ Procesando fecha: `{ddir.relative_to(base_dir)}`", expanded=True) as status:
            st.write("Cargando bandas y aplicando filtros...")
            res = process_all_grids(ddir, grid_path, delete_originals)
            
            if "error" in res:
                st.error(res["error"])
                continue
                
            st.write(f"✅ Guardados: **{res['saved']}** | ☁️ Omitidos: **{res['skipped']}**")
            overall_stats["saved"] += res["saved"]
            overall_stats["skipped"] += res["skipped"]
            status.update(label=f"✅ Fecha completada: {ddir.name}", state="complete")

    st.divider()
    st.success(
        f"🎯 **Procesamiento finalizado.**\n"
        f"- Total recortes generados: **{overall_stats['saved']}**\n"
        f"- Total áreas nubladas descartadas: **{overall_stats['skipped']}**"
    )
    
    if delete_originals:
        st.info("🧹 Los archivos temporales `.tif` han sido eliminados para ahorrar espacio.")


def _run_super_res_process():
    """Ejecuta el escalado IA con feedback visual."""
    base_dir = Path(__file__).parent / "Data_Sentinel"
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
    
    # --- Galería de Comparación (Task 3.3) ---
    if last_processed:
        st.divider()
        st.subheader("🔍 Comparativa Antes vs Después")
        original_path = Path(str(last_processed).replace("_SR.png", ".png").replace("super_res", "crops"))
        
        col_orig, col_sr = st.columns(2)
        with col_orig:
            st.image(str(original_path), caption="Original (128x128)", use_container_width=True)
        with col_sr:
            st.image(str(last_processed), caption="Super-Resolución (1024x1024)", use_container_width=True)


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def main():
    _init_session()
    search_params = render_sidebar()
    render_main(search_params)


if __name__ == "__main__":
    main()
