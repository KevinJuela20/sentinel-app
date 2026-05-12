## Context

El flujo de trabajo actual en la aplicación Streamlit permite que el usuario acceda a la funcionalidad de súper-resolución en cualquier momento. Sin embargo, esta función depende directamente de la existencia de recortes PNG generados en la fase de procesamiento de cuadrícula. La falta de validación visual y lógica en la UI permite ejecuciones fallidas que degradan la experiencia del usuario.

## Goals / Non-Goals

**Goals:**
- Implementar una guarda lógica que impida ejecutar el aumento de resolución si no hay recortes listos.
- Proporcionar feedback visual claro sobre los requisitos previos para cada etapa.
- Asegurar que el estado de "procesamiento completado" persista correctamente durante la sesión.

**Non-Goals:**
- No se automatizará el inicio de SR tras la fragmentación (el usuario aún debe presionar el botón).
- No se bloquearán las pestañas de forma total, solo las acciones críticas dentro de ellas.

## Decisions

### 1. Uso de `st.session_state` para Control de Secuencia
**Decisión**: Introducir una variable `grid_processed` en el estado de la sesión.
**Racional**: Es la forma más eficiente en Streamlit de comunicar el éxito de una operación asíncrona (como el procesamiento de cuadrícula) a otros componentes de la UI que se renderizan posteriormente.

### 2. Renderizado Condicional de la Sección SR
**Decisión**: Utilizar un bloque `if st.session_state.get("grid_processed", False):` para mostrar el botón de aumento de resolución.
**Racional**: Limpia la interfaz y guía al usuario de forma natural hacia el siguiente paso lógico.
**Alternativa**: Mantener el botón visible pero deshabilitado (`disabled=True`). *Decisión*: Se prefiere ocultar o mostrar un mensaje informativo para reducir el ruido visual.

### 3. Validación de Carpeta Física como Respaldo
**Decisión**: Al cargar la pestaña de procesamiento, se verificará si existen subcarpetas `crops/` en los directorios de descarga.
**Racional**: Permite que si el usuario ya procesó los datos en una ejecución anterior, la UI reconozca que puede proceder a SR sin re-procesar la cuadrícula obligatoriamente.

## Risks / Trade-offs

- **[Riesgo] Pérdida de Estado** → Si el usuario recarga la página (F5), el estado de la sesión se pierde. *Mitigación*: La validación física de carpetas (Decisión 3) recuperará el estado automáticamente basándose en la estructura de archivos en disco.
- **[Trade-off] Rigidez del Flujo** → Algunos usuarios avanzados podrían querer saltar pasos. *Racional*: Dado que SR depende críticamente de los recortes, esta rigidez es necesaria para evitar errores de sistema.
