## Why

La superposición del contorno del AOI (borde rojo) sobre los tiles de previsualización muestra una geometría incorrecta: líneas rectas formando triángulos en lugar del perímetro real de la zona de estudio. La causa raíz tiene dos componentes:

1. **KML incorrecto**: El sistema carga `ARH_MAP.kml` (un cuadrilátero simplificado de 5 vértices) en lugar de `ARH_ETAPA.kml` (el polígono real con ~150 vértices de la cuenca MACHANGARA). Esto traza UC-02 (RF-02) y la spec existente `aoi-overlay`.
2. **Sin recorte al extent del tile**: La función `_draw_aoi_boundary` en `preview_engine.py` proyecta todos los vértices al espacio de píxeles sin recortar (clip) la geometría al bounding box del tile. Cuando el AOI excede los límites del tile, las líneas se dibujan fuera de la imagen creando artefactos visuales. Esto explica por qué en el sistema de referencia solo se veía correctamente en el tile MPS (el único que contenía la mayor parte del AOI) pero no en MQT ni MQS.

## What Changes

- Cambiar `DEFAULT_KML_PATH` en `app.py` para apuntar a `ARH_ETAPA.kml` (el polígono de la zona de estudio real).
- Refactorizar `_draw_aoi_boundary()` en `preview_engine.py` para **recortar (clip)** la geometría del AOI al bounding box del tile antes de dibujar, usando `shapely.intersection()`. Esto garantiza que el contorno se dibuje correctamente en los tres tiles (MPS, MQT, MQS), mostrando solo la porción del AOI que cae dentro de cada tile.
- Cerrar visualmente el polígono (conectar el último punto con el primero) en `draw.line()`.

## Capabilities

### New Capabilities

_(ninguna — se corrige la implementación existente)_

### Modified Capabilities

- `aoi-overlay`: El requisito RF-OVERLAY-01 se mantiene, pero la implementación cambia para usar clipping geométrico en lugar de proyección directa, y se corrige el archivo KML fuente para representar la zona de estudio real.

## Impact

- **Archivos afectados**:
  - `sentinel-project/app.py` (línea 42: `DEFAULT_KML_PATH`)
  - `sentinel-project/src/preview_engine.py` (función `_draw_aoi_boundary`)
- **Dependencias**: Se requiere `shapely` (ya instalada como dependencia de `geopandas`).
- **Sin cambios en APIs ni modelos de datos**: La firma de `get_masked_preview()` y la estructura del `aoi_geom` (GeoJSON dict) no cambian.
- **UC dependientes**: UC-04 (descarga con recorte) no se ve afectado ya que usa la misma geometría GeoJSON para el clip rasterizado, que ya funciona correctamente.
