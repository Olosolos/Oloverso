# Capacidad requerida para subir imagenes a Drive

Fecha: 2026-05-31

## Regla principal

Una imagen del Oloverso solo puede producirse dentro del flujo Drive-first cuando la ejecucion actual puede subir el archivo final de imagen a Google Drive como PNG/JPG/WebP independiente.

Destino oficial:

- Carpeta: `Oloverso`
- Folder ID: `1YFDN7o7yxyTVrH3kaPxHta8HxgOKmk1M`
- URL: `https://drive.google.com/drive/folders/1YFDN7o7yxyTVrH3kaPxHta8HxgOKmk1M`

## Preflight obligatorio antes de generar

Antes de generar cualquier imagen, la tarea debe demostrar que tiene una herramienta/API autenticada capaz de subir un archivo PNG/JPG/WebP crudo a la carpeta Drive oficial.

Si esa capacidad no existe o no se puede verificar:

1. Detenerse inmediatamente.
2. No generar imagenes temporales.
3. No ejecutar scripts de generacion por lotes.
4. No modificar la cola ni el manifiesto.
5. No hacer commit de avances simulados.
6. Reportar el bloqueo exacto como `Bloqueado_DriveUpload`.

Esta regla existe para evitar gastar uso/modelo en imagenes que luego no puedan conservarse en Drive.

## Que cuenta como subida valida

Cuenta como subida valida cualquiera de estas opciones:

- Una herramienta de Google Drive que cree/suba un archivo PNG/JPG/WebP crudo en la carpeta destino y devuelva `DriveFileId` o URL directa del archivo.
- Una API/CLI autenticada de Google Drive que cree el archivo binario final en esa carpeta y permita verificarlo con metadatos.
- Una operacion equivalente que deje el archivo final como elemento de Drive independiente, visible en la carpeta `Oloverso`.

## Que NO cuenta como subida valida

No cuenta como subida final:

- Insertar una imagen dentro de un Google Doc.
- Insertar una imagen dentro de una presentacion de Google Slides.
- Poner una formula `IMAGE()` en Google Sheets.
- Guardar solo un enlace temporal local.
- Guardar solo un PNG dentro de GitHub.
- Registrar una URL generada mentalmente sin haberla observado en la respuesta de Drive.

Esas opciones pueden servir para previsualizacion o auditoria, pero no son el archivo final solicitado.

## Si aparece una imagen ya generada de una ejecucion anterior

Solo se puede registrar como `Generada_No_Subida` una imagen que ya exista de una ejecucion anterior interrumpida y que el usuario haya pedido conservar explicitamente. No se debe crear trabajo nuevo en ese estado.

Incluso en ese caso:

1. No marcar el item como `Correcta`.
2. No inventar `DriveFileId` ni `DriveUrl`.
3. Registrar el bloqueo en `Notes` y en el resumen del turno.
4. Priorizar resolver la subida a Drive antes de seguir generando.

Ejemplo para registrar un bloqueo ya existente, no para crear trabajo nuevo:

```powershell
python tools/oloverso_drive_workflow.py record-upload `
  --item-id IMG-00030 `
  --status Bloqueado_DriveUpload `
  --notes "No hay herramienta de subida cruda PNG/JPG a Drive en esta ejecucion."
```

## Objetivo operativo

El objetivo sigue siendo subir todas las imagenes finales a Drive. Esta compuerta existe para evitar falsos positivos y gasto inutil: una imagen no esta terminada hasta que el archivo final esta en Drive y registrado en `06_Registro/Manifest Drive Imagenes Oloverso.csv`.
