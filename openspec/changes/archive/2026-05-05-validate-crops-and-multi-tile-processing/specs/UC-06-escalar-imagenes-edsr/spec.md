## MODIFIED Requirements

### Requirement: Super-resolución con Modelos EDSR (RF-06)
El sistema SHALL procesar todos los recortes PNG disponibles en la carpeta `crops/`, independientemente del tile de origen. El sistema SHALL aplicar el pipeline de escalado secuencial (128→512→1024) a cada imagen válida.

#### Scenario: Procesamiento de lote multi-tile
- **WHEN** el usuario inicia el proceso de super-resolución para una fecha
- **THEN** el sistema identifica todos los archivos `.png` en la subcarpeta `crops/` (incluyendo aquellos de diferentes tiles como `..._MPS.png`, `..._MQT.png`)
- **AND** aplica el pipeline EDSR x4 y EDSR x2 a cada uno
- **AND** guarda los resultados en `super_res/` manteniendo la referencia al tile en el nombre (ej: `[id]_[fecha]_[id_tile]_SR.png`)
