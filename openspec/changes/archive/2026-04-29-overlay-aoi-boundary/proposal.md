## Why

Actualmente, el sistema muestra las imágenes de Sentinel-2 recortadas por el Área de Interés (AOI), pero no dibuja el contorno del AOI sobre la imagen. Esto dificulta al usuario ver qué parte exacta de su zona de estudio está siendo cubierta por un tile específico (especialmente en tiles de borde como MQT). Superponer el contorno en color rojo proporcionará una referencia visual clara para que el usuario decida si la cobertura es suficiente para sus necesidades de descarga.

## What Changes

- **Modificar** el motor de previsualización (`src/preview_engine.py`) para dibujar el contorno del AOI en color rojo sobre la imagen generada.
- **Transformar** las coordenadas geográficas del AOI a coordenadas de píxeles usando la transformación afín del recorte de rasterio.
- **Asegurar** que el contorno sea visible y tenga un grosor adecuado.

## Capabilities

### New Capabilities

- `aoi-overlay`: Capacidad para proyectar y dibujar geometrías vectoriales (AOI) sobre imágenes rasterizadas recortadas, manteniendo la precisión geográfica.

### Modified Capabilities

- `UC-02-previsualizar-imagen-mascara`: Se actualiza el requisito de visualización para incluir la superposición del contorno rojo del AOI sobre la imagen recortada.

## Impact

- **Código afectado**: `src/preview_engine.py` (lógica de dibujo), `app.py` (posiblemente limpieza de caché si cambia el formato).
- **Dependencias**: Se utilizará `PIL.ImageDraw` o `cv2` (ya presentes en el proyecto) para el dibujo vectorial.
- **UI**: Las cards de la galería mostrarán imágenes con un contorno rojo que delimita la zona de estudio.
