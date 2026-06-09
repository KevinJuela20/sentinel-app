## ADDED Requirements

### Requirement: Centralizar la ruta raíz de datos en una función única
El sistema SHALL proveer una función `get_data_root()` en `file_manager.py` que retorne la ruta absoluta `~/Documents/Data_Sentinel` como un objeto `Path`.

#### Scenario: Obtener ruta raíz de datos
- **WHEN** cualquier módulo invoca `get_data_root()`
- **THEN** el sistema retorna `Path.home() / "Documents" / "Data_Sentinel"` como ruta absoluta

#### Scenario: Directorio raíz no existe previamente
- **WHEN** se invoca `get_data_root()` y el directorio `~/Documents/Data_Sentinel` no existe
- **THEN** el sistema MUST crear el directorio (incluyendo padres intermedios) y retornar la ruta creada

#### Scenario: Directorio raíz ya existe
- **WHEN** se invoca `get_data_root()` y el directorio `~/Documents/Data_Sentinel` ya existe
- **THEN** el sistema retorna la ruta existente sin error ni modificación

### Requirement: Eliminar rutas hardcodeadas en la capa de presentación
El módulo `app.py` SHALL utilizar exclusivamente `get_data_root()` para obtener la ruta base de datos. No MUST existir ninguna referencia literal a `"Data_Sentinel"` como path construido con `Path(__file__).parent`.

#### Scenario: Reemplazo de ruta en flujo de descarga
- **WHEN** el usuario inicia una descarga de bandas Sentinel-2 desde la UI
- **THEN** los archivos se guardan dentro de `~/Documents/Data_Sentinel/YYYY/MM/DD/`

#### Scenario: Reemplazo de ruta en flujo de procesamiento
- **WHEN** el usuario ejecuta el procesamiento de mosaicos y recortes
- **THEN** el sistema lee los datos de entrada desde `~/Documents/Data_Sentinel/` y guarda los resultados (crops) en subdirectorios dentro de la misma ruta

#### Scenario: Reemplazo de ruta en galería de recortes
- **WHEN** el usuario accede a la galería de recortes en la UI
- **THEN** el sistema escanea `~/Documents/Data_Sentinel/**/crops/*.png` para listar los recortes disponibles

### Requirement: Importación de get_data_root en app.py
El módulo `app.py` SHALL importar `get_data_root` desde `src.file_manager` junto con las importaciones existentes.

#### Scenario: Import actualizado
- **WHEN** se carga el módulo `app.py`
- **THEN** `get_data_root` está disponible como símbolo importado desde `src.file_manager`
