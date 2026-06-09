## Context

El proyecto Sentinel-App descarga y persiste imágenes Sentinel-2 (bandas GeoTIFF y recortes PNG) en la ruta `sentinel-project/Data_Sentinel/`. Esta ruta es relativa al archivo `app.py`, lo que provoca que los datos queden dentro del árbol del repositorio git. Las consecuencias son:

- `git status` reporta datos descargados como archivos no rastreados.
- Los datos de usuario no se respaldan de forma independiente del código.
- Desplegar el proyecto en otra máquina puede generar paths inesperados.

La ruta de destino requerida es `~/Documents/Data_Sentinel` (absoluta al directorio `Documents` del usuario actual del sistema operativo).

**Componentes afectados (arquitectura en capas):**

| Capa | Archivo | Rol actual |
|---|---|---|
| Presentación | `app.py` | Construye `base_dir` con `Path(__file__).parent / "Data_Sentinel"` en 5 funciones distintas |
| Infraestructura | `src/file_manager.py` | Crea subdirectorios y resuelve rutas; recibe `base_dir` como parámetro |

## Goals / Non-Goals

**Goals:**
- Introducir `get_data_root()` en `file_manager.py` como única fuente de verdad de la ruta `~/Documents/Data_Sentinel`.
- Reemplazar todas las instancias hardcodeadas de `Path(__file__).parent / "Data_Sentinel"` en `app.py` por `get_data_root()`.
- Garantizar que el directorio destino se crea automáticamente en el primer uso.
- Actualizar `.gitignore` del repositorio para ignorar el directorio antiguo residual.

**Non-Goals:**
- Migración automática de datos existentes de la ruta antigua a la nueva.
- Soporte para rutas configurables por el usuario desde la UI.
- Cambios en la estructura de subdirectorios internos (`YYYY/MM/DD/`, `crops/`, etc.).
- Compatibilidad con Windows (fuera de alcance actual).

## Decisions

### D1 — `get_data_root()` centralizada en `file_manager.py`

**Decisión**: Añadir una función `get_data_root() -> Path` en `file_manager.py` que devuelva y garantice la existencia de `Path.home() / "Documents" / "Data_Sentinel"`.

**Alternativas consideradas**:
- *Variable de módulo constante*: menos flexible si en el futuro se quiere hacer configurable (env var, argumento CLI). Descartada.
- *Constante en `app.py`*: mantendría la lógica en la capa de presentación. Descartada porque `file_manager.py` es la capa de infraestructura natural para resolver rutas de datos.

**Rationale**: Una función en la capa de infraestructura puede evolucionar (leer env var `SENTINEL_DATA_DIR`, por ejemplo) sin cambiar `app.py`.

### D2 — No migrar datos existentes automáticamente

**Decisión**: Los datos en `sentinel-project/Data_Sentinel/` no se mueven programáticamente.

**Rationale**: Una migración automática en startup añade riesgo de perder datos si el proceso falla a mitad. El usuario es quien mejor conoce si quiere conservar los datos antiguos. Se informará en la UI con un mensaje en `app.py` si se detecta el directorio antiguo.

### D3 — Mantener firmas de funciones existentes sin cambio

**Decisión**: `get_output_dir`, `get_full_path` y `check_date_data_exists` conservan su firma `(base_dir, ...)`. Solo cambia el valor concreto que reciben.

**Rationale**: Evita romper los tests unitarios existentes que pasan `base_dir` como parámetro configurable.

## Risks / Trade-offs

| Riesgo | Mitigación |
|---|---|
| El directorio `~/Documents/` no existe en el sistema del usuario | `get_data_root()` usa `mkdir(parents=True, exist_ok=True)` para crear toda la jerarquía |
| Datos antiguos en `sentinel-project/Data_Sentinel/` quedan huérfanos | Añadir aviso en UI + instrucción en README para migración manual |
| Tests que mockean la ruta antigua pueden fallar | Actualizar mocks en `tests/` para apuntar a la nueva función `get_data_root()` |
| En entornos sin directorio `Documents` (ej. servidor headless) la ruta puede ser inesperada | Documentado como limitación; futura mejora: soporte `SENTINEL_DATA_DIR` env var |

## Migration Plan

1. Añadir `get_data_root()` a `file_manager.py`.
2. Actualizar las 5 ocurrencias de `Path(__file__).parent / "Data_Sentinel"` en `app.py`.
3. Actualizar la importación en `app.py` para incluir `get_data_root`.
4. Añadir `sentinel-project/Data_Sentinel/` a `.gitignore`.
5. Actualizar tests existentes que referencien la ruta antigua.
6. Verificación manual: ejecutar `streamlit run app.py`, hacer una descarga y confirmar que los archivos aparecen en `~/Documents/Data_Sentinel/`.

**Rollback**: Revertir el commit. Los datos en la nueva ruta permanecen intactos.
