# Codex operating guide for Oloverso

This repository is the central source of truth for the Oloverso image-production project.

## Goal

Generate every pending Oloverso law image from the production queue, keep visual coherence with the Oloverso reference style, and update the production records after each completed image.

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
4. Generate the image.
5. Save the PNG to `OutputPath` after converting to a repo-relative path.
6. Set `Status` to `Correcta` and update `Notes` with a concise description and date.
7. Refresh `06_Registro/SIGUIENTE_ACCION_GENERAR.txt`, `06_Registro/Tablero Produccion Imagenes Oloverso.md`, and the summary CSV/TXT files.
8. Commit the completed image plus record updates.

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

Some prompt files contain mojibake text such as `atenciÃ³n`. When generating an image, silently normalize those strings into correct Spanish meaning in the generation prompt. Do not stop solely because of mojibake.

## Git discipline

Commit small, verifiable increments. A good commit is one completed image or one completed law plus the corresponding queue/dashboard updates.

Do not delete existing generated images. Do not rewrite history. Do not mark the overall goal complete until all required images for all laws are generated, saved, recorded, and verified.

## Cloud-first rule

The preferred 24/7 route is Codex Cloud/worktree plus GitHub. Termux/mobile can be a fallback control surface, but it should not be the primary production server.
