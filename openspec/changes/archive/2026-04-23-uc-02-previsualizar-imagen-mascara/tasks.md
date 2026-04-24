# Tasks: UC-02 Previsualizar imagen con máscara

## Prerequisites
- [x] Baseline spec created in `specs/UC-02-previsualizar-imagen-mascara/spec.md`
- [x] Change proposal created
- [x] design.md created

## Implementation Tasks

### 1. Preview Engine (Backend)
- [x] 1.1 Crear módulo `sentinel-project/src/preview_engine.py`
  - Acceptance: Módulo importable sin errores
  - Files: `sentinel-project/src/preview_engine.py`

- [x] 1.2 Implementar descarga y apertura de imagen en memoria
  - Acceptance: `download_image(url)` retorna bytes válidos
  - Files: `sentinel-project/src/preview_engine.py`

- [x] 1.3 Implementar lógica de masking con `rasterio`
  - Acceptance: `apply_aoi_mask` retorna un array de 4 bandas (RGBA)
  - Files: `sentinel-project/src/preview_engine.py`

- [x] 1.4 Implementar conversión a PIL Image
  - Acceptance: El output es compatible con `st.image`
  - Files: `sentinel-project/src/preview_engine.py`

### 2. Gallery Integration (Frontend)
- [x] 2.1 Refactorizar `app.py` para incluir sección de galería
  - Acceptance: Contenedor `st.container` para los resultados
  - Files: `sentinel-project/app.py`

- [x] 2.2 Implementar cards de imágenes con `st.columns`
  - Acceptance: Visualización en cuadrícula (grid)
  - Files: `sentinel-project/app.py`

- [x] 2.3 Integrar `PreviewEngine` con cache de Streamlit
  - Acceptance: Las imágenes se cargan y permanecen cacheadas al interactuar
  - Files: `sentinel-project/app.py`

- [x] 2.4 Agregar checkbox de selección en cada card
  - Acceptance: Estado de selección persistente en `st.session_state`
  - Files: `sentinel-project/app.py`

### 3. Error Handling & Placeholders
- [x] 3.1 Manejar fallos del Tiler (HTTP 404/500)
  - Acceptance: Mostrar imagen de placeholder o texto descriptivo
  - Files: `sentinel-project/src/preview_engine.py`, `sentinel-project/app.py`

### 4. Testing
- [x] 4.1 Escribir unit tests para `preview_engine.py`
  - Acceptance: Cobertura de la lógica de masking con mocks
  - Files: `sentinel-project/tests/test_preview_engine.py`

## Validation Checklist
- [x] PreviewEngine funcional con imágenes reales de MPC
- [x] Máscara AOI aplicada correctamente (zonas externas transparentes)
- [x] Galería renderizada sin bloqueos de performance
- [x] Checkboxes capturan correctamente la intención del usuario
- [x] Tests pasando
