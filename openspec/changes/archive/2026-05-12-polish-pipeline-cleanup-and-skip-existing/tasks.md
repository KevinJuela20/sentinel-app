## 1. Download Validation

- [x] 1.1 Modify `sentinel-project/src/downloader.py` or `sentinel-project/app.py` to implement a check for existing `.tif` files before downloading.
- [x] 1.2 Update the download loop to skip dates that already have all required bands locally.

## 2. Post-Processing Cleanup

- [x] 2.1 Update `sentinel-project/src/super_resolution.py` to delete the `crops/` folder after successful batch processing.
- [x] 2.2 Ensure the deletion only happens if the process finished without critical errors.

## 3. UI and State Management

- [x] 3.1 Implement a `reset_app_state` function in `sentinel-project/app.py`.
- [x] 3.2 Integrate the state reset at the end of the `_run_super_res_process` workflow.
- [x] 3.3 Verify that the app returns to a clean state (search sidebar ready, gallery empty) after SR completion.
