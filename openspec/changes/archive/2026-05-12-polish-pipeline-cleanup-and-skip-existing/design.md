## Context

The current processing pipeline for Sentinel-2 data involves multiple steps: search, download, grid processing (cropping), and super-resolution (SR). 
- **Redundancy**: The system doesn't check if a date has already been downloaded/processed before starting a new download, leading to wasted bandwidth and storage.
- **Temporary Files**: The `crops/` folder (128x128 images) is a temporary intermediate step. Once the 1024x1024 SR images are generated, these crops are no longer needed.
- **State Management**: After a successful SR process, the UI remains in a "completed" state with old variables, which can be confusing for a new search.

## Goals / Non-Goals

**Goals:**
- Skip downloading if valid `.tif` files (or the directory structure) for a date already exist.
- Delete the `crops/` directory for a date once `super_res/` has been successfully populated.
- Reset relevant `st.session_state` variables after SR to return the app to a clean state.

**Non-Goals:**
- Deleting the `super_res/` or main date folders.
- Modifying the underlying super-resolution models.

## Decisions

### 1. Download Validation
- **Decision**: Add a check in `src/downloader.py` or the app's orchestration logic to see if `Data_Sentinel/YYYY/MM/DD` contains the expected `.tif` files before calling `download_item_bands`.
- **Rationale**: This is the most efficient way to prevent redundant network calls.

### 2. Automatic Cleanup
- **Decision**: In `src/super_resolution.py`, add a step at the end of `process_super_res_batch` to delete the `crops_dir` if the process was successful.
- **Rationale**: Frees up disk space and keeps the directory structure clean.

### 3. Session State Reset
- **Decision**: Create a `reset_app_state` function in `app.py` that clears `download_queue`, `search_result`, `selection_confirmed`, and `grid_processed`. Call this after the SR process finishes.
- **Rationale**: Provides a "fresh" feel to the application for the next use case.

## Risks / Trade-offs

- **Risk**: Deleting `crops/` might be problematic if the user wanted to re-run SR with different parameters.
- **Mitigation**: Since parameters are currently fixed, this is acceptable. We can always re-generate crops from `.tif` if needed.
- **Risk**: Validation might skip a date that was only partially downloaded.
- **Mitigation**: Check for the presence of ALL expected bands before considering a date "skipped".
