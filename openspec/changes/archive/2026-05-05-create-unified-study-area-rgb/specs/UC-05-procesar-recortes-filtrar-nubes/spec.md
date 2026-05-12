## MODIFIED Requirements

### Requirement: Preprocesamiento de Recortes y Filtrado de Nubes (RF-05)

#### Scenario: Generación de mosaico RGB de la zona de estudio
- **WHEN** el procesamiento de recortes para una fecha específica ha finalizado
- **AND** antes de eliminar los archivos temporales
- **THEN** el sistema SHALL identificar todos los archivos `*_visual.tif` de los tiles descargados
- **AND** realizar una unión (mosaico) de estos archivos para cubrir la zona de estudio completa
- **AND** guardar el resultado como `Color_YYYY-MM-DD.tif` en la raíz del directorio de la fecha

#### Scenario: Limpieza de archivos temporales (Actualizado)
- **WHEN** el mosaico RGB ha sido generado con éxito
- **AND** los recortes PNG han sido guardados
- **THEN** el sistema SHALL eliminar los archivos `.tif` originales (excepto el mosaico `Color_*.tif`) para optimizar espacio
