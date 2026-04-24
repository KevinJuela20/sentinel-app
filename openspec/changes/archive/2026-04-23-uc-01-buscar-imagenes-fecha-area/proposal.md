# Change: UC-01 Buscar Imágenes por Fecha y Área

## Why
Los analistas necesitan descubrir imágenes de Sentinel-2 disponibles para un período y zona específicos. Esta es la funcionalidad base sobre la cual se construyen todos los demás casos de uso (previsualización, selección, descarga y procesamiento).

## What Changes
- **ADDED** Interfaz de barra lateral con selectores de mes/año de inicio y fin
- **ADDED** Módulo de carga y parseo de archivos KML para extraer geometría del AOI
- **ADDED** Controlador de Búsqueda que consulta la API STAC de MPC
- **ADDED** Procesamiento de metadatos STAC (fecha, cobertura de nubes, assets)
- **ADDED** Manejo de errores (sin resultados, fallo de conexión)

## Impact
- New specs: `specs/UC-01-buscar-imagenes-fecha-area/spec.md`
- Affected existing specs: Ninguno
- Dependencies on other capabilities: Ninguna (caso de uso base)

## Traceability
| Requirement | Source |
| ----------- | ------ |
| RF-01 | SRS sección 3.2 — Búsqueda Temporal y Espacial de Imágenes |
| UC-01 | detailed_use_cases_Fase1 — Buscar imágenes por fecha y área |
| Controlador de Búsqueda | SDD sección 5.1 |
