## 1. Refactorización del Núcleo de Procesamiento

- [x] 1.1 Actualizar `process_grid_cell` en `src/processor.py` para abrir B04 como referencia de CRS y resolución.
- [x] 1.2 Implementar el cálculo de la `window` de extracción basada en los bounds de la celda proyectados al CRS de B04.
- [x] 1.3 Modificar la lógica de validación SCL para que lea el área correspondiente en su resolución nativa (20m) antes de la extracción de 10m.
- [x] 1.4 Implementar la extracción de bandas (B04, B03, B02) usando la `window` calculada y asegurando dimensiones consistentes.

## 2. Mejora de Calidad Visual

- [x] 2.1 Actualizar `save_rgb_png` en `src/image_utils.py` para incluir la normalización por percentiles (2% - 98%) según el ejemplo del usuario.
- [x] 2.2 Asegurar que el descarte por tamaño insuficiente se mantenga en el umbral de 63 píxeles.

## 3. Verificación

- [x] 3.1 Procesar una fecha completa y verificar en los logs que no hay desajustes de dimensiones.
- [x] 3.2 Validar visualmente que los nuevos recortes PNG tienen mejor contraste y alineación.
