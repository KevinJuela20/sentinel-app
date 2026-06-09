## 1. Infraestructura — file_manager.py

- [x] 1.1 Añadir función `get_data_root() -> Path` en `src/file_manager.py` que retorne `Path.home() / "Documents" / "Data_Sentinel"` y cree el directorio con `mkdir(parents=True, exist_ok=True)`
- [x] 1.2 Exportar `get_data_root` en el `__init__.py` o verificar que sea accesible vía `from src.file_manager import get_data_root`

## 2. Presentación — app.py

- [x] 2.1 Actualizar la línea de import para incluir `get_data_root` en `from src.file_manager import get_output_dir, DEFAULT_BANDS, check_date_data_exists, get_data_root`
- [x] 2.2 Reemplazar `Path(__file__).parent / "Data_Sentinel"` en la función de detección de crops (≈línea 380) por `get_data_root()`
- [x] 2.3 Reemplazar `Path(__file__).parent / "Data_Sentinel"` en la sección de detección de TIFs (≈línea 451) por `get_data_root()`
- [x] 2.4 Reemplazar `Path(__file__).parent / "Data_Sentinel"` en `base_dir` del flujo de descarga (≈línea 498) por `get_data_root()`
- [x] 2.5 Reemplazar `Path(__file__).parent / "Data_Sentinel"` en la sección de procesamiento de mosaicos (≈línea 562) por `get_data_root()`
- [x] 2.6 Reemplazar `Path(__file__).parent / "Data_Sentinel"` en la sección de galería de crops (≈línea 603) por `get_data_root()`

## 3. Limpieza del repositorio

- [x] 3.1 Añadir `sentinel-project/Data_Sentinel/` al `.gitignore` raíz del proyecto (si no está ya)
- [x] 3.2 Verificar que no existen otras referencias hardcodeadas a la ruta antigua en archivos de `src/` o `tests/`

## 4. Verificación

- [x] 4.1 Ejecutar los tests unitarios existentes (`pytest sentinel-project/tests/`) y confirmar que pasan
- [x] 4.2 Verificar manualmente que al iniciar la app, los datos se leen/escriben en `~/Documents/Data_Sentinel/`
