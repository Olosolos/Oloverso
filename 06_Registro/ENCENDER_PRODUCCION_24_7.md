# Encender produccion 24/7 del Oloverso

Fecha: 2026-05-31

## Que queda preparado

El repositorio ya contiene una produccion horaria en GitHub Actions:

- Workflow: `.github/workflows/oloverso-producer.yml`
- Script: `tools/oloverso_cloud_producer.py`
- Dependencias: `requirements-oloverso-cloud.txt`

Este flujo:

1. Lee la cola.
2. Toma 1 imagen pendiente.
3. Genera con la API de imagenes de OpenAI.
4. Sube el PNG a Google Drive.
5. Registra `DriveFileId` y `DriveUrl`.
6. Marca `Correcta` solo si la subida a Drive funciono.
7. Hace commit solo de metadatos en `06_Registro`.

## Paso 1: crear credencial de Google Drive

1. Entra en Google Cloud Console.
2. Crea o usa un proyecto.
3. Activa `Google Drive API`.
4. Crea una `Service Account`.
5. Crea una clave JSON para esa service account.
6. Copia el email de la service account.
7. Abre la carpeta Drive `Oloverso`.
8. Comparte la carpeta con el email de la service account como `Editor`.

Carpeta destino:

- Folder ID: `1YFDN7o7yxyTVrH3kaPxHta8HxgOKmk1M`
- URL: `https://drive.google.com/drive/folders/1YFDN7o7yxyTVrH3kaPxHta8HxgOKmk1M`

## Paso 2: anadir secretos en GitHub

En GitHub repo `Olosolos/Oloverso`:

1. `Settings`
2. `Secrets and variables`
3. `Actions`
4. `New repository secret`

Crear estos secrets:

- `OPENAI_API_KEY`: tu API key de OpenAI.
- `GOOGLE_SERVICE_ACCOUNT_JSON`: el contenido completo del JSON de la service account de Google.

## Paso 3: anadir variables en GitHub

En la misma pantalla, pestana `Variables`, crear:

- `OLOVERSO_PRODUCER_ENABLED` = `true`
- `OLOVERSO_DRIVE_FOLDER_ID` = `1YFDN7o7yxyTVrH3kaPxHta8HxgOKmk1M`
- `OLOVERSO_IMAGE_MODEL` = `gpt-image-1.5`
- `OLOVERSO_IMAGE_QUALITY` = `high`
- `OLOVERSO_IMAGE_SIZE` = `1024x1024`

Si tu cuenta/API no tiene `gpt-image-1.5`, cambia `OLOVERSO_IMAGE_MODEL` al modelo de imagen que OpenAI te permita usar.

## Paso 4: probar manualmente

1. GitHub repo `Olosolos/Oloverso`.
2. `Actions`.
3. Workflow `Oloverso producer`.
4. `Run workflow`.
5. Dejar `limit = 1`.
6. Ejecutar.

Si sale verde:

- Abrir la carpeta Drive `Oloverso` y comprobar que aparecio el PNG.
- Comprobar que `06_Registro/Manifest Drive Imagenes Oloverso.csv` tiene `DriveFileId` y `DriveUrl`.
- Comprobar que la cola marco ese item como `Correcta`.

## Paso 5: dejarlo 24/7

Cuando la prueba manual este verde, el workflow ya correra cada hora por horario.

Mantener `limit = 1` hasta que haya varias ejecuciones correctas. Despues se puede subir con cuidado.

## Papel de Codex Cloud

Codex Cloud no debe ser el motor principal de subida a Drive mientras no tenga herramienta cruda de upload PNG/JPG/WebP. Su papel recomendado es:

- Revisar logs.
- Mejorar prompts/scripts.
- Corregir fallos del workflow.
- Auditar calidad.

La produccion 24/7 real queda en GitHub Actions porque funciona aunque el PC este apagado.
