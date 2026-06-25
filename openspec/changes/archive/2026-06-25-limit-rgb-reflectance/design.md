## Context

The system generates an RGB mosaic from Sentinel-2 bands (B04, B03, B02). Currently, `process_all_grids` in `src/processor.py` takes the final mosaic array, which is originally in Sentinel-2's 10,000-based reflectance (uint16), and converts it into an 8-bit (uint8) image using percentile 2 and 98 limits. This operation causes the final images to appear excessively dark and lose dynamic range when viewed in external GIS software like QGIS.

## Goals / Non-Goals

**Goals:**
- Provide a brighter, higher dynamic range RGB mosaic output.
- Limit reflectance values to a fixed threshold of 3500 to clip excessively bright spots (like clouds or snow) without distorting the normal land reflectance.
- Produce a `uint16` GeoTIFF instead of `uint8` to preserve original data fidelity.

**Non-Goals:**
- Modifying the underlying individual cropped tiles or source files.
- Changing the mosaic bounding box or geographic logic.

## Decisions

1. **Keep raw values, clip at 3500:** Instead of normalizing to 0-255 based on image-wide percentiles (which varies per scene), we will use `np.clip(band, 0, 3500)`. This ensures that typical surface reflectance values remain proportional and unchanged, improving the brightness consistency.
2. **Export as `uint16`:** We will update the `dtype` in the output metadata to `uint16` and ensure the raster array retains `uint16` formatting.
3. **Streamlined Normalization Loop:** The `mosaic_norm` logic will simply be an `np.clip()` on the original mosaic, avoiding expensive percentile calculations and ignoring the 0-10000 conversion logic.

## Risks / Trade-offs

- **Larger File Size:** Outputting 16-bit instead of 8-bit will double the file size of the generated mosaic. Given that the mosaic covers a limited study area, the file size increase is acceptable.
- **Default Visualisation:** Standard image viewers might display a 16-bit TIFF incorrectly if they don't stretch the histogram properly. However, professional GIS tools (QGIS) will display it accurately once symbology is set to min=0, max=3500. This is the desired behavior for the user.
