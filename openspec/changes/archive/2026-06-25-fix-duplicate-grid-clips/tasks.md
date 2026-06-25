## 1. Constante de Asignación de IDs de Borde

- [ ] 1.1 Agregar la constante `IDS_POR_TILE` como diccionario a nivel de módulo en `processor.py`, con las claves "MPS", "MQS", "MQT" y sus listas de IDs de celdas de borde
- [ ] 1.2 Agregar un diccionario invertido `_TILE_POR_ID` (generado automáticamente desde `IDS_POR_TILE`) para búsqueda O(1) de tile asignado dado un ID

## 2. Función de Deduplicación

- [ ] 2.1 Crear la función `should_process_cell(cell_id: str, tile_id: str, crops_dir: Path, date_str: str) -> bool` en `processor.py`
- [ ] 2.2 Implementar la lógica de verificación de IDs de borde: si `cell_id` está en `_TILE_POR_ID`, retornar `True` solo si `tile_id` coincide con el tile asignado
- [ ] 2.3 Implementar la lógica de verificación de existencia en disco: si `cell_id` NO está en `_TILE_POR_ID`, verificar si existe algún archivo `{cell_id}_{date_str}_*.png` en `crops_dir`; retornar `True` solo si no existe
- [ ] 2.4 Agregar logging para cada caso de omisión (tile incorrecto / ya existente)

## 3. Integración en el Flujo de Procesamiento

- [ ] 3.1 Modificar el bucle de `process_all_grids` para invocar `should_process_cell` antes de llamar a `process_grid_cell`
- [ ] 3.2 Agregar el contador `dedup_skipped` al diccionario `stats` retornado por `process_all_grids`
- [ ] 3.3 Incrementar `dedup_skipped` cuando `should_process_cell` retorne `False`, sin incrementar `skipped` (que se reserva para omisiones por nubes/tamaño)

## 4. Actualización de la UI

- [ ] 4.1 Actualizar la función `_run_grid_processing` en `app.py` para mostrar el nuevo contador `dedup_skipped` junto a los contadores existentes de guardados y omitidos

## 5. Verificación

- [ ] 5.1 Verificar que la sintaxis del módulo `processor.py` sea correcta (importación exitosa)
- [ ] 5.2 Revisar que el flujo completo de `process_all_grids` maneje correctamente los tres escenarios: ID de borde en tile correcto, ID de borde en tile incorrecto, ID no listado con/sin existencia previa
