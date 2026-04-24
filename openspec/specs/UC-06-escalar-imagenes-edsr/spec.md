## Purpose

Aumentar la resolución de los recortes limpios para permitir una mejor detección de cambios. Los archivos PNG generados en UC-05 se redimensionan a 128x128 y luego se aplican modelos de super-resolución EDSR para obtener imágenes de 1024x1024.

## Requirements

### Requirement: Super-resolución con Modelos EDSR (RF-06)
El sistema SHALL redimensionar los recortes limpios a exactamente 128x128 píxeles antes de procesar. El pipeline de super-resolución debe consistir en la aplicación secuencial de dos modelos: EDSR x4 (resultando en 512x512) y EDSR x2 (resultando en 1024x1024). Las imágenes resultantes deben guardarse en formato PNG de 8 bits con el sufijo `_SR`.

#### Scenario: Escalado exitoso de un recorte limpio
- **WHEN** el sistema identifica un archivo `.png` en la subcarpeta `crops/` de una fecha
- **THEN** redimensiona la imagen a 128x128 píxeles usando interpolación bicúbica si es necesario
- **AND** aplica el modelo `EDSR_x4.pb` obteniendo una resolución de 512x512
- **AND** aplica el modelo `EDSR_x2.pb` obteniendo una resolución de 1024x1024
- **AND** guarda el archivo en la subcarpeta `super_res/` con el nombre `[original]_SR.png`
- **AND** verifica que el tamaño del archivo final sea exactamente 1024x1024 píxeles

#### Scenario: Error por falta de archivos de modelo
- **WHEN** el sistema intenta iniciar el proceso de super-resolución
- **AND** no se encuentran los archivos `.pb` en la carpeta `models/`
- **THEN** detiene el proceso de escalado para esa imagen
- **AND** informa al usuario sobre la ausencia de los modelos requeridos mediante una alerta en la UI
- **AND** permite continuar con el procesamiento si se cargan los archivos faltantes

#### Scenario: Proceso completo de super-resolución
- **WHEN** todos los recortes limpios de una fecha han sido procesados
- **THEN** el sistema notifica al usuario que el proceso de super-resolución ha concluido
- **AND** muestra un resumen con cantidad de imágenes procesadas

#### Scenario: Error en modelo EDSR
- **WHEN** el modelo EDSR falla al procesar una imagen
- **THEN** el sistema registra el error en el log
- **AND** conserva la imagen original sin escalar
- **AND** continúa con las demás imágenes

## Acceptance Criteria
- Los recortes se redimensionan correctamente a 128x128 antes del escalado
- EDSRx4 produce imágenes de 512x512
- EDSRx2 produce imágenes finales de 1024x1024
- El tamaño final verificado es exactamente 1024x1024 píxeles
- El usuario recibe notificación al completar el proceso
- Los errores de modelo no detienen el proceso completo

## Stories
- [ ] Story 1: Identificar y listar recortes limpios (.png) en subcarpetas
- [ ] Story 2: Redimensionar imágenes a tamaño base de 128x128
- [ ] Story 3: Cargar e integrar modelo EDSRx4 pre-entrenado
- [ ] Story 4: Cargar e integrar modelo EDSRx2 pre-entrenado
- [ ] Story 5: Aplicar pipeline de escalado secuencial (128→512→1024)
- [ ] Story 6: Verificar tamaño final y guardar en carpeta de procesados
- [ ] Story 7: Implementar notificación y resumen de resultados
- [ ] Story 8: Manejar errores de modelo con logging

## Technical Notes
- Components: Escalador EDSR
- Dependencies: UC-05 (requiere recortes limpios generados)
- Modelos: EDSRx4 (128→512), EDSRx2 (512→1024)
- Entrada: 128x128px PNG de 8 bits
- Salida: 1024x1024px PNG de 8 bits
- Requiere capacidad de cómputo para modelos de IA (GPU recomendada)

## Traceability
| Source | Reference |
| ------ | --------- |
| SRS | RF-06 |
| Use Case | UC-06 |
| SDD | Escalador EDSR (sección 3.2, apéndice 8.2) |
