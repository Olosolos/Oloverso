# Reanudacion tras limite de uso de Codex

Fecha: 2026-05-31

## Idea principal

Si Codex Cloud se cancela por falta de tokens/uso, no hay que reanudar desde memoria local. La siguiente ejecucion debe reconstruir el estado desde GitHub y Google Drive:

1. Leer `AGENTS.md`.
2. Leer `06_Registro/ARRANQUE_CODEX_CLOUD.md`.
3. Ejecutar `python tools/oloverso_drive_workflow.py audit`.
4. Ejecutar `python tools/oloverso_drive_workflow.py plan --limit 3`.
5. Continuar desde el primer item que no sea `Correcta`.

## Configuracion recomendada

Usar una automatizacion recurrente en Codex Cloud cada hora.

Cuando no haya uso disponible, la ejecucion puede fallar o no arrancar. Cuando el limite se restablezca, la siguiente ejecucion programada debe volver a empezar desde GitHub y continuar por la cola.

## Regla anti-perdida

Trabajar en lotes pequenos y atomicos:

- Preferir `--limit 3` cuando haya riesgo de limite.
- Generar, validar, subir a Drive y registrar de una imagen en una imagen.
- Hacer commit despues de cada imagen correcta o, como maximo, despues de un lote pequeno.
- No esperar a generar 10 imagenes para commitear.

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

Ejecuta `python tools/oloverso_drive_workflow.py audit` y luego `python tools/oloverso_drive_workflow.py plan --limit 3`.

Continua solo desde el primer item cuyo Status no sea Correcta. Para cada imagen: genera temporal, valida, sube a Drive como archivo independiente, registra con `record-upload`, ejecuta audit, y haz commit/push de metadatos. No subas PNG/JPG a GitHub. Si falta capacidad de Drive upload, usa Pendiente_Drive o Generada_No_Subida y explica el bloqueo.
```

## Prompt para automatizacion recurrente

```text
Ejecucion recurrente Cloud del proyecto Oloverso. Reanuda siempre desde GitHub, no desde memoria local.

Lee AGENTS.md y 06_Registro/REANUDACION_TRAS_LIMITE_CODEX.md. Ejecuta `python tools/oloverso_drive_workflow.py audit` y `python tools/oloverso_drive_workflow.py plan --limit 3`. Procesa como maximo 3 imagenes, de una en una: generar, validar, subir a Drive, registrar con record-upload, commit/push metadatos. Si el limite de uso corto una ejecucion anterior, ignora memoria parcial y continua desde la cola remota.
```

## Como saber si se reanudo bien

La tarea reanudada debe informar:

- Siguiente item detectado por `plan`.
- Resultado de `audit`.
- Cuantas imagenes proceso en esta ejecucion.
- Commit SHA si hizo cambios.
- Si no pudo continuar, bloqueo exacto.
