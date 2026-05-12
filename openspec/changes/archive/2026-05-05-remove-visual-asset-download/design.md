## Context

El sistema descarga actualmente el asset `visual` de Sentinel-2 para generar mosaicos de referencia y previsualizaciones rápidas fuera de Streamlit. Sin embargo, este archivo es redundante ya que los componentes espectrales (B04, B03, B02) se descargan de todos modos. La eliminación de este asset ahorrará espacio y tiempo de descarga.

## Goals / Non-Goals

**Goals:**
- Eliminar `visual` de la lista de descargas automáticas.
- Asegurar que la aplicación no falle al intentar buscar el archivo `visual` inexistente.
- Proporcionar un mecanismo alternativo para generar el mosaico "Color_YYYY-MM-DD.tif" a partir de las bandas RGB individuales.

**Non-Goals:**
- No se modificará la previsualización de la galería en Streamlit (UC-02), ya que esta utiliza el asset `rendered_preview` (thumbnail) que no se descarga a disco permanentemente.

## Decisions

### 1. Actualización de Constantes de Configuración
**Decisión**: Modificar `DEFAULT_BANDS` en `src/file_manager.py`.
**Racional**: Centraliza el cambio y afecta a todas las descargas futuras de forma coherente.

### 2. Generación del Mosaico RGB Sintético
**Decisión**: Modificar `src/processor.py` para que, si el asset `visual` no está presente, intente combinar B04, B03 y B02 en un archivo temporal de 3 bandas antes de llamar a `rasterio.merge` (mosaico).
**Racional**: Mantiene la funcionalidad del "Mosaico RGB Unificado" que es muy valorada por el usuario para control de calidad, sin requerir la descarga del asset extra.

### 3. Manejo de Errores en el Procesador
**Decisión**: Añadir validaciones en `process_all_grids` para manejar de forma segura la ausencia de cualquier banda, emitiendo warnings en lugar de excepciones críticas.

## Risks / Trade-offs

- **[Trade-off] Tiempo de Procesamiento** → Generar el RGB localmente consume tiempo de CPU/IO. *Racional*: Es preferible al tiempo de descarga y uso de disco del asset `visual` completo (que es mucho mayor).
- **[Riesgo] Falta de una banda RGB** → Si falla la descarga de B02, B03 o B04, el mosaico no podrá generarse. *Mitigación*: Se informará al usuario y se generará un mosaico parcial o se omitirá.
