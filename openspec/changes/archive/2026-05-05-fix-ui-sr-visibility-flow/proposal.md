## Why

Actualmente, el botón de "Aumento de Resolución (SR)" es visible y accionable incluso si el paso previo de "Procesamiento de Cuadrícula" no se ha ejecutado. Esto genera confusión en el flujo de usuario y puede provocar errores al intentar procesar carpetas de recortes inexistentes o incompletas. Es necesario forzar un flujo de trabajo secuencial en la interfaz.

## What Changes

- **Control de Flujo en UI**: Se condicionará la visibilidad y activación de la sección de Súper-Resolución al éxito previo de la fase de fragmentación de cuadrícula.
- **Estado de Sesión**: Se utilizará `st.session_state` para rastrear la finalización del procesamiento de celdas por fecha.
- **Mensajes Informativos**: Se añadirán mensajes guía que indiquen al usuario que debe procesar la cuadrícula antes de poder aumentar la resolución.

## Capabilities

### New Capabilities
- None

### Modified Capabilities
- `UC-06-escalar-imagenes-edsr`: Se añade el requisito de dependencia funcional en la interfaz de usuario respecto a `UC-05`.

## Impact

- **app.py**: Modificación en el renderizado de la pestaña "3. Procesamiento IA" para incluir lógica condicional.
- **Flujo de Usuario**: Mejora en la experiencia de usuario al prevenir acciones fuera de secuencia.
