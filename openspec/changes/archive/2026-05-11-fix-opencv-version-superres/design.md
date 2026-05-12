## Context

The current super-resolution implementation in the Sentinel app relies on OpenCV's `dnn_superres` module. Recent environment updates or inconsistent installations of `opencv-contrib-python-headless` have led to `AttributeError` because the module is missing or not correctly loaded. The user has verified that version `4.12.0` (specifically the contrib headless version) works correctly with their EDSR models.

## Goals / Non-Goals

**Goals:**
- Fix the `AttributeError: module 'cv2' has no attribute 'dnn_superres'` by pinning the correct OpenCV version.
- Implement a two-stage upscaling pipeline (x4 then x2) to achieve 1024px from 128px source images, matching the user's reference script.
- Ensure the `SuperResEngine` (or equivalent in `processor.py`) is robust and handles model loading sequentially.

**Non-Goals:**
- Upgrading to other super-resolution libraries (e.g., Real-ESRGAN) at this time.
- Changing the underlying UI for image selection.

## Decisions

### 1. Pin OpenCV Version
- **Decision**: Pin `opencv-contrib-python-headless==4.12.0.20250211` in `requirements.txt`.
- **Rationale**: The user confirmed this version works. Using the `headless` version is standard for Streamlit/Docker environments to avoid dependency issues with X11/GUI libraries.
- **Alternatives**: Using the standard `opencv-python` (lacks contrib modules) or `opencv-contrib-python` (may have GUI dependencies).

### 2. Sequential Model Loading
- **Decision**: The engine will load and execute the x4 model, then load and execute the x2 model on the result.
- **Rationale**: Achieving x8 total scale (128 -> 1024) is best done using the models designed for specific ratios (4 and 2) rather than attempting a single x8 jump if a single x8 model is not available or stable.

## Risks / Trade-offs

- **Risk**: Pinning a very specific version might conflict with other libraries if they have strict OpenCV version requirements.
- **Mitigation**: Test the entire Streamlit app to ensure no regressions in image processing or display.
- **Risk**: Performance might be slow for multiple concurrent requests.
- **Mitigation**: The `ProcessPoolExecutor` (as seen in the reference) is a good approach for background processing, but within Streamlit, we should be careful with resource management.
