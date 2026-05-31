# Arranque Codex Cloud - Oloverso

Este archivo existe para arrancar la produccion desde Codex Cloud sin depender del PC local ni de este hilo local.

## Estado operativo

- Produccion local: pausada.
- Fuente de verdad: `https://github.com/Olosolos/Oloverso`.
- Modo correcto: Codex Cloud.
- Almacen de imagenes finales: Google Drive carpeta `Oloverso`.
- Drive folder ID: `1YFDN7o7yxyTVrH3kaPxHta8HxgOKmk1M`.
- Drive URL: `https://drive.google.com/drive/folders/1YFDN7o7yxyTVrH3kaPxHta8HxgOKmk1M`.

## Prompt para pegar en Codex Cloud

```text
Trabaja en Codex Cloud sobre el repositorio Olosolos/Oloverso. No uses local, no uses worktrees del PC, no dependas de C:\Users\david y no ejecutes automatizaciones locales.

Reanuda siempre desde GitHub, no desde memoria local. Si una ejecucion anterior se cancelo por limite de uso, ignora cualquier estado parcial no commiteado y reconstruye el avance desde la cola y el manifiesto remotos.

Antes de planificar o generar, reporta el modelo/entorno que estas usando si la interfaz te lo permite.

Lee en este orden:
1. AGENTS.md
2. 06_Registro/REANUDACION_TRAS_LIMITE_CODEX.md
3. 06_Registro/INSTRUCCIONES_CODEX_CLOUD_DRIVE.md
4. 06_Registro/CAPACIDAD_DRIVE_UPLOAD.md
5. 06_Registro/USO_HELPER_DRIVE_FIRST.md

Objetivo: continuar generando TODAS las imagenes pendientes del Oloverso, por lotes pequenos, manteniendo coherencia visual total: OLO stickman luminoso, fondo oscuro elegante, energia verde, pulso amarillo, logo como aro verde con onda amarilla, composicion pedagogica sin texto grande.

Preflight obligatorio:
1. Antes de ejecutar `plan` y antes de generar imagenes, verifica que tienes una herramienta real y autenticada para subir PNG/JPG/WebP crudos como archivos independientes a Google Drive.
2. La carpeta destino obligatoria es `Oloverso`, folder ID `1YFDN7o7yxyTVrH3kaPxHta8HxgOKmk1M`.
3. Si no tienes subida cruda real a Drive, detente inmediatamente con estado `Bloqueado_DriveUpload`.
4. En ese caso no generes imagenes temporales, no modifiques la cola, no cambies manifiestos y no hagas commit.

Flujo obligatorio solo si el preflight de Drive es correcto:
1. Ejecuta `python tools/oloverso_drive_workflow.py audit`.
2. Ejecuta `python tools/oloverso_drive_workflow.py plan --limit 1`.
3. Lee el prompt repo-relativo devuelto por el plan.
4. Procesa una imagen: generar temporal, validar visualmente, subir a Drive, registrar y commitear metadatos.
5. Sube la imagen final correcta a Google Drive como archivo independiente PNG/JPG/WebP en la carpeta `Oloverso`, folder ID `1YFDN7o7yxyTVrH3kaPxHta8HxgOKmk1M`.
6. Registra el upload con `python tools/oloverso_drive_workflow.py record-upload --item-id ... --drive-file-id ... --drive-url ... --local-file ... --notes ...`.
7. Ejecuta `python tools/oloverso_drive_workflow.py audit` al final.
8. Haz commit y push solo de metadatos/registros. No subas PNG/JPG finales a GitHub.

Regla de seguridad: no marques nada como `Correcta` si no hay DriveFileId/DriveUrl reales de un archivo final independiente en Drive. Si Drive no permite subida cruda de imagenes, no generes nada y explica el bloqueo.
```

## Primer control al iniciar

Despues de arrancar en Cloud, confirmar en el resumen:

- Que estas ejecutando en Codex Cloud.
- Que modelo/entorno reporta la interfaz, si es visible.
- Que el repo es `Olosolos/Oloverso`.
- Que has leido `AGENTS.md` y `REANUDACION_TRAS_LIMITE_CODEX.md`.
- Que has verificado la capacidad real de subida cruda PNG/JPG/WebP a Drive antes de generar.
- Que el siguiente lote viene de `tools/oloverso_drive_workflow.py plan --limit 1` solo si Drive upload funciona.

## Nota sobre limite de uso

Si la interfaz muestra `Se ha alcanzado el limite de uso`, no hay que cambiar el repo ni el prompt. Hay que esperar al restablecimiento indicado por ChatGPT/Codex o ampliar capacidad. El limite impide que Cloud arranque nuevas tareas aunque la configuracion sea correcta.

Para reanudar tras el limite, crear o reintentar una ejecucion Cloud con el prompt de `06_Registro/REANUDACION_TRAS_LIMITE_CODEX.md`. La tarea debe continuar desde el primer item no `Correcta` de la cola remota.
