# Codex operating guide for Oloverso

This repository is the central source of truth for the Oloverso image-production project.

## Goal

Generate every pending Oloverso law image from the production queue, keep visual coherence with the Oloverso reference style, and update the production records after each completed image.

## Storage model

GitHub is the control plane. Keep prompts, CSV files, manifests, scripts, instructions, dashboards, and small reference assets here.

Google Drive is the image store. Final generated image files must be exported to the shared Drive folder below instead of being added to GitHub at scale:

- Drive folder name: `Oloverso`
- Drive folder ID: `1YFDN7o7yxyTVrH3kaPxHta8HxgOKmk1M`
- Drive folder URL: `https://drive.google.com/drive/folders/1YFDN7o7yxyTVrH3kaPxHta8HxgOKmk1M`

Do not add new bulk PNG/JPG outputs to GitHub. Existing tracked images may remain until a deliberate migration removes them from Git history or replaces them with Drive manifest records. New generated outputs should be temporary local artifacts, uploaded to Drive, recorded in `06_Registro/Manifest Drive Imagenes Oloverso.csv`, and then left out of Git commits.

If Drive upload is unavailable in the current environment, do not mark the queue item as `Correcta`. Use a clear temporary status such as `Pendiente_Drive` or `Generada_No_Subida`, record the blocker, and stop before claiming completion for that item.

## Work from the repo root

Always treat the repository root as the project root. Do not depend on absolute Windows paths such as `C:\Users\david\...`.

Some CSV fields still contain absolute Windows paths. When running in cloud/worktree, convert them to repo-relative paths by removing everything up to and including `Imagenes Oloverso\`, then replacing backslashes with forward slashes.

Examples:

- `C:\Users\david\OneDrive\Escritorio\Imagenes Oloverso\03_Prompts\x.txt` becomes `03_Prompts/x.txt`.
- `C:\Users\david\OneDrive\Escritorio\Imagenes Oloverso\04_Imagenes_Generadas\x.png` becomes `04_Imagenes_Generadas/x.png`.

## Authoritative queue

Use `06_Registro/Cola Generacion Imagenes Oloverso.csv` as the authoritative queue.

Next item rule:

1. Read the CSV.
2. Find the first row where `Status` is not `Correcta`.
3. Read its prompt from `PromptPath` after converting to a repo-relative path.
4. Generate a temporary image file.
5. Validate visual coherence and reject bad outputs before upload.
6. Upload the accepted image to the Drive folder `1YFDN7o7yxyTVrH3kaPxHta8HxgOKmk1M`, preserving the block/law folder structure in Drive when possible.
7. Compute or record the best available checksum/identifier, then append or update the row in `06_Registro/Manifest Drive Imagenes Oloverso.csv` with `DriveFileId`, `DriveUrl`, filename, status, and notes.
8. Set the queue `Status` to `Correcta` only after Drive upload and manifest update succeed.
9. Refresh `06_Registro/SIGUIENTE_ACCION_GENERAR.txt`, `06_Registro/Tablero Produccion Imagenes Oloverso.md`, and the summary CSV/TXT files.
10. Commit only metadata, manifests, prompts, and records. Do not commit new final PNG/JPG outputs.

Recommended batch size for unattended cloud work is 3 to 10 images per run. The overall objective is all images, but small batches are easier to validate, upload, and recover.

## Visual coherence

Maintain absolute coherence with the Biblia Visual del Oloverso:

- OLO is the main luminous white stickman guide.
- The Oloverso logo is a luminous green ring with a dark center and yellow waveform pulse.
- Use dark elegant backgrounds, green energy, yellow pulse accents, and clean symbolic compositions.
- Avoid cheap childish style, anime, hyperrealistic humans, meme aesthetics, random colors, chaos, gore, horror, and altered logos.
- Avoid large readable text inside generated images.

Reference assets:

- `01_Personajes/Referencia Personajes Oloverso.png`
- `02_Logo_Oloverso/Logo Oloverso - Referencia.jpeg`
- `00_Biblia_Visual/Biblia Visual del Oloverso.txt`

## Prompt text quality

Some prompt files contain mojibake text such as `atenci\u00c3\u00b3n`. When generating an image, silently normalize those strings into correct Spanish meaning in the generation prompt. Do not stop solely because of mojibake.

## Git discipline

Commit small, verifiable increments. A good commit is one completed batch of Drive uploads plus the corresponding queue/dashboard/manifest updates.

Do not delete existing generated images unless the task is explicitly a migration and the Drive manifest proves the images were uploaded. Do not rewrite history. Do not mark the overall goal complete until all required images for all laws are generated, uploaded to Drive, recorded, and verified.

## Cloud-first rule

The preferred 24/7 route is Codex Cloud/worktree plus GitHub for control and Google Drive for image storage. Termux/mobile can be a fallback control surface, but it should not be the primary production server.
