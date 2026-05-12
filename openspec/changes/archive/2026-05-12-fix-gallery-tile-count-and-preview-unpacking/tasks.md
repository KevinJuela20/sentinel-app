## 1. Gallery Stability (app.py)

- [x] 1.1 Update `_render_results` in `sentinel-project/app.py` to filter `grouped_items` by tile count.
- [x] 1.2 Ensure only dates with exactly 3 items are processed for pre-loading and rendering.
- [x] 1.3 Verify that the `IndexError` no longer occurs during gallery rendering.

## 2. Preview Engine Robustness (preview_engine.py)

- [x] 2.1 Update `_draw_aoi_boundary` in `sentinel-project/src/preview_engine.py` to handle 3D coordinates.
- [x] 2.2 Change the loop unpacking `lon, lat` to explicitly slice the first two coordinates.
- [x] 2.3 Verify that the "too many values to unpack" error is resolved.
