## Why

To improve system efficiency and user experience by avoiding redundant data processing and ensuring a clean state for subsequent searches. Currently, the system may re-download existing data and leaves temporary crop files even after they are no longer needed.

## What Changes

- **Download Skipping**: Before starting the download for a specific date, the system will check if valid data for that date already exists in `Data_Sentinel`. If it exists, the download will be skipped.
- **Post-SR Cleanup**: Automatically delete the `crops/` directory after the Super-Resolution process is successfully completed.
- **Session Reset**: Clear relevant Streamlit session state variables (selection, confirmation, etc.) after the SR process to allow the user to start a fresh search without manual intervention.

## Capabilities

### New Capabilities
- None

### Modified Capabilities
- `UC-04-descargar-bandas-recorte`: Add requirement to validate existing local data before downloading.
- `UC-06-escalar-imagenes-edsr`: Add requirement to cleanup temporary files and reset application state after successful processing.

## Impact

- `sentinel-project/app.py`: UI logic for session reset and download orchestration.
- `sentinel-project/src/downloader.py`: Logic to check for existing folders/files.
- `sentinel-project/src/super_resolution.py`: Logic to delete the crops directory.
