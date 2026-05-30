# Estado de automatizacion nube - Oloverso

Fecha: 2026-05-30

## Estado actual

- La automatizacion `Oloverso` esta activa cada hora.
- La automatizacion ya apunta a la carpeta real del proyecto: `C:\Users\david\OneDrive\Escritorio\Imagenes Oloverso`.
- El modo actual es `worktree`.
- El repositorio local esta inicializado en Git y tiene `origin` apuntando a `https://github.com/Olosolos/Oloverso.git`.
- El remoto GitHub responde por HTTPS, pero no hay credenciales GitHub guardadas para poder hacer `git push`.
- El conector GitHub de Codex devolvio `token_expired` al consultar `Olosolos/Oloverso`.
- Google Drive tambien devolvio `token_expired`.

## Para continuar con el PC apagado

1. Reautenticar el conector de GitHub en Codex o iniciar sesion en Git Credential Manager.
2. Ejecutar `git push -u origin main` desde `C:\Users\david\OneDrive\Escritorio\Imagenes Oloverso`.
3. Verificar que GitHub muestre la rama `main`.
4. Mantener la automatizacion `Oloverso` en modo `worktree`.

## Trabajo horario esperado

La automatizacion debe continuar desde `06_Registro\Cola Generacion Imagenes Oloverso.csv`, generar el siguiente item pendiente, guardar cada salida en su `OutputPath`, actualizar la cola, actualizar `06_Registro\SIGUIENTE_ACCION_GENERAR.txt` y dejar el tablero de produccion al dia.
