## Why

The application currently crashes with an `IndexError` when a date returns more or fewer than 3 tiles, as the UI is hardcoded to display a 3-column layout. Additionally, an unpacking error occurs in the preview engine when processing KML files with 3D coordinates (longitude, latitude, altitude), as the code only expects 2 values.

## What Changes

- **Tile Count Enforcement**: In the search results gallery, only dates that contain exactly 3 tiles will be displayed. Dates with missing or extra tiles will be filtered out to maintain UI stability.
- **Robust Coordinate Unpacking**: Update the `preview_engine.py` to handle coordinates with more than 2 values (e.g., [lon, lat, alt]) by explicitly taking only the first two.

## Capabilities

### New Capabilities
- None

### Modified Capabilities
- `UC-03-seleccionar-imagenes-galeria`: Update requirement to only show dates with a complete set of 3 tiles.

## Impact

- `sentinel-project/app.py`: Filtering logic for grouped items.
- `sentinel-project/src/preview_engine.py`: Coordinate unpacking logic.
