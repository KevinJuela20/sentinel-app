# Tasks: UC-06 Escalar imágenes con EDSR

## 1. Motores de IA (Infrastructure)
- [x] 1.1 Crear directorio `sentinel-project/models/` para almacenamiento de pesos
- [x] 1.2 Implementar `sentinel-project/src/super_resolution.py`:
  - Carga de modelos EDSR x4 y x2 usando OpenCV DNN
  - Función `upscale_image(img_path)` que ejecuta el pipeline 128→512→1024
- [x] 1.3 Implementar validación de existencia de archivos `.pb`

## 2. Orquestación Batch (Application)
- [x] 2.1 Implementar `process_super_res_batch(crops_dir)`:
  - Listar PNGs en `crops/`
  - Crear subcarpeta `super_res/`
  - Ejecutar escalado secuencial por cada imagen
- [x] 2.2 Implementar manejo de errores y logging de fallos por imagen

## 3. Integración UI (Presentation)
- [x] 3.1 Agregar sección "Mejora de Resolución IA" en `app.py`
- [x] 3.2 Implementar barra de progreso específica para el escalado AI
- [x] 3.3 Galería de comparación (Antes vs Después) para el último recorte procesado

## 4. Pruebas
- [x] 4.1 Escribir unit tests para `super_resolution.py` (con mocks de DNN si es necesario)
- [x] 4.2 Verificación de dimensiones finales (1024x1024) en archivos generados
- [x] 4.3 Validación de compatibilidad de tipos (uint8)

## Validation Checklist
- [x] Modelos EDSR x4 y x2 integrados correctamente
- [x] Resolución final de 1024x1024 alcanzada
- [x] Estructura `super_res/` creada y poblada
- [x] Barra de progreso funcional en UI
- [x] RF-06 satisfecho
