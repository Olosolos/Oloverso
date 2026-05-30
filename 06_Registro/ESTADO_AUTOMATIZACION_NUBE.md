# Estado de automatizacion nube - Oloverso

Fecha: 2026-05-30

## Estado actual

- La automatizacion `Oloverso` esta activa cada hora.
- La automatizacion ya apunta a la carpeta real del proyecto: `C:\Users\david\OneDrive\Escritorio\Imagenes Oloverso`.
- El modo actual sigue siendo `local`, por lo que solo corre si el PC esta encendido.
- Google Drive y GitHub no se pudieron usar desde Codex porque ambos conectores devolvieron `token_expired`.

## Para continuar con el PC apagado

1. Reautenticar el conector de GitHub en Codex.
2. Crear o seleccionar un repositorio GitHub para `Imagenes Oloverso`.
3. Subir este repo local al remoto.
4. Cambiar la automatizacion `Oloverso` de `local` a `worktree` cuando Codex tenga un repo remoto accesible.

## Trabajo horario esperado

La automatizacion debe continuar desde `06_Registro\Cola Generacion Imagenes Oloverso.csv`, generar el siguiente item pendiente, guardar cada salida en su `OutputPath`, actualizar la cola, actualizar `06_Registro\SIGUIENTE_ACCION_GENERAR.txt` y dejar el tablero de produccion al dia.

