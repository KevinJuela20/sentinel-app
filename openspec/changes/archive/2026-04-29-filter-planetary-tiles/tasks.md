## 1. Constantes y Configuración

- [x] 1.1 Añadir la constante `ALLOWED_TILES = ["MPS", "MQT", "MQS"]` en `src/search_controller.py` junto a las demás constantes del módulo (`MPC_STAC_URL`, `SENTINEL_COLLECTION`)

## 2. Funciones de Filtrado

- [x] 2.1 Implementar `_extract_tile_id(item_id: str) -> str | None` en `src/search_controller.py` que extraiga los últimos 3 caracteres del código MGRS del `item_id` de Sentinel-2 usando regex (patrón: segmento `_T` seguido de 5 caracteres alfanuméricos)
- [x] 2.2 Implementar `_filter_by_tile(items: list[STACItem], allowed: list[str]) -> list[STACItem]` en `src/search_controller.py` que filtre la lista de items conservando solo aquellos cuyo tile ID esté en `allowed`, y que conserve items cuyo tile ID no se pueda extraer (loguear warning)
- [x] 2.3 Integrar `_filter_by_tile()` en `search_images()` después de parsear los items y antes de construir el `SearchResult`, actualizando el `total` con la cantidad filtrada

## 3. Tests Unitarios

- [x] 3.1 Crear tests para `_extract_tile_id()`: caso exitoso con formato estándar, caso con formato no estándar (retorna `None`)
- [x] 3.2 Crear tests para `_filter_by_tile()`: caso con mix de tiles (filtra correctamente), caso con todos tiles permitidos (no filtra), caso con item_id no parseable (conserva el item)
- [x] 3.3 Actualizar test de `search_images()` para verificar que los resultados excluyen tiles no permitidos (mock de la respuesta STAC con 4 tiles, verificar que solo llegan 3)

## 4. Verificación

- [x] 4.1 Ejecutar suite de tests completa (`python -m pytest tests/`) y verificar que todos pasan
- [x] 4.2 Verificar manualmente en la UI de Streamlit que la búsqueda devuelve ~25% menos resultados que antes y que no aparecen items con tile MPT en la galería
