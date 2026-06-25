## Why

Currently, the RGB mosaic generation process converts reflectance values from 0-10000 to an 8-bit (0-255) scale using the 2nd and 98th percentiles. This often results in mosaics that appear too dark. Keeping the raw values as uint16 and applying a fixed clip limit (e.g., 3500) will yield brighter, more visually appealing mosaics by preserving the original range without forcing it into a narrow 8-bit distribution.

## What Changes

- Modify the `process_all_grids` function in `src/processor.py` to stop converting the mosaic from uint16 to uint8.
- Set a fixed maximum reflectance limit of 3500 and clip all values exceeding it.
- Save the final RGB mosaic as a uint16 GeoTIFF instead of uint8.
- Update the raster meta dictionary to reflect the `uint16` data type.

## Capabilities

### New Capabilities
None.

### Modified Capabilities
- `UC-05-procesar-recortes-filtrar-nubes`: The mosaic generation requirement is changing to produce a uint16 GeoTIFF with a fixed max reflectance of 3500, instead of an 8-bit image with percentile-based normalization.

## Impact

- `src/processor.py`: Changes to the mosaic finalization logic in `process_all_grids`.
- Output artifacts: The final `Color_YYYY-MM-DD.tif` files will be `uint16` instead of `uint8` and might be larger in file size, but will have better dynamic range and visual brightness in GIS software like QGIS.
