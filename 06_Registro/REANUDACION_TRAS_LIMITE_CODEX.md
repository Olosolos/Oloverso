# Reanudacion tras limite de uso de Codex

Fecha: 2026-05-31

## Idea principal

Si Codex Cloud se cancela por falta de tokens/uso, no hay que reanudar desde memoria local. La siguiente ejecucion debe reconstruir el estado desde GitHub y Google Drive:

1. Leer `AGENTS.md`.
2. Leer `06_Registro/ARRANQUE_CODEX_CLOUD.md`.
3. Leer `06_Registro/CAPACIDAD_DRIVE_UPLOAD.md`.
4. Verificar capacidad real de subida cruda PNG/JPG/WebP a Drive.
5. Si no existe esa capacidad, detenerse con `Bloqueado_DriveUpload` sin generar ni commitear.
6. Solo si Drive upload funciona, ejecutar `python tools/oloverso_drive_workflow.py audit`.
7. Ejecutar `python tools/oloverso_drive_workflow.py plan --limit 1`.
8. Continuar desde el primer item que no sea `Correcta`.

## Configuracion recomendada

Usar una automatizacion recurrente en Codex Cloud cada hora.

Cuando no haya uso disponible, la ejecucion puede fallar o no arrancar. Cuando el limite se restablezca, la siguiente ejecucion programada debe volver a empezar desde GitHub y continuar por la cola.

## Regla anti-perdida

Trabajar en lotes pequenos y atomicos:

- Preferir `--limit 1` hasta que la subida a Drive este probada varias veces en Codex Cloud.
- Generar, validar, subir a Drive y registrar una imagen completa antes de empezar la siguiente.
- Hacer commit despues de cada imagen correcta.
- No esperar a generar varias imagenes para commitear.
- No generar nada si la ejecucion actual no puede subir PNG/JPG/WebP crudos a Drive.

Si una ejecucion se corta antes del commit, ese trabajo puede perderse. Por eso cada imagen completada debe quedar registrada cuanto antes en GitHub.

## Prompt de reanudacion manual

Pegar esto en Codex Cloud si una tarea quedo cancelada:

```text
Reanuda el proyecto Oloverso desde GitHub, no desde memoria local. Trabaja en Codex Cloud sobre Olosolos/Oloverso.

Primero lee:
1. AGENTS.md
2. 06_Registro/ARRANQUE_CODEX_CLOUD.md
3. 06_Registro/REANUDACION_TRAS_LIMITE_CODEX.md
4. 06_Registro/CAPACIDAD_DRIVE_UPLOAD.md
5. 06_Registro/USO_HELPER_DRIVE_FIRST.md

Antes de generar cualquier imagen, verifica que tienes una herramienta real y autenticada para subir PNG/JPG/WebP crudos como archivos independientes a Google Drive en la carpeta `Oloverso`, folder ID `1YFDN7o7yxyTVrH3kaPxHta8HxgOKmk1M`.

Si no tienes subida cruda real a Drive, detente inmediatamente. Reporta `Bloqueado_DriveUpload`. No generes imagenes temporales, no modifiques cola/manifiestos, no hagas commit y no marques nada como Correcta.

Solo si Drive upload funciona: ejecuta `python tools/oloverso_drive_workflow.py audit` y luego `python tools/oloverso_drive_workflow.py plan --limit 1`.

Continua solo desde el primer item cuyo Status no sea Correcta. Para esa imagen: genera temporal, valida visualmente, sube a Drive como archivo independiente, registra con `record-upload`, ejecuta audit, y haz commit/push de metadatos. No subas PNG/JPG a GitHub.

En el resumen final indica: modelo/entorno visible, item procesado, DriveFileId/DriveUrl real si hubo subida, resultado de audit y commit SHA.
```

## Prompt para automatizacion recurrente

```text
Ejecucion recurrente Cloud del proyecto Oloverso. Reanuda siempre desde GitHub, no desde memoria local.

Lee AGENTS.md, 06_Registro/CAPACIDAD_DRIVE_UPLOAD.md y 06_Registro/REANUDACION_TRAS_LIMITE_CODEX.md.

Antes de planificar o generar, verifica capacidad real de subida cruda PNG/JPG/WebP a Google Drive folder ID `1YFDN7o7yxyTVrH3kaPxHta8HxgOKmk1M`.

Si no tienes esa capacidad, termina con `Bloqueado_DriveUpload`: no generes imagenes, no edites cola/manifiesto, no hagas commit.

Solo si Drive upload funciona: ejecuta `python tools/oloverso_drive_workflow.py audit` y `python tools/oloverso_drive_workflow.py plan --limit 1`. Procesa como maximo 1 imagen: generar, validar, subir a Drive, registrar con record-upload, audit, commit/push metadatos. Si el limite de uso corto una ejecucion anterior, ignora memoria parcial y continua desde la cola remota.
```

## Como saber si se reanudo bien

La tarea reanudada debe informar:

- Modelo/entorno visible en la interfaz, si esta disponible.
- Resultado del preflight Drive upload.
- Siguiente item detectado por `plan`.
- Resultado de `audit`.
- Cuantas imagenes proceso en esta ejecucion.
- DriveFileId/DriveUrl real si subio una imagen.
- Commit SHA si hizo cambios.
- Si no pudo continuar, bloqueo exacto.
