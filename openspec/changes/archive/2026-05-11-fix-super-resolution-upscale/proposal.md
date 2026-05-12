## Why

The current super-resolution implementation is failing due to library errors and does not consistently achieve the required 1024x1024 resolution. The user has provided a working reference implementation that needs to be integrated into the project's architecture to ensure stable and correct upscaling of the 128x128 crops.

## What Changes

- **Fix `SuperResEngine` Logic**: Update the `src/super_resolution.py` to correctly orchestrate the x4 and x2 EDSR models, following the provided working example.
- **Library Error Resolution**: Ensure the `cv2.dnn_superres` module is correctly utilized and handle potential environment-specific issues that cause attribute errors.
- **Path and Model Alignment**: Ensure models are loaded from the correct relative paths within the project structure (`sentinel-project/models/`).

## Capabilities

### New Capabilities
- None

### Modified Capabilities
- `UC-06-escalar-imagenes-edsr`: Updated implementation logic for the upscaling pipeline to ensure stability and correct final dimensions (1024x1024).

## Impact

- `src/super_resolution.py`: Core logic for model loading and image processing.
- `sentinel-project/models/`: Model file locations and accessibility.
- `requirements.txt`: Verify `opencv-contrib-python-headless` versioning if necessary to avoid `AttributeError`.
