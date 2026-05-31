# Instrucciones para Codex Cloud - Oloverso Drive-first

Usa este texto como prompt para Codex Cloud o para cualquier automatizacion cloud/worktree del proyecto.

```text
Trabaja sobre el repositorio GitHub Olosolos/Oloverso.

Objetivo: continuar el proyecto Oloverso generando TODAS las imagenes pendientes de las leyes, con la misma coherencia visual ya definida: OLO como guia stickman luminoso, fondo oscuro elegante, energia verde del Oloverso, pulso amarillo, logo integrado como aro verde con onda amarilla, composicion pedagogica sin texto grande.

Regla de almacenamiento:
- GitHub NO debe almacenar las imagenes finales masivamente.
- GitHub solo debe guardar prompts, CSV, registros, tablero, scripts y manifiestos.
- Todas las imagenes generadas deben subirse a Google Drive en la carpeta compartida:
  Nombre: Oloverso
  Folder ID: 1YFDN7o7yxyTVrH3kaPxHta8HxgOKmk1M
  URL: https://drive.google.com/drive/folders/1YFDN7o7yxyTVrH3kaPxHta8HxgOKmk1M

Primero lee AGENTS.md. Despues:
1. Lee 06_Registro/Cola Generacion Imagenes Oloverso.csv.
2. Lee o crea 06_Registro/Manifest Drive Imagenes Oloverso.csv.
3. Busca el primer item donde Status no sea Correcta.
4. Genera un lote pequeno de 3 a 10 imagenes.
5. Valida visualmente cada imagen.
6. Sube cada imagen correcta a Google Drive dentro de la carpeta Oloverso, manteniendo subcarpetas por bloque y ley cuando sea posible.
7. Registra DriveFileId, DriveUrl, FileName, SHA256 si esta disponible, Status, Notes y CreatedAt en el manifiesto.
8. Marca Correcta en la cola solo despues de que la imagen este subida a Drive y registrada.
9. Actualiza SIGUIENTE_ACCION_GENERAR.txt, Tablero Produccion Imagenes Oloverso.md, resumenes e indice de lotes.
10. Haz commit y push a GitHub solo con metadatos/registros. No subas PNG/JPG finales al repo.

Si Google Drive no permite subir archivos en la ejecucion actual, no marques el item como Correcta. Usa Pendiente_Drive o Generada_No_Subida y reporta el bloqueo exacto.
```

## Prompt corto para la automatizacion horaria

```text
Continua el proyecto Oloverso desde Olosolos/Oloverso. Lee AGENTS.md primero.

Toma el siguiente lote pendiente de 3 a 10 imagenes desde 06_Registro/Cola Generacion Imagenes Oloverso.csv. Genera, valida y sube cada imagen correcta a Google Drive en la carpeta Oloverso, folder ID 1YFDN7o7yxyTVrH3kaPxHta8HxgOKmk1M. No guardes PNG/JPG finales en GitHub. Actualiza cola, Manifest Drive Imagenes Oloverso.csv, tablero, resumenes y SIGUIENTE_ACCION_GENERAR.txt. Haz commit y push solo de metadatos/registros. Manten coherencia visual total del Oloverso.
```
