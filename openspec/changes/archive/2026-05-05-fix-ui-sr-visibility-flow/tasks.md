## 1. Gestión de Estado en la Aplicación

- [x] 1.1 Inicializar la variable `grid_processed` en `st.session_state` dentro de `app.py`.
- [x] 1.2 Actualizar `grid_processed` a `True` tras una ejecución exitosa de `_run_grid_process`.
- [x] 1.3 Reiniciar `grid_processed` a `False` cuando se limpie la cola de descargas o se inicie una nueva búsqueda.

## 2. Refactorización de la Interfaz (Streamlit)

- [x] 2.1 Implementar la función `_check_if_crops_exist` para verificar físicamente la presencia de recortes en el disco y actualizar el estado de sesión de forma proactiva.
- [x] 2.2 Modificar el renderizado de la pestaña "3. Procesamiento IA" para mostrar condicionalmente la sección de Súper-Resolución.
- [x] 2.3 Añadir mensajes informativos (`st.info`) que guíen al usuario sobre los pasos previos faltantes.

## 3. Verificación

- [x] 3.1 Verificar manualmente que al iniciar la app el botón de SR está oculto.
- [x] 3.2 Verificar que tras procesar la cuadrícula, el botón de SR aparece automáticamente.
- [x] 3.3 Validar que el reinicio de búsqueda oculta nuevamente la sección de SR.
