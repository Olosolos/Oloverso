# Estado de automatizacion nube - Oloverso

Fecha: 2026-05-31

## Estado actual

- El repositorio GitHub central existe y responde: `https://github.com/Olosolos/Oloverso.git`.
- Codex tiene permisos sobre `Olosolos/Oloverso` mediante el conector GitHub.
- La rama principal es `main`.
- La automatizacion `Oloverso` esta configurada como `worktree`.
- La carpeta compartida de Google Drive para imagenes existe y responde:
  - Nombre: `Oloverso`
  - Folder ID: `1YFDN7o7yxyTVrH3kaPxHta8HxgOKmk1M`
  - URL: `https://drive.google.com/drive/folders/1YFDN7o7yxyTVrH3kaPxHta8HxgOKmk1M`
- GitHub debe usarse como plano de control: prompts, cola, tablero, registros, scripts y manifiestos.
- Google Drive debe usarse como almacen masivo de imagenes finales.
- El siguiente item remoto registrado antes de la migracion Drive-first era `IMG-00027`, Ley 0006, Principio 1. Algunos worktrees locales pueden tener avances pendientes no empujados; antes de continuar deben hacer fetch/rebase y conservar cualquier avance valido.

## Decision recomendada

Usar Codex Cloud/worktree + GitHub + Google Drive como sistema principal 24/7:

1. Codex Cloud ejecuta el trabajo incluso con el PC apagado.
2. GitHub mantiene el estado verificable y versionado.
3. Google Drive almacena todas las imagenes finales para evitar saturar GitHub con miles de PNG/JPG.

No usar Termux/movil como servidor principal salvo emergencia. Termux depende de bateria, red movil, gestion agresiva de procesos de Android y credenciales locales; es mas fragil que una ejecucion cloud/worktree.

## Condiciones para que funcione con el PC apagado

1. El repo remoto `Olosolos/Oloverso` debe ser la fuente central de verdad para cola, prompts y registros.
2. Codex debe ejecutar la automatizacion contra un worktree del repo, no contra archivos que solo existan en el PC.
3. Las instrucciones deben usar rutas relativas al repo.
4. Las rutas Windows dentro del CSV deben convertirse mentalmente o por herramienta a rutas relativas antes de leer archivos.
5. Las imagenes finales deben subirse a Google Drive, carpeta `Oloverso`, folder ID `1YFDN7o7yxyTVrH3kaPxHta8HxgOKmk1M`.
6. Cada avance debe terminar con commit en `main` o en una rama de trabajo que luego se integre, pero el commit debe contener metadatos/registros, no nuevos PNG/JPG masivos.

## Trabajo horario esperado

La automatizacion debe continuar desde `06_Registro/Cola Generacion Imagenes Oloverso.csv`:

1. Buscar el primer item donde `Status` no sea `Correcta`.
2. Leer el prompt indicado por `PromptPath`, convirtiendo rutas Windows a rutas relativas.
3. Generar la imagen con coherencia visual del Oloverso.
4. Validar visualmente la imagen generada.
5. Subir la imagen correcta a Google Drive en la carpeta `Oloverso`.
6. Registrar `DriveFileId`, `DriveUrl`, filename, checksum si esta disponible, estado y notas en `06_Registro/Manifest Drive Imagenes Oloverso.csv`.
7. Marcar `Correcta` en la cola solo despues de la subida a Drive y el registro en el manifiesto.
8. Actualizar siguiente accion, tablero y resumenes.
9. Hacer commit del avance con solo metadatos/registros.

## Archivos clave

- `AGENTS.md`: guia principal para Codex en cloud/worktree.
- `06_Registro/Cola Generacion Imagenes Oloverso.csv`: cola de produccion.
- `06_Registro/Manifest Drive Imagenes Oloverso.csv`: indice de imagenes finales subidas a Drive.
- `06_Registro/SIGUIENTE_ACCION_GENERAR.txt`: siguiente accion humana/automatica.
- `06_Registro/Tablero Produccion Imagenes Oloverso.md`: tablero de estado.
- `06_Registro/INSTRUCCIONES_CODEX_CLOUD_DRIVE.md`: prompt operativo para Codex Cloud.
- `01_Personajes/Referencia Personajes Oloverso.png`: referencia visual.

## Nota de capacidad

GitHub no es el destino correcto para 20.000 imagenes finales. El repositorio debe mantenerse ligero y auditable; Drive debe contener los binarios finales.
