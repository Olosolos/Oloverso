# Estado de automatizacion nube - Oloverso

Fecha: 2026-05-31

## Estado actual

- El repositorio GitHub central existe y responde: `https://github.com/Olosolos/Oloverso.git`.
- Codex tiene permisos sobre `Olosolos/Oloverso` mediante el conector GitHub.
- La rama principal es `main`.
- El repositorio remoto contiene la cola, prompts, registros, referencias y las imagenes generadas hasta el estado actual.
- La automatizacion `Oloverso` esta configurada como `worktree`.
- El siguiente item remoto registrado es `IMG-00027`, Ley 0006, Principio 1.
- Google Drive sigue siendo opcional/secundario; la via principal para trabajar con el PC apagado debe ser GitHub + Codex worktree/cloud.

## Decision recomendada

Usar Codex Cloud/worktree + GitHub como sistema principal 24/7.

No usar Termux/movil como servidor principal salvo emergencia. Termux depende de bateria, red movil, gestion agresiva de procesos de Android y credenciales locales; es mas fragil que una ejecucion cloud/worktree.

## Condiciones para que funcione con el PC apagado

1. El repo remoto `Olosolos/Oloverso` debe ser la fuente central de verdad.
2. Codex debe ejecutar la automatizacion contra un worktree del repo, no contra archivos que solo existan en el PC.
3. Las instrucciones deben usar rutas relativas al repo.
4. Las rutas Windows dentro del CSV deben convertirse mentalmente o por herramienta a rutas relativas antes de leer/escribir archivos.
5. Cada avance debe terminar con commit en `main` o en una rama de trabajo que luego se integre.

## Trabajo horario esperado

La automatizacion debe continuar desde `06_Registro/Cola Generacion Imagenes Oloverso.csv`:

1. Buscar el primer item donde `Status` no sea `Correcta`.
2. Leer el prompt indicado por `PromptPath`, convirtiendo rutas Windows a rutas relativas.
3. Generar la imagen con coherencia visual del Oloverso.
4. Guardar la salida en el `OutputPath`, tambien convertido a ruta relativa.
5. Actualizar cola, siguiente accion, tablero y resumenes.
6. Hacer commit del avance.

## Archivos clave

- `AGENTS.md`: guia principal para Codex en cloud/worktree.
- `06_Registro/Cola Generacion Imagenes Oloverso.csv`: cola de produccion.
- `06_Registro/SIGUIENTE_ACCION_GENERAR.txt`: siguiente accion humana/automatica.
- `06_Registro/Tablero Produccion Imagenes Oloverso.md`: tablero de estado.
- `01_Personajes/Referencia Personajes Oloverso.png`: referencia visual.
