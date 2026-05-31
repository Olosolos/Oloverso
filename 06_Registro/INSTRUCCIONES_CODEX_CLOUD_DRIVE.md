# Instrucciones para Codex Cloud - Oloverso Drive-first

Usa este texto como prompt para Codex Cloud o para cualquier automatizacion cloud del proyecto. No usar la automatizacion local del PC para producir imagenes.

```text
Trabaja en Codex Cloud sobre el repositorio GitHub Olosolos/Oloverso.

Objetivo: continuar el proyecto Oloverso generando TODAS las imagenes pendientes de las leyes, con la misma coherencia visual ya definida: OLO como guia stickman luminoso, fondo oscuro elegante, energia verde del Oloverso, pulso amarillo, logo integrado como aro verde con onda amarilla, composicion pedagogica sin texto grande.

Regla de ejecucion:
- Ejecutate solo en Codex Cloud.
- No dependas de mi PC local ni de rutas C:\Users\david.
- Usa el repo remoto como fuente de verdad.
- No uses la automatizacion local pausada.

Regla de almacenamiento:
- GitHub NO debe almacenar las imagenes finales masivamente.
- GitHub solo debe guardar prompts, CSV, registros, tablero, scripts y manifiestos.
- Todas las imagenes finales deben subirse a Google Drive como archivos PNG/JPG/WebP independientes en la carpeta compartida:
  Nombre: Oloverso
  Folder ID: 1YFDN7o7yxyTVrH3kaPxHta8HxgOKmk1M
  URL: https://drive.google.com/drive/folders/1YFDN7o7yxyTVrH3kaPxHta8HxgOKmk1M

Primero lee AGENTS.md, 06_Registro/CAPACIDAD_DRIVE_UPLOAD.md y 06_Registro/USO_HELPER_DRIVE_FIRST.md. Despues:
1. Ejecuta python tools/oloverso_drive_workflow.py plan --limit 5.
2. Lee 06_Registro/Cola Generacion Imagenes Oloverso.csv.
3. Lee 06_Registro/Manifest Drive Imagenes Oloverso.csv.
4. Genera un lote pequeno de 3 a 10 imagenes.
5. Valida visualmente cada imagen.
6. Sube cada imagen correcta a Google Drive dentro de la carpeta Oloverso como archivo final independiente.
7. Registra DriveFileId, DriveUrl, FileName, SHA256 si esta disponible, Status, Notes y CreatedAt con tools/oloverso_drive_workflow.py record-upload.
8. Marca Correcta en la cola solo despues de que la imagen este subida a Drive y registrada.
9. Actualiza SIGUIENTE_ACCION_GENERAR.txt, Tablero Produccion Imagenes Oloverso.md, resumenes e indice de lotes.
10. Haz commit y push a GitHub solo con metadatos/registros. No subas PNG/JPG finales al repo.

Si Google Drive no permite subir archivos crudos PNG/JPG/WebP en la ejecucion actual, no marques el item como Correcta. Usa Pendiente_Drive o Generada_No_Subida y reporta el bloqueo exacto. Insertar imagenes en Docs, Slides o Sheets no cuenta como subida final.
```

## Prompt corto para la automatizacion horaria cloud

```text
Continua el proyecto Oloverso desde Olosolos/Oloverso en Codex Cloud. Lee AGENTS.md primero.

Toma el siguiente lote pendiente de 3 a 10 imagenes con `python tools/oloverso_drive_workflow.py plan --limit 5`. Genera, valida y sube cada imagen correcta a Google Drive como archivo independiente PNG/JPG/WebP en la carpeta Oloverso, folder ID 1YFDN7o7yxyTVrH3kaPxHta8HxgOKmk1M. No guardes PNG/JPG finales en GitHub. Registra cada upload con `python tools/oloverso_drive_workflow.py record-upload ...`. Actualiza cola, Manifest Drive Imagenes Oloverso.csv, tablero, resumenes y SIGUIENTE_ACCION_GENERAR.txt. Haz commit y push solo de metadatos/registros. Manten coherencia visual total del Oloverso.
```
