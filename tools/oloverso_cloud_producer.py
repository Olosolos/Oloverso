#!/usr/bin/env python3
"""Generate one Oloverso image and upload it to Google Drive.

This is intended for GitHub Actions. It requires:

- OPENAI_API_KEY
- GOOGLE_SERVICE_ACCOUNT_JSON
- The Drive folder shared with the service account email as Editor

It processes one queue item at a time so the repo is always recoverable.
"""
from __future__ import annotations

import argparse
import base64
import json
import os
import subprocess
import tempfile
from datetime import datetime, timezone
from pathlib import Path

from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from openai import OpenAI

DRIVE_FOLDER_ID = "1YFDN7o7yxyTVrH3kaPxHta8HxgOKmk1M"
DRIVE_FOLDER_URL = f"https://drive.google.com/drive/folders/{DRIVE_FOLDER_ID}"
VISUAL_BIBLE = Path("00_Biblia_Visual/Biblia Visual del Oloverso.txt")


def run_json(args: list[str]) -> dict:
    completed = subprocess.run(args, check=True, text=True, capture_output=True)
    return json.loads(completed.stdout)


def run(args: list[str]) -> None:
    subprocess.run(args, check=True)


def require_env(name: str) -> str:
    value = os.environ.get(name, "").strip()
    if not value:
        raise SystemExit(f"Missing required environment variable: {name}")
    return value


def read_text(path: Path, limit: int | None = None) -> str:
    text = path.read_text(encoding="utf-8-sig", errors="replace")
    return text if limit is None else text[:limit]


def build_generation_prompt(item: dict) -> str:
    prompt_path = Path(item["PromptPathRepo"])
    if not prompt_path.exists():
        raise SystemExit(f"Prompt file not found: {prompt_path}")
    prompt = read_text(prompt_path)
    bible = read_text(VISUAL_BIBLE, limit=8000) if VISUAL_BIBLE.exists() else ""
    return f"""Crea una imagen final del Oloverso con calidad alta.

Reglas visuales obligatorias:
- OLO es un stickman blanco luminoso, limpio y elegante.
- Fondo oscuro, sobrio, con energia verde y acentos de pulso amarillo.
- Logo del Oloverso: aro verde luminoso con centro oscuro y onda amarilla.
- Composicion pedagogica, simbolica, clara y premium.
- Sin texto grande legible dentro de la imagen.
- Evitar estilo infantil, anime, meme, horror, gore, caos, colores aleatorios o humanos hiperrealistas.

Biblia visual resumida:
{bible}

Item:
- ItemId: {item.get('ItemId', '')}
- Ley: {item.get('LawNumber', '')} - {item.get('LawTitle', '')}
- Tipo: {item.get('ImageKind', '')}

Prompt especifico:
{prompt}
"""


def generate_image(prompt: str, out_path: Path) -> None:
    client = OpenAI(api_key=require_env("OPENAI_API_KEY"))
    model = os.environ.get("OLOVERSO_IMAGE_MODEL", "gpt-image-1.5")
    quality = os.environ.get("OLOVERSO_IMAGE_QUALITY", "high")
    size = os.environ.get("OLOVERSO_IMAGE_SIZE", "1024x1024")

    response = client.images.generate(
        model=model,
        prompt=prompt,
        size=size,
        quality=quality,
    )

    image_b64 = response.data[0].b64_json
    if not image_b64:
        raise SystemExit("Image API did not return b64_json data.")
    out_path.write_bytes(base64.b64decode(image_b64))


def drive_service():
    raw = require_env("GOOGLE_SERVICE_ACCOUNT_JSON")
    info = json.loads(raw)
    scopes = ["https://www.googleapis.com/auth/drive.file"]
    creds = service_account.Credentials.from_service_account_info(info, scopes=scopes)
    return build("drive", "v3", credentials=creds, cache_discovery=False)


def upload_to_drive(path: Path, name: str, folder_id: str) -> tuple[str, str]:
    service = drive_service()
    metadata = {"name": name, "parents": [folder_id]}
    media = MediaFileUpload(str(path), mimetype="image/png", resumable=True)
    uploaded = service.files().create(
        body=metadata,
        media_body=media,
        fields="id, webViewLink",
        supportsAllDrives=True,
    ).execute()
    file_id = uploaded["id"]
    url = uploaded.get("webViewLink") or f"https://drive.google.com/file/d/{file_id}/view"
    return file_id, url


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--limit", type=int, default=1)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    require_env("OPENAI_API_KEY")
    require_env("GOOGLE_SERVICE_ACCOUNT_JSON")
    folder_id = os.environ.get("OLOVERSO_DRIVE_FOLDER_ID", DRIVE_FOLDER_ID)

    audit = run_json(["python", "tools/oloverso_drive_workflow.py", "audit"])
    print(json.dumps({"pre_audit": audit}, ensure_ascii=False, indent=2))

    plan = run_json(["python", "tools/oloverso_drive_workflow.py", "plan", "--limit", str(args.limit)])
    items = plan.get("items") or []
    if not items:
        print("No pending items.")
        return 0

    item = items[0]
    prompt = build_generation_prompt(item)
    output_name = Path(item.get("FileName") or f"{item['ItemId']}.png").with_suffix(".png").name

    if args.dry_run:
        print(json.dumps({"dry_run_item": item, "output_name": output_name}, ensure_ascii=False, indent=2))
        return 0

    with tempfile.TemporaryDirectory() as tmp:
        out_path = Path(tmp) / output_name
        generate_image(prompt, out_path)
        drive_file_id, drive_url = upload_to_drive(out_path, output_name, folder_id)
        notes = (
            "Generada por GitHub Actions con API de OpenAI, "
            "subida a Drive como PNG independiente y registrada automaticamente."
        )
        run([
            "python",
            "tools/oloverso_drive_workflow.py",
            "record-upload",
            "--item-id",
            item["ItemId"],
            "--drive-file-id",
            drive_file_id,
            "--drive-url",
            drive_url,
            "--local-file",
            str(out_path),
            "--file-name",
            output_name,
            "--status",
            "Correcta",
            "--notes",
            notes,
            "--created-at",
            datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
        ])

    post_audit = run_json(["python", "tools/oloverso_drive_workflow.py", "audit"])
    print(json.dumps({"processed_item": item["ItemId"], "post_audit": post_audit}, ensure_ascii=False, indent=2))
    print(f"Drive folder: {DRIVE_FOLDER_URL}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
