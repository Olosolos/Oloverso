# Capacidad requerida para subir imagenes a Drive

Fecha: 2026-05-31

## Regla

Una imagen del Oloverso solo puede marcarse como `Correcta` bajo el flujo Drive-first cuando existe un archivo final de imagen en Google Drive y el manifiesto contiene un identificador verificable de ese archivo.

Destino oficial:

- Carpeta: `Oloverso`
- Folder ID: `1YFDN7o7yxyTVrH3kaPxHta8HxgOKmk1M`
- URL: `https://drive.google.com/drive/folders/1YFDN7o7yxyTVrH3kaPxHta8HxgOKmk1M`

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

## Si no hay herramienta de subida cruda disponible

Si la ejecucion actual no tiene una herramienta real para subir PNG/JPG/WebP a Drive:

1. Genera y valida la imagen solo si tiene sentido conservar el avance temporal.
2. No marques el item como `Correcta`.
3. Usa `Pendiente_Drive` o `Generada_No_Subida` en la cola.
4. Registra el bloqueo en `Notes` y en el resumen del turno.
5. No inventes `DriveFileId` ni `DriveUrl`.

Ejemplo:

```powershell
python tools/oloverso_drive_workflow.py record-upload `
  --item-id IMG-00030 `
  --status Pendiente_Drive `
  --notes "No hay herramienta de subida cruda PNG/JPG a Drive en esta ejecucion."
```

## Objetivo operativo

El objetivo sigue siendo subir todas las imagenes finales a Drive. Esta compuerta existe para evitar falsos positivos: una imagen no esta terminada hasta que el archivo final esta en Drive y registrado en `06_Registro/Manifest Drive Imagenes Oloverso.csv`.
