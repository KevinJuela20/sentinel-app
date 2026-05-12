## Why

The super-resolution module in OpenCV (`dnn_superres`) has been inconsistent or failing to load in recent versions. Pinning to a known stable version (4.12.0) ensures that the upscaling pipeline works correctly across all environments and handles the transition from 128px to 1024px without `AttributeError`.

## What Changes

- Pin `opencv-contrib-python-headless` to version `4.12.0.20250211` (or latest stable 4.12.x).
- Ensure the `SuperResEngine` uses the same sequential loading logic (EDSR x4 then x2) as the provided reference script.
- Update `requirements.txt` to reflect the fixed version.

## Capabilities

### New Capabilities
- None

### Modified Capabilities
- `super-resolution-upscaling`: Update the implementation requirements to use OpenCV 4.12.0 and sequential model application for better stability.

## Impact

- `sentinel-project/requirements.txt`: Version pinning.
- `sentinel-project/src/processor.py`: Internal logic for super-resolution processing if different from the reference script.
- Deployment environments will need to reinstall the specific OpenCV version.
