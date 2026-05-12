## 1. Environment and Dependency Verification

- [x] 1.1 Verify `opencv-contrib-python-headless` installation and `cv2.dnn_superres` availability
- [x] 1.2 Confirm model paths and accessibility in `sentinel-project/models/`

## 2. Refactor Super-Resolution Engine

- [x] 2.1 Update `SuperResEngine` class in `src/super_resolution.py` to use a sequential model loading approach
- [x] 2.2 Implement the two-step upscaling pipeline: 128 -> (x4) -> 512 -> (x2) -> 1024
- [x] 2.3 Add explicit image dimension validation before and after each upsampling step
- [x] 2.4 Improve error handling and logging for DNN module calls to capture specific failures

## 3. Testing and Validation

- [x] 3.1 Execute `verify_sr.py` to validate the fix with a sample image
- [x] 3.2 Verify the final output dimensions are exactly 1024x1024
- [x] 3.3 Test the super-resolution process via the Streamlit UI (app.py)
