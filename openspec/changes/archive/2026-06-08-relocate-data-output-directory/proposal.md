## Why

Actualmente, el directorio `Data_Sentinel/` se crea dentro del directorio del proyecto (`sentinel-project/`), mezclando datos de usuario con código fuente. Esto dificulta el respaldo selectivo de datos, contamina el repositorio git y genera confusión entre artefactos de código y datos descargados. Centralizar los datos en `~/Documents/Data_Sentinel` sigue la convención estándar del sistema operativo y separa claramente código de datos.

## What Changes

- La constante/ruta `base_dir` en `app.py` dejará de apuntar a `Path(__file__).parent / "Data_Sentinel"` y pasará a apuntar a `~/Documents/Data_Sentinel` (usando `Path.home() / "Documents" / "Data_Sentinel"`).
- Se introduce una función centralizada `get_data_root()` en `file_manager.py` que devuelve la ruta raíz absoluta y la crea si no existe, siendo la única fuente de verdad de la ruta base.
- Todas las referencias hardcodeadas a `Path(__file__).parent / "Data_Sentinel"` en `app.py` (líneas 380, 451, 498, 562, 603) son reemplazadas por llamadas a `get_data_root()`.
- El directorio `sentinel-project/Data_Sentinel/` existente en el proyecto puede quedar vacío o ser ignorado; los nuevos datos se escribirán en la nueva ruta.
- Se actualiza `.gitignore` para excluir explícitamente el directorio antiguo si persiste, y se documenta la nueva ruta en el README/comments del código.

## Capabilities

### New Capabilities
- `centralized-data-root`: Función única `get_data_root()` en `file_manager.py` que resuelve y garantiza la existencia de `~/Documents/Data_Sentinel`, utilizada por toda la capa de aplicación.

### Modified Capabilities
- `UC-04-descargar-bandas-recorte`: La ruta de salida de las descargas cambia de relativa-al-proyecto a `~/Documents/Data_Sentinel`. El comportamiento funcional (estructura de subdirectorios por fecha, nombres de archivo) no cambia.

## Impact

- **Archivos afectados**: `sentinel-project/app.py`, `sentinel-project/src/file_manager.py`
- **Datos existentes**: Los datos ya descargados en `sentinel-project/Data_Sentinel/` no se migran automáticamente; el usuario deberá moverlos manualmente si lo desea.
- **Git**: El directorio `sentinel-project/Data_Sentinel/` puede añadirse a `.gitignore` o eliminarse del repositorio.
- **Portabilidad**: La ruta `~/Documents/Data_Sentinel` es compatible con Linux/macOS; en Windows sería `Documents\Data_Sentinel` bajo el perfil de usuario.
- **Sin cambios de API**: Las firmas de `get_output_dir`, `get_full_path` y `check_date_data_exists` no cambian; solo cambia el valor de `base_dir` que se les pasa.
