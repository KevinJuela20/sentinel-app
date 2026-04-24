# Proposal: UC-02 Previsualizar imagen con máscara

## Rationale
Para facilitar la selección de imágenes (UC-03), el usuario necesita ver la calidad real de la imagen sobre su área específica. Mostrar la imagen completa de Sentinel-2 (100km x 100km) es ineficiente y confunde si solo se trabaja sobre una zona pequeña. Esta propuesta implementa un "recorte al vuelo" de los thumbnails de MPC.

## Traceability
- **RF-02**: Previsualización Dinámica con Recorte.
- **SRS**: Satisface el requisito de visualización previa al procesamiento.
- **Dependencies**: Requiere `STACItem` obtenidos en UC-01 y la geometría AOI del KML.

## Proposed Components
- **PreviewEngine**: Módulo encargado del procesamiento de imágenes en memoria (descarga, masking, RGBA).
- **Gallery UI**: Sección en Streamlit que renderiza los resultados de búsqueda como una cuadrícula de imágenes procesadas.

## ADR-003: Memory-only Image Processing
Se ha decidido procesar los thumbnails enteramente en memoria (`BytesIO` + `rasterio.MemoryFile`) para maximizar la velocidad y evitar el uso de almacenamiento temporal en disco para visualizaciones eficientes.
