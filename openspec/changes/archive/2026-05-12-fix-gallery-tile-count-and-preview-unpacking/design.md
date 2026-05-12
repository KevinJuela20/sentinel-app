## Context

The application relies on a 3-tile structure for each Sentinel-2 acquisition date to cover the study area properly.
- **IndexError**: `st.columns(3)` is used, and the loop assumes `len(items) == 3`. If `len(items) > 3`, it accesses an invalid index.
- **Unpacking Error**: `for lon, lat in ring` fails if `ring` contains points with 3 or more coordinates.

## Goals / Non-Goals

**Goals:**
- Filter out dates that don't have exactly 3 tiles.
- Make coordinate unpacking in `_draw_aoi_boundary` robust to extra dimensions.

**Non-Goals:**
- Supporting arbitrary numbers of tiles in the UI.
- Re-querying for missing tiles.

## Decisions

### 1. Filtering in `app.py`
- **Decision**: Filter the `grouped_items` dictionary in `_render_results` to keep only keys where `len(grouped_items[k]) == 3`.
- **Rationale**: Ensures that `_render_date_section` always receives exactly 3 items, satisfying the UI constraints.

### 2. Robust Unpacking in `preview_engine.py`
- **Decision**: Change `for lon, lat in ring:` to `for pt in ring: lon, lat = pt[:2]`.
- **Rationale**: This is a safe way to extract 2D coordinates regardless of whether the input is 2D or 3D.

## Risks / Trade-offs

- **Risk**: Some valid data might be hidden if only 1 or 2 tiles cover the AOI.
- **Mitigation**: The current project requirement is the 3-tile set for the specific ARH area. Filtering is safer than crashing.
