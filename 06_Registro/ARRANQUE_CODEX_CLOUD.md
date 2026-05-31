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

Lee en este orden:
1. AGENTS.md
2. 06_Registro/INSTRUCCIONES_CODEX_CLOUD_DRIVE.md
3. 06_Registro/CAPACIDAD_DRIVE_UPLOAD.md
4. 06_Registro/USO_HELPER_DRIVE_FIRST.md

Objetivo: continuar generando TODAS las imagenes pendientes del Oloverso, por lotes pequenos de 3 a 10, manteniendo coherencia visual total: OLO stickman luminoso, fondo oscuro elegante, energia verde, pulso amarillo, logo como aro verde con onda amarilla, composicion pedagogica sin texto grande.

Flujo obligatorio:
1. Ejecuta `python tools/oloverso_drive_workflow.py plan --limit 5`.
2. Lee los prompts repo-relativos devueltos por el plan.
3. Genera imagenes temporales.
4. Valida visualmente cada imagen.
5. Sube cada imagen final correcta a Google Drive como archivo independiente PNG/JPG/WebP en la carpeta `Oloverso`, folder ID `1YFDN7o7yxyTVrH3kaPxHta8HxgOKmk1M`.
6. Registra cada upload con `python tools/oloverso_drive_workflow.py record-upload --item-id ... --drive-file-id ... --drive-url ... --local-file ... --notes ...`.
7. Ejecuta `python tools/oloverso_drive_workflow.py audit`.
8. Haz commit y push solo de metadatos/registros. No subas PNG/JPG finales a GitHub.

Regla de seguridad: no marques nada como `Correcta` si no hay DriveFileId/DriveUrl reales de un archivo final independiente en Drive. Si Drive no permite subida cruda de imagenes, usa `Pendiente_Drive` o `Generada_No_Subida` y explica el bloqueo.
```

## Primer control al iniciar

Despues de arrancar en Cloud, confirmar en el resumen:

- Que estas ejecutando en Codex Cloud.
- Que el repo es `Olosolos/Oloverso`.
- Que has leido `AGENTS.md`.
- Que el siguiente lote viene de `tools/oloverso_drive_workflow.py plan --limit 5`.
- Que Drive puede o no puede subir archivos crudos PNG/JPG/WebP.

## Nota sobre limite de uso

Si la interfaz muestra `Se ha alcanzado el limite de uso`, no hay que cambiar el repo ni el prompt. Hay que esperar al restablecimiento indicado por ChatGPT/Codex o ampliar capacidad. El limite impide que Cloud arranque nuevas tareas aunque la configuracion sea correcta.
