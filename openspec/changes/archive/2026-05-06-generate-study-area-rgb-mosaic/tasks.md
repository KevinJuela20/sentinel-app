## 1. Utilidades Geográficas

- [x] 1.1 Implementar `load_kml_geometry` en `src/geo_utils.py` habilitando el soporte de drivers de Fiona.
- [x] 1.2 Asegurar que el polígono KML se cargue y se pueda proyectar a diferentes CRS.

## 2. Lógica de Mosaico RGB en el Procesador

- [x] 2.1 Modificar `process_all_grids` en `src/processor.py` para cargar el archivo `ARH_ETAPA.kml` desde la ruta externa.
- [x] 2.2 Implementar la generación de stacks RGB temporales (recortados por KML) para cada uno de los tres tiles.
- [x] 2.3 Utilizar `rasterio.merge` para unir los tres recortes RGB en un mosaico final `Color_YYYY-MM-DD.tif`.
- [x] 2.4 Guardar el mosaico en el directorio raíz de la fecha, junto a la carpeta `crops`.

## 3. Limpieza y Verificación

- [x] 3.1 Actualizar la lógica de limpieza final: solo eliminar archivos `.tif` si el mosaico RGB se generó correctamente.
- [x] 3.2 Verificar que el mosaico resultante sea RGB y mantenga la georreferenciación correcta al abrirlo en QGIS u otra herramienta.
