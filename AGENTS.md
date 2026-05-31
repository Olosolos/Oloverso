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

If Drive upload is unavailable in the current environment, do not generate new images, do not mark queue items as `Correcta`, and do not create commits that pretend a batch advanced. Stop and report `Bloqueado_DriveUpload`.

## Drive upload validity gate

Read `06_Registro/CAPACIDAD_DRIVE_UPLOAD.md` before planning or generating.

A valid final image upload means a standalone PNG/JPG/WebP file exists as a Drive item in the `Oloverso` folder and its observed `DriveFileId` or URL is stored in the manifest. Inserting an image into a Google Doc, Google Slides deck, or Google Sheet is not a valid final upload for this project. Those can be previews, but they do not satisfy the image-storage requirement.

Preflight is mandatory before generation. The task must verify that it has a real authenticated raw-file upload path for PNG/JPG/WebP into the target Drive folder. If this cannot be verified, stop before `plan`, before generation, before queue edits, and before commit. Do not use `/tmp` generation scripts to create batches that cannot be uploaded.

Never invent Drive URLs or IDs. Only record values returned by a real Drive upload or verified by Drive metadata. `Generada_No_Subida` may only be used to preserve an already-existing interrupted artifact when the user explicitly asks for that; it must not be used as the normal outcome of a new run.

## Work from the repo root

Always treat the repository root as the project root. Do not depend on absolute Windows paths such as `C:\Users\david\...`.

Some CSV fields still contain absolute Windows paths. When running in cloud/worktree, convert them to repo-relative paths by removing everything up to and including `Imagenes Oloverso\`, then replacing backslashes with forward slashes.

Examples:

- `C:\Users\david\OneDrive\Escritorio\Imagenes Oloverso\03_Prompts\x.txt` becomes `03_Prompts/x.txt`.
- `C:\Users\david\OneDrive\Escritorio\Imagenes Oloverso\04_Imagenes_Generadas\x.png` becomes `04_Imagenes_Generadas/x.png`.

## Authoritative queue

Use `06_Registro/Cola Generacion Imagenes Oloverso.csv` as the authoritative queue.

Next item rule:

1. Read `06_Registro/CAPACIDAD_DRIVE_UPLOAD.md` and verify raw Drive upload capability for PNG/JPG/WebP files.
2. If raw Drive upload is unavailable, stop immediately and report `Bloqueado_DriveUpload`; do not generate images or edit records.
3. Read the CSV.
4. Find the first row where `Status` is not `Correcta`.
5. Read its prompt from `PromptPath` after converting to a repo-relative path.
6. Generate one temporary image file.
7. Validate visual coherence and reject bad outputs before upload.
8. Upload the accepted image to the Drive folder `1YFDN7o7yxyTVrH3kaPxHta8HxgOKmk1M`, preserving the block/law folder structure in Drive when possible.
9. Verify the upload is a standalone image file in Drive, then append or update the row in `06_Registro/Manifest Drive Imagenes Oloverso.csv` with `DriveFileId`, `DriveUrl`, filename, status, and notes.
10. Set the queue `Status` to `Correcta` only after Drive upload and manifest update succeed.
11. Refresh `06_Registro/SIGUIENTE_ACCION_GENERAR.txt`, `06_Registro/Tablero Produccion Imagenes Oloverso.md`, and the summary CSV/TXT files.
12. Commit only metadata, manifests, prompts, and records. Do not commit new final PNG/JPG outputs.

Recommended batch size is 1 image until Drive upload has been proven in the current Cloud environment. After repeated successful uploads, unattended cloud work may increase to 3 images per run. The overall objective is all images, but small batches are easier to validate, upload, and recover.

## Drive-first helper

Use `tools/oloverso_drive_workflow.py` for the mechanical parts of the Drive-first workflow.

Common commands:

```powershell
python tools/oloverso_drive_workflow.py plan --limit 1
python tools/oloverso_drive_workflow.py audit
python tools/oloverso_drive_workflow.py record-upload --item-id IMG-00030 --drive-file-id DRIVE_FILE_ID --drive-url DRIVE_URL --local-file path/to/generated.png --notes "Imagen validada y subida a Drive."
```

Read `06_Registro/USO_HELPER_DRIVE_FIRST.md` for the full helper protocol.

The helper does not generate images and does not upload files to Drive. Generate and validate the image first, upload it with a real raw-file Drive upload capability, then call `record-upload` to update queue, manifest, next action, dashboard, summaries, and batch index.

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

Commit small, verifiable increments. A good commit is one completed Drive upload plus the corresponding queue/dashboard/manifest updates.

Do not delete existing generated images unless the task is explicitly a migration and the Drive manifest proves the images were uploaded. Do not rewrite history. Do not mark the overall goal complete until all required images for all laws are generated, uploaded to Drive, recorded, and verified.

## Cloud-first rule

The preferred 24/7 route is Codex Cloud/worktree plus GitHub for control and Google Drive for image storage. Termux/mobile can be a fallback control surface, but it should not be the primary production server.
