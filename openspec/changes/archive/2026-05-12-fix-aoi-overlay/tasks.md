## 1. Corrección de la Fuente KML (RF-OVERLAY-02)

- [x] 1.1 Cambiar `DEFAULT_KML_PATH` en `app.py` (línea 42) de `ARH_MAP.kml` a `ARH_ETAPA.kml`

## 2. Clipping Geométrico en Preview Engine (RF-OVERLAY-01)

- [x] 2.1 Añadir función `_clip_geometry_to_bbox(aoi_geom, bbox)` en `preview_engine.py` que use `shapely.geometry.shape()` + `shapely.geometry.box()` + `.intersection()` para recortar el AOI al extent del tile
- [x] 2.2 Manejar todos los tipos de geometría resultantes del clip: `Polygon`, `MultiPolygon`, `LineString`, `MultiLineString`, `GeometryCollection`, y `EMPTY`
- [x] 2.3 Refactorizar `_draw_aoi_boundary()` para recibir la geometría ya recortada y dibujar correctamente todos los componentes (polígonos y líneas)
- [x] 2.4 Cerrar visualmente cada anillo de polígono conectando el último punto con el primero en `draw.line()`
- [x] 2.5 Integrar `_clip_geometry_to_bbox()` en `apply_aoi_mask()` antes de llamar a `_draw_aoi_boundary()`


## 3. Verificación

- [x] 3.1 Ejecutar la aplicación Streamlit y verificar visualmente que el contorno rojo se muestra correctamente en los tres tiles (MPS, MQT, MQS)
- [x] 3.2 Verificar que tiles sin intersección con el AOI se muestran sin contorno y sin errores

