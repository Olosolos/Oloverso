# Uso del helper Drive-first

Helper: `tools/oloverso_drive_workflow.py`

Este script mantiene consistente la parte mecanica del flujo Drive-first. No genera imagenes y no sube archivos a Drive. Codex debe generar, validar visualmente y subir a Drive con una herramienta real de subida de archivo crudo; despues usa este helper para registrar el resultado.

Lee tambien `06_Registro/CAPACIDAD_DRIVE_UPLOAD.md` antes de marcar cualquier item como `Correcta`.

## 1. Ver siguiente lote pendiente

```powershell
python tools/oloverso_drive_workflow.py plan --limit 5
```

Devuelve JSON con:

- `ItemId`
- `PromptPathRepo`
- `OutputPathRepo`
- `DriveFolderId`
- `DriveSuggestedPath`
- `FileName`

## 2. Generar y subir a Drive

Para cada item del plan:

1. Lee `PromptPathRepo`.
2. Normaliza mojibake mentalmente si aparece.
3. Genera imagen temporal.
4. Valida coherencia visual del Oloverso.
5. Sube la imagen final correcta a Google Drive como archivo independiente PNG/JPG/WebP:
   - Folder ID: `1YFDN7o7yxyTVrH3kaPxHta8HxgOKmk1M`
   - URL: `https://drive.google.com/drive/folders/1YFDN7o7yxyTVrH3kaPxHta8HxgOKmk1M`
6. Conserva el `DriveFileId` y `DriveUrl` devueltos por Drive.

No cuenta como subida final insertar una imagen en Docs, Slides o Sheets. Esas rutas pueden servir de vista previa, pero no cumplen el almacenamiento final del proyecto.

## 3. Registrar upload correcto

```powershell
python tools/oloverso_drive_workflow.py record-upload `
  --item-id IMG-00030 `
  --drive-file-id DRIVE_FILE_ID_AQUI `
  --drive-url DRIVE_URL_AQUI `
  --local-file "ruta/local/temporal.png" `
  --notes "Imagen validada y subida a Drive."
```

Esto actualiza:

- `06_Registro/Cola Generacion Imagenes Oloverso.csv`
- `06_Registro/Manifest Drive Imagenes Oloverso.csv`
- `06_Registro/SIGUIENTE_ACCION_GENERAR.txt`
- `06_Registro/Tablero Produccion Imagenes Oloverso.md`
- `06_Registro/Resumen Cola Generacion Imagenes Oloverso.txt`
- `06_Registro/Resumen Produccion por Bloques.csv`
- `06_Registro/Indice Lotes Generacion Oloverso.csv`

## 4. Si Drive falla o no hay upload crudo

No marques el item como `Correcta`. Registra el bloqueo asi:

```powershell
python tools/oloverso_drive_workflow.py record-upload `
  --item-id IMG-00030 `
  --status Pendiente_Drive `
  --notes "Drive no permitio subir un archivo PNG/JPG/WebP crudo en esta ejecucion; falta permiso o herramienta de upload."
```

## 5. Auditar consistencia

```powershell
python tools/oloverso_drive_workflow.py audit
```

El audit informa cuantos items `Correcta` aun no tienen fila correcta en el manifiesto Drive. Durante la migracion inicial puede haber correctas antiguas sin manifiesto; las nuevas deben quedar siempre registradas.

## 6. Commit esperado

Despues de registrar un lote:

```powershell
git status --short
git add 06_Registro tools AGENTS.md .gitignore
git commit -m "Record Oloverso Drive image batch"
git push
```

No anadir PNG/JPG finales al commit. Las imagenes finales viven en Drive.
