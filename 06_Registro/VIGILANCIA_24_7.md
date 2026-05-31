# Vigilancia 24/7 del Oloverso

Fecha: 2026-05-31

## Objetivo

Mantener una supervision horaria del proyecto aunque el PC local este apagado.

## Componentes activos

1. GitHub Actions: `.github/workflows/oloverso-watchdog.yml`
   - Se ejecuta cada hora.
   - Audita la cola y los registros con `tools/oloverso_drive_workflow.py audit`.
   - Comprueba que las compuertas Drive-first siguen presentes.
   - No genera imagenes.
   - No sube archivos a Drive.
   - No modifica el repositorio.

2. Codex Cloud production task
   - Debe ejecutarse aparte desde Codex Cloud.
   - Debe usar modelo alto disponible en la interfaz, preferiblemente GPT-5.5 Codex con razonamiento alto si aparece en el selector.
   - Debe leer `AGENTS.md` y `06_Registro/CAPACIDAD_DRIVE_UPLOAD.md` antes de generar.
   - Debe detenerse con `Bloqueado_DriveUpload` si no puede subir PNG/JPG/WebP crudos a Drive.

## Prompt recomendado para produccion Cloud

```text
Trabaja en Codex Cloud sobre Olosolos/Oloverso.

Configura la tarea con el modelo mas alto disponible. Si el selector ofrece GPT-5.5 Codex, usa GPT-5.5 Codex. Usa razonamiento alto.

Antes de generar cualquier imagen, lee AGENTS.md y 06_Registro/CAPACIDAD_DRIVE_UPLOAD.md.

Primero verifica si tienes una herramienta real y autenticada para subir PNG/JPG/WebP crudos como archivos independientes a Google Drive, carpeta Oloverso, folder ID 1YFDN7o7yxyTVrH3kaPxHta8HxgOKmk1M.

Si no tienes subida cruda real a Drive, detente inmediatamente con Bloqueado_DriveUpload. No generes imagenes, no modifiques cola/manifiesto, no hagas commit.

Si si tienes subida real a Drive, procesa solo 1 imagen:
python tools/oloverso_drive_workflow.py audit
python tools/oloverso_drive_workflow.py plan --limit 1

Genera, valida visualmente, sube a Drive, registra con record-upload, ejecuta audit y haz commit/push solo de metadatos.

En el resumen dime el modelo/entorno visible, el item procesado, el DriveFileId/DriveUrl real y el commit SHA.
```

## Como comprobar la vigilancia

En GitHub:

1. Abrir `Olosolos/Oloverso`.
2. Entrar en `Actions`.
3. Abrir el workflow `Oloverso watchdog`.
4. Comprobar que la ultima ejecucion esta en verde.
5. Si esta en rojo, abrir el log y resolver el bloqueo antes de lanzar mas produccion Cloud.

## Limitacion importante

La vigilancia de GitHub Actions confirma el estado del repositorio y las reglas de seguridad. No reemplaza a la tarea de produccion de Codex Cloud y no puede subir imagenes a Drive por si sola sin credenciales/API de Google Drive configuradas como secreto de GitHub.
