## 1. Modify Reflectance Clipping Logic

- [x] 1.1 Update `mosaic_norm` initialization in `src/processor.py` to use `uint16` instead of `uint8`.
- [x] 1.2 Replace percentile-based normalization with `np.clip(band, 0, 3500)` inside the normalization loop.

## 2. Update Output Format

- [x] 2.1 Change `dtype` in output metadata dictionary to `uint16`.
- [x] 2.2 Verify that the `Color_YYYY-MM-DD.tif` file is generated correctly with `uint16` data.
