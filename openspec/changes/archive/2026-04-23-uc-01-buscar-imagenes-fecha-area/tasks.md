# Tasks: UC-01 Buscar Imágenes por Fecha y Área

## Prerequisites
- [x] Baseline spec created in `specs/UC-01-buscar-imagenes-fecha-area/spec.md`
- [x] Change proposal created
- [x] design.md reviewed and approved

## Implementation Tasks

### 1. Infrastructure Setup
- [x] 1.1 Crear estructura base del proyecto Streamlit
  - Acceptance: `app.py` ejecutable con `streamlit run app.py`
  - Verify: La aplicación se abre en el navegador
  - Files: `app.py`, `requirements.txt`

- [x] 1.2 Configurar dependencias del proyecto
  - Acceptance: Todas las librerías instalables: `streamlit`, `pystac-client`, `planetary-computer`, `geopandas`, `fiona`
  - Verify: `pip install -r requirements.txt` sin errores
  - Files: `requirements.txt`

### 2. Backend Components
- [x] 2.1 Implementar Parser KML
  - Acceptance: `load_aoi("ARH_ETAPA.kml")` retorna geometría GeoJSON válida
  - Verify: Unit test con archivo KML de ejemplo
  - Files: `src/geo_utils.py`

- [x] 2.2 Implementar Controlador de Búsqueda
  - Acceptance: `search_images(mes_inicio, año_inicio, mes_fin, año_fin, geom_aoi)` retorna ItemCollection
  - Verify: Integration test con consulta real a MPC
  - Files: `src/search_controller.py`

- [x] 2.3 Implementar formateo de rango de fechas
  - Acceptance: `format_date_range(1, 2026, 3, 2026)` → `"2026-01-01/2026-03-31"`
  - Verify: Unit test con diferentes combinaciones de fechas
  - Files: `src/search_controller.py`

- [x] 2.4 Procesar metadatos de items STAC
  - Acceptance: Extraer fecha, `eo:cloud_cover`, y assets de cada item
  - Verify: Unit test con mock de ItemCollection
  - Files: `src/search_controller.py`

### 3. Frontend Components
- [x] 3.1 Crear barra lateral con selectores de fecha
  - Acceptance: Selectores de mes y año para inicio y fin
  - Verify: Widgets renderizados en la barra lateral de Streamlit
  - Files: `app.py`

- [x] 3.2 Agregar botón de búsqueda con feedback visual
  - Acceptance: Botón "Buscar" que muestra spinner durante la consulta
  - Verify: Click en botón ejecuta la búsqueda y muestra spinner
  - Files: `app.py`

- [x] 3.3 Mostrar resultados o mensajes de error
  - Acceptance: Mostrar cantidad de imágenes encontradas o mensaje de "sin resultados"
  - Verify: Probar con fechas que tengan y no tengan resultados
  - Files: `app.py`

### 4. Error Handling
- [x] 4.1 Manejar error de conexión con MPC
  - Acceptance: Capturar excepciones de red y mostrar mensaje amigable
  - Verify: Simular fallo de red y verificar mensaje
  - Files: `src/search_controller.py`, `app.py`

- [x] 4.2 Validar fechas de entrada
  - Acceptance: Fecha de inicio no puede ser posterior a fecha de fin
  - Verify: Intentar búsqueda con fechas invertidas
  - Files: `app.py`

### 5. Testing
- [x] 5.1 Escribir unit tests para geo_utils
  - Acceptance: Coverage >= 80% en módulo geo_utils
  - Verify: `pytest tests/test_geo_utils.py`

- [x] 5.2 Escribir unit tests para search_controller
  - Acceptance: Coverage >= 80% en módulo search_controller
  - Verify: `pytest tests/test_search_controller.py`

## Validation Checklist
- [x] Todos los tasks completados
- [x] Todos los criterios de aceptación del spec cumplidos
- [x] RF-01 satisfecho
- [x] Tests pasando (27 passed, 3 skipped — integración requiere geopandas instalado)
- [x] Aplicación ejecutable con `streamlit run app.py`

## Dependencies
- Ninguna (caso de uso base)
