## 1. Environment and Dependencies

- [x] 1.1 Update `sentinel-project/requirements.txt` to pin `opencv-contrib-python-headless==4.12.0.20250211`
- [x] 1.2 Reinstall dependencies in the virtual environment to verify version compatibility

## 2. Core Implementation Refactoring

- [x] 2.1 Modify `sentinel-project/src/processor.py` (or the relevant super-resolution engine) to implement sequential model application (EDSR x4 followed by EDSR x2)
- [x] 2.2 Ensure robust error handling for `cv2.dnn_superres` initialization to catch missing module errors gracefully
- [x] 2.3 Verify that the final output dimensions are consistently 1024x1024

## 3. Verification and Cleanup

- [x] 3.1 Run `sentinel-project/verify_sr.py` with the new environment to confirm it works without `AttributeError`
- [x] 3.2 Test the full processing pipeline via the Streamlit UI (`app.py`)
- [x] 3.3 Verify that the `super_res/` output folder contains the expected high-resolution images
