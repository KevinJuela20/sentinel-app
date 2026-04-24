# Especificación de Requerimientos de Software (SRS) - Sentinel Data Downloader

## 1. Introducción

### 1.1 Propósito

El propósito de este documento es definir los requerimientos funcionales y no funcionales para el desarrollo de una aplicación web orientada a la descarga y procesamiento de datos satelitales de Sentinel-2. El público objetivo incluye desarrolladores, analistas geoespaciales e investigadores interesados en el procesamiento masivo de imágenes satelitales.

### 1.2 Alcance

El software se denomina **Sentinel Data Downloader**.

- **Lo que hará**: Permitirá la consulta, visualización, filtrado por nubosidad, descarga selectiva de bandas y preprocesamiento avanzado (recorte por polígonos, escalado con IA) de imágenes de Sentinel-2.
- **Lo que no hará**: No proveerá análisis de clasificación de cobertura de suelo avanzado más allá del filtrado de nubes basado en la máscara SCL. No funcionará como una plataforma de SIG (GIS) completa.
- **Objetivos**: Facilitar el acceso a datos limpios de nubes y listos para alimentar modelos de IA o plugins de QGIS.

### 1.3 Definiciones, Acrónimos y Abreviaturas

| Término              | Definición                                                                                                        |
| --------------------- | ------------------------------------------------------------------------------------------------------------------ |
| **STAC**        | SpatioTemporal Asset Catalog. Estándar para organizar metadatos geoespaciales.                                    |
| **MPC**         | Microsoft Planetary Computer. Plataforma proveedora de los datos y servicios de búsqueda.                         |
| **SCL**         | Scene Classification Layer. Capa de Sentinel-2 que clasifica tipos de píxeles (nubes, sombra, vegetación, etc.). |
| **KML/GeoJSON** | Formatos de archivos geoespaciales usados para definir el área de interés (AOI).                                 |
| **EDSR**        | Enhanced Deep Residual Networks for Single Image Super-Resolution. Modelo de IA para aumentar la resolución.      |
| **TIF**         | Tagged Image File Format. Formato estándar para datos raster geoespaciales.                                       |

### 1.4 Referencias

| Ref | Título                          | Path/URL                                                    | Fecha | Autor         |
| --- | -------------------------------- | ----------------------------------------------------------- | ----- | ------------- |
| 1   | Microsoft Planetary Computer API | [Planetary Computer](https://planetarycomputer.microsoft.com/) | 2026  | Microsoft     |
| 2   | Repositorio STAC Spec            | [STAC Spec](https://github.com/radiantearth/stac-spec)         | 2026  | Radiant Earth |

---

## 2. Descripción General

### 2.1 Perspectiva del Producto

La aplicación es un sistema autónomo basado en la web (usando Streamlit) que interactúa con las APIs de Microsoft Planetary Computer. Funciona como una herramienta de preparación de datos para un flujo de trabajo más amplio que incluye detección de cambios mediante plugins en QGIS.

### 2.2 Funciones del Producto

- Consulta cronológica de imágenes Sentinel-2 L2A.
- Previsualización dinámica de áreas de estudio con recortes personalizados.
- Galería de imágenes con filtrado visual de nubosidad.
- Descarga parcial de activos (bandas específicas) con recorte previo.
- Procesamiento desatendido de recortes por cuadrícula.
- Super-resolución de imágenes mediante modelos EDSR (x2 y x4).

### 2.3 Actores del Sistema

| Actor                         | Descripción                    | Actividades Clave                                                                                |
| ----------------------------- | ------------------------------- | ------------------------------------------------------------------------------------------------ |
| **Usuario (Analista)**  | Usuario final técnico.         | Ingresar fechas, seleccionar imágenes "limpias", iniciar procesos de descarga/preprocesamiento. |
| **MPC STAC API**        | Interfaz de búsqueda de datos. | Proveer metadatos y enlaces a activos satelitales.                                               |
| **MPC Tiler**           | Servicio de renderizado.        | Generar visualizaciones rápidas (tiles) para la previsualización.                              |
| **Sistema de Archivos** | Almacenamiento local.           | Organizar las descargas en la estructura jerárquica definida.                                   |

### 2.4 Restricciones

- **Lenguaje**: Desarrollo obligatorio en Python.
- **Librerías**: Uso de `streamlit`, `pystac-client`, `planetary-computer`, `geopandas`, `leafmap`, `rasterio`.
- **Hardware**: Requiere capacidad de cómputo para ejecutar modelos de IA (EDSR) localmente.
- **Almacenamiento**: Las descargas se realizan por defecto en la carpeta `/Desktop/Download Data` y `/Desktop/Data_Sentinel`.

### 2.5 Suposiciones y Dependencias

- Se asume una conexión a internet estable para la comunicación con MPC.
- Se depende de la disponibilidad del catálogo STAC de Microsoft.
- El usuario debe contar con los archivos `ARH_ETAPA.kml` y `Cuadrícula_ARH.geojson` para definir el área.

---

## 3. Requerimientos Específicos

### 3.1 Interfaces de Software

- **Microsoft Planetary Computer STAC API**: Conexión vía `pystac_client` a `https://planetarycomputer.microsoft.com/api/stac/v1`.
- **Planetary Computer Sign**: Uso de `planetary_computer.sign` para obtener URLs autenticadas de descarga.

### 3.2 Requerimientos Funcionales

**RF-01: Búsqueda Temporal y Espacial de Imágenes**

| Campo                | Valor                                                       |
| -------------------- | ----------------------------------------------------------- |
| ID del Requerimiento | RF-01                                                       |
| Tipo                 | [X] Requerimiento [ ] Restricción                          |
| Prioridad            | [X] Alta (Esencial) [ ] Media (Deseada) [ ] Baja (Opcional) |

**Historia de usuario:**

> *Como analista, quiero ingresar un rango de fechas y un área de estudio para encontrar imágenes satelitales disponibles.*

**Descripción:**
El sistema permitirá ingresar dos fechas (mes y año). Realizará una consulta a la colección `sentinel-2-l2a` usando la intersección del AOI definido por el archivo KML provisto.

---

**RF-02: Previsualización Dinámica con Recorte**

| Campo                | Valor                                                       |
| -------------------- | ----------------------------------------------------------- |
| ID del Requerimiento | RF-02                                                       |
| Tipo                 | [X] Requerimiento [ ] Restricción                          |
| Prioridad            | [ ] Alta (Esencial) [X] Media (Deseada) [ ] Baja (Opcional) |

**Historia de usuario:**

> *Como analista, quiero ver una previa de las imágenes recortadas exactamente al área de interés para evaluar la cobertura de nubes.*

**Descripción:**
El sistema mostrará un thumbnail de baja resolución renderizado vía el MPC Tiler. La visualización debe aplicar una máscara de transparencia a las zonas fuera del área de estudio.

---

**RF-03: Galería de Selección con Metadatos**

| Campo                | Valor                                                       |
| -------------------- | ----------------------------------------------------------- |
| ID del Requerimiento | RF-03                                                       |
| Tipo                 | [X] Requerimiento [ ] Restricción                          |
| Prioridad            | [X] Alta (Esencial) [ ] Media (Deseada) [ ] Baja (Opcional) |

**Historia de usuario:**

> *Como analista, quiero ver el porcentaje de nubosidad y seleccionar múltiples imágenes para descargar simultáneamente.*

**Descripción:**
Mostrar los resultados en una cuadrícula cronológica con el porcentaje de `eo:cloud_cover` y fecha exacta. Permitir selección multuple mediante checkboxes.

---

**RF-04: Descarga Optimizada de Bandas Seleccionadas**

| Campo                | Valor                                                       |
| -------------------- | ----------------------------------------------------------- |
| ID del Requerimiento | RF-04                                                       |
| Tipo                 | [X] Requerimiento [ ] Restricción                          |
| Prioridad            | [X] Alta (Esencial) [ ] Media (Deseada) [ ] Baja (Opcional) |

**Historia de usuario:**

> *Como analista, quiero descargar solo las bandas necesarias recortadas a la cuadrícula para ahorrar tiempo y ancho de banda.*

**Descripción:**
Al confirmar la selección, el sistema descargará las bandas B02, B03, B04 y SCL, además del producto True Color (.tif). Se debe realizar un recorte (clip) a los polígonos del archivo `Cuadrícula_ARH.geojson` antes de guardar en disco.

---

**RF-05: Preprocesamiento de Recortes y Filtrado de Nubes (Fase 2)**

| Campo                | Valor                                                       |
| -------------------- | ----------------------------------------------------------- |
| ID del Requerimiento | RF-05                                                       |
| Tipo                 | [X] Requerimiento [ ] Restricción                          |
| Prioridad            | [X] Alta (Esencial) [ ] Media (Deseada) [ ] Baja (Opcional) |

**Historia de usuario:**

> *Como investigador, quiero generar automáticamente imágenes PNG de cada celda de la cuadrícula que estén libres de nubes.*

**Descripción:**
Por cada polígono en `Cuadrícula_ARH.geojson`, el sistema verificará la capa SCL. Si los píxeles indican presencia de nubes (códigos 1, 2, 3, 8, 9, 10), el recorte se descarta. Si está limpio, se guarda como .png con el formato `[id]_[fecha]`.

---

**RF-06: Super-resolución con Modelos EDSR**

| Campo                | Valor                                                       |
| -------------------- | ----------------------------------------------------------- |
| ID del Requerimiento | RF-06                                                       |
| Tipo                 | [X] Requerimiento [ ] Restricción                          |
| Prioridad            | [ ] Alta (Esencial) [X] Media (Deseada) [ ] Baja (Opcional) |

**Historia de usuario:**

> *Como investigador, quiero aumentar la resolución de mis recortes limpios a 1024x1024 para mejorar la detección de cambios.*

**Descripción:**
Los recortes limpios (aprox. 128x128px) se redimensionarán exactamente a 128x128 y luego pasarán por los modelos EDSRx4 y EDSRx2 para alcanzar un tamaño final de 1024x1024 píxeles.

---

**RF-07: Estructura de Almacenamiento Jerárquica**

| Campo                | Valor                                                       |
| -------------------- | ----------------------------------------------------------- |
| ID del Requerimiento | RF-07                                                       |
| Tipo                 | [ ] Requerimiento [X] Restricción                          |
| Prioridad            | [X] Alta (Esencial) [ ] Media (Deseada) [ ] Baja (Opcional) |

**Historia de usuario:**

> *Como usuario, quiero que mis archivos se organicen automáticamente por año y mes para mantener el orden.*

**Descripción:**
Carpeta principal: `Data_Sentinel`. Subestructuras: `[Año]/[Mes]/[Día]/`. Dentro de cada carpeta de día se almacenará el área completa (.tif) y una subcarpeta con los recortes limpios.

---

### 3.3 Priorización de Requerimientos

| ID    | a. Importancia de Negocio | b. Complejidad Técnica | c. Impacto Arquitectónico | Total |
| ----- | ------------------------- | ----------------------- | -------------------------- | ----- |
| RF-01 | 5                         | 2                       | 3                          | 10    |
| RF-02 | 3                         | 4                       | 2                          | 9     |
| RF-03 | 4                         | 2                       | 2                          | 8     |
| RF-04 | 5                         | 4                       | 4                          | 13    |
| RF-05 | 5                         | 5                       | 4                          | 14    |
| RF-06 | 3                         | 5                       | 3                          | 11    |
| RF-07 | 4                         | 2                       | 2                          | 8     |

---

## 4. Requerimientos No Funcionales

**Rendimiento**

- El proceso de consulta STAC debe responder en menos de 5 segundos.
- La previsualización de tiles debe cargarse de forma asíncrona para no bloquear la interfaz.

**Mantenibilidad**

- El código debe seguir estándares de Python (PEP 8).
- Limpieza automática de datos temporales e innecesarios tras el procesamiento para liberar espacio en disco.

**Portabilidad**

- La aplicación debe ejecutarse en entornos con Python 3.9+ y ser agnóstica al SO.
