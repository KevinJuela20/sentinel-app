## Project Structure

- `sentinel-project/`: Root of the implementation codebase.
  - `src/`: Core logic and backend modules.
  - `tests/`: Test suite.
  - `external/`: GeoJSON/KML and AI models.
  - `app.py`: Streamlit main application.
  - `requirements.txt`: Python dependencies.
- `openspec/`: OpenSpec orchestration artifacts (specs, changes, project overview).
- `input/`: Requirements and design documents (SRS, SDD).

## Use Case Dependency Graph

```
Level 0 (sin dependencias):
  UC-01 Buscar imágenes por fecha y área

Level 1 (depende de Level 0):
  UC-02 Previsualizar imagen con máscara → depende de UC-01

Level 2 (depende de Level 1):
  UC-03 Seleccionar imágenes de la galería → depende de UC-02

Level 3 (depende de Level 2):
  UC-04 Descargar bandas seleccionadas → depende de UC-03

Level 4 (depende de Level 3):
  UC-05 Procesar recortes y filtrar nubes → depende de UC-04

Level 5 (depende de Level 4):
  UC-06 Escalar imágenes con modelos EDSR → depende de UC-05
```

## Implementation Order

| Orden | Caso de Uso | Dependencias | Prioridad | Sprint |
|-------|-------------|--------------|-----------|--------|
| 1 | UC-01 Buscar imágenes por fecha y área | Ninguna | Alta | Sprint 1 |
| 2 | UC-02 Previsualizar imagen con máscara | UC-01 | Media | Sprint 1 |
| 3 | UC-03 Seleccionar imágenes de la galería | UC-02 | Alta | Sprint 2 |
| 4 | UC-04 Descargar bandas seleccionadas | UC-03 | Alta | Sprint 2 |
| 5 | UC-05 Procesar recortes y filtrar nubes | UC-04 | Alta | Sprint 3 |
| 6 | UC-06 Escalar imágenes con EDSR | UC-05 | Media | Sprint 3 |

## Traceability Matrix

| RF | Descripción | UC | Componente SDD |
|----|-------------|----|----------------|
| RF-01 | Búsqueda Temporal y Espacial | UC-01 | Controlador de Búsqueda |
| RF-02 | Previsualización Dinámica | UC-02 | UI Principal + Tiler |
| RF-03 | Galería de Selección | UC-03 | Galería + UI |
| RF-04 | Descarga Optimizada de Bandas | UC-04 | Motor de Procesamiento |
| RF-05 | Filtrado de Nubes | UC-05 | Motor de Procesamiento |
| RF-06 | Super-resolución EDSR | UC-06 | Escalador EDSR |
| RF-07 | Estructura de Almacenamiento | UC-04, UC-05 | Gestor FileSys |
