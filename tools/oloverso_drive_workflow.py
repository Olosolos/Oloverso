#!/usr/bin/env python3
"""Drive-first helper for the Oloverso image production queue.

This script intentionally does not generate images and does not upload files to
Drive. Codex performs those steps with the available image and Drive tools, then
uses this helper to keep queue, manifest, next-action, dashboard, and summary
files consistent.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import sys
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path

DRIVE_FOLDER_ID = "1YFDN7o7yxyTVrH3kaPxHta8HxgOKmk1M"
DRIVE_FOLDER_URL = "https://drive.google.com/drive/folders/1YFDN7o7yxyTVrH3kaPxHta8HxgOKmk1M"
REGISTRY_DIR = Path("06_Registro")
QUEUE_PATH = REGISTRY_DIR / "Cola Generacion Imagenes Oloverso.csv"
MANIFEST_PATH = REGISTRY_DIR / "Manifest Drive Imagenes Oloverso.csv"
NEXT_ACTION_PATH = REGISTRY_DIR / "SIGUIENTE_ACCION_GENERAR.txt"
DASHBOARD_PATH = REGISTRY_DIR / "Tablero Produccion Imagenes Oloverso.md"
QUEUE_SUMMARY_PATH = REGISTRY_DIR / "Resumen Cola Generacion Imagenes Oloverso.txt"
BLOCK_SUMMARY_PATH = REGISTRY_DIR / "Resumen Produccion por Bloques.csv"
BATCH_INDEX_PATH = REGISTRY_DIR / "Indice Lotes Generacion Oloverso.csv"

MANIFEST_FIELDS = [
    "ItemId",
    "LawNumber",
    "LawTitle",
    "ImageKind",
    "PromptPath",
    "DriveFolderId",
    "DriveFileId",
    "DriveUrl",
    "FileName",
    "SHA256",
    "Status",
    "Notes",
    "CreatedAt",
]


def normalize_repo_path(value: str | None) -> str:
    """Convert Windows project paths to repo-relative POSIX-style paths."""
    if not value:
        return ""
    path = str(value).strip().strip('"').replace("\\", "/")
    marker = "imagenes oloverso/"
    lower = path.lower()
    idx = lower.rfind(marker)
    if idx != -1:
        path = path[idx + len(marker) :]
    while path.startswith("./") or path.startswith("/"):
        if path.startswith("./"):
            path = path[2:]
        elif path.startswith("/"):
            path = path[1:]
    return path


def read_csv(path: Path) -> tuple[list[str], list[dict[str, str]]]:
    if not path.exists():
        return [], []
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        return list(reader.fieldnames or []), [dict(row) for row in reader]


def write_csv(path: Path, fieldnames: list[str], rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=fieldnames,
            extrasaction="ignore",
            quoting=csv.QUOTE_ALL,
            lineterminator="\n",
        )
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in fieldnames})


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def status_of(row: dict[str, str]) -> str:
    return (row.get("Status") or "").strip()


def is_correct(row: dict[str, str]) -> bool:
    return status_of(row).lower() == "correcta"


def output_path_for(row: dict[str, str]) -> str:
    output_path = normalize_repo_path(row.get("OutputPath"))
    if output_path:
        return output_path
    folder = normalize_repo_path(row.get("OutputFolder"))
    filename = row.get("OutputFilename") or row.get("FileName") or ""
    return str(Path(folder) / filename).replace("\\", "/") if filename else folder


def prompt_path_for(row: dict[str, str]) -> str:
    return normalize_repo_path(row.get("PromptPath"))


def file_name_for(row: dict[str, str]) -> str:
    return row.get("OutputFilename") or Path(output_path_for(row)).name


def queue_item_payload(row: dict[str, str]) -> dict[str, str]:
    return {
        "ItemId": row.get("ItemId", ""),
        "Batch": row.get("Batch", ""),
        "Block": row.get("Block", ""),
        "LawNumber": row.get("LawNumber", ""),
        "LawTitle": row.get("LawTitle", ""),
        "ImageKind": row.get("ImageKind", ""),
        "Status": status_of(row),
        "PromptPathRepo": prompt_path_for(row),
        "OutputPathRepo": output_path_for(row),
        "DriveFolderId": DRIVE_FOLDER_ID,
        "DriveSuggestedPath": output_path_for(row),
        "FileName": file_name_for(row),
    }


def read_text(path: Path, limit: int | None = None) -> str:
    if not path.exists():
        return ""
    text = path.read_text(encoding="utf-8-sig", errors="replace")
    return text if limit is None else text[:limit]


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def ensure_manifest_fields(fieldnames: list[str]) -> list[str]:
    merged = list(fieldnames)
    for field in MANIFEST_FIELDS:
        if field not in merged:
            merged.append(field)
    return merged or list(MANIFEST_FIELDS)


def upsert_by_item(rows: list[dict[str, str]], new_row: dict[str, str]) -> list[dict[str, str]]:
    item_id = new_row.get("ItemId", "")
    updated = False
    result = []
    for row in rows:
        if row.get("ItemId") == item_id:
            merged = dict(row)
            merged.update(new_row)
            result.append(merged)
            updated = True
        else:
            result.append(row)
    if not updated:
        result.append(new_row)
    return result


def first_pending(rows: list[dict[str, str]]) -> dict[str, str] | None:
    for row in rows:
        if not is_correct(row):
            return row
    return None


def block_summary(rows: list[dict[str, str]]) -> list[dict[str, str]]:
    grouped: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in rows:
        grouped[row.get("Block", "Sin bloque")].append(row)
    output = []
    for block, items in grouped.items():
        laws = [row.get("LawNumber", "") for row in items if row.get("LawNumber")]
        law_range = "-"
        if laws:
            law_range = f"{min(laws)}-{max(laws)}"
        kinds = [row.get("ImageKind", "").lower() for row in items]
        output.append(
            {
                "Bloque": block,
                "Leyes": law_range,
                "Items": str(len(items)),
                "General": str(sum("imagen general" in kind for kind in kinds)),
                "Principios": str(sum("principio" in kind for kind in kinds)),
                "Apartados": str(sum("apartado" in kind for kind in kinds)),
                "Pendientes": str(sum(not is_correct(row) for row in items)),
                "Correctas": str(sum(is_correct(row) for row in items)),
            }
        )
    return output


def batch_summary(rows: list[dict[str, str]]) -> list[dict[str, str]]:
    grouped: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in rows:
        grouped[row.get("Batch", "Sin lote")].append(row)
    output = []
    for batch, items in grouped.items():
        laws = [row.get("LawNumber", "") for row in items if row.get("LawNumber")]
        output.append(
            {
                "Batch": batch,
                "Count": str(len(items)),
                "FirstItem": items[0].get("ItemId", "") if items else "",
                "LastItem": items[-1].get("ItemId", "") if items else "",
                "FirstLaw": min(laws) if laws else "",
                "LastLaw": max(laws) if laws else "",
                "FirstKind": items[0].get("ImageKind", "") if items else "",
                "LastKind": items[-1].get("ImageKind", "") if items else "",
                "Pending": str(sum(not is_correct(row) for row in items)),
                "Correct": str(sum(is_correct(row) for row in items)),
            }
        )
    return output


def refresh_next_action(root: Path, queue_rows: list[dict[str, str]]) -> None:
    today = datetime.now().date().isoformat()
    pending = first_pending(queue_rows)
    if pending is None:
        NEXT_ACTION_PATH.joinpath().parent.mkdir(parents=True, exist_ok=True)
        (root / NEXT_ACTION_PATH).write_text(
            f"SIGUIENTE ACCION - OLOVERSO\nFecha: {today}\n\nNo quedan items pendientes en la cola.\n",
            encoding="utf-8",
        )
        return

    prompt_rel = prompt_path_for(pending)
    output_rel = output_path_for(pending)
    prompt_text = read_text(root / prompt_rel, limit=20000)
    body = [
        "SIGUIENTE ACCION - OLOVERSO",
        f"Fecha: {today}",
        "",
        "Generar ahora el siguiente item pendiente:",
        f"Item: {pending.get('ItemId', '')}",
        f"Lote: {pending.get('Batch', '')}",
        f"Tipo: {pending.get('ImageKind', '')}",
        f"Ley: {pending.get('LawNumber', '')} - {pending.get('LawTitle', '')}",
        f"Prompt repo-relativo: {prompt_rel}",
        f"Archivo temporal sugerido: {output_rel}",
        f"Destino Drive folder ID: {DRIVE_FOLDER_ID}",
        f"Destino Drive URL: {DRIVE_FOLDER_URL}",
        "",
        "Prompt completo para generacion:",
        "---",
        prompt_text or "[Prompt no encontrado; revisar PromptPath.]",
        "---",
    ]
    (root / NEXT_ACTION_PATH).write_text("\n".join(body), encoding="utf-8")


def refresh_summaries(root: Path, queue_rows: list[dict[str, str]]) -> None:
    total = len(queue_rows)
    correct = sum(is_correct(row) for row in queue_rows)
    pending = total - correct
    failed = sum("fall" in status_of(row).lower() for row in queue_rows)
    status_counts = Counter(status_of(row) or "[vacio]" for row in queue_rows)

    summary_lines = [
        "RESUMEN COLA GENERACION IMAGENES OLOVERSO",
        f"Fecha: {datetime.now().date().isoformat()}",
        "",
        f"Items totales: {total}",
        f"Correctas: {correct}",
        f"Pendientes/no correctas: {pending}",
        f"Fallidas: {failed}",
        "",
        "Estados:",
    ]
    for status, count in sorted(status_counts.items()):
        summary_lines.append(f"- {status}: {count}")
    (root / QUEUE_SUMMARY_PATH).write_text("\n".join(summary_lines) + "\n", encoding="utf-8")

    blocks = block_summary(queue_rows)
    batches = batch_summary(queue_rows)
    write_csv(root / BLOCK_SUMMARY_PATH, ["Bloque", "Leyes", "Items", "General", "Principios", "Apartados", "Pendientes", "Correctas"], blocks)
    write_csv(root / BATCH_INDEX_PATH, ["Batch", "Count", "FirstItem", "LastItem", "FirstLaw", "LastLaw", "FirstKind", "LastKind", "Pending", "Correct"], batches)

    next_item = first_pending(queue_rows)
    dashboard = [
        "# TABLERO PRODUCCION IMAGENES OLOVERSO",
        f"Fecha: {datetime.now().date().isoformat()}",
        "",
        "## Estado global",
        f"- Items totales en cola: {total}",
        f"- Pendientes/no correctas: {pending}",
        f"- Correctas: {correct}",
        f"- Fallidas: {failed}",
        f"- Drive folder: {DRIVE_FOLDER_URL}",
        "- GitHub: solo control, registros y manifiestos; imagenes finales en Drive.",
        "",
        "## Siguiente accion",
    ]
    if next_item:
        dashboard.extend(
            [
                f"- Item: {next_item.get('ItemId', '')}",
                f"- Lote: {next_item.get('Batch', '')}",
                f"- Tipo: {next_item.get('ImageKind', '')}",
                f"- Ley: {next_item.get('LawNumber', '')} - {next_item.get('LawTitle', '')}",
                f"- Prompt repo-relativo: {prompt_path_for(next_item)}",
                f"- Archivo temporal sugerido: {output_path_for(next_item)}",
            ]
        )
    else:
        dashboard.append("- No quedan items pendientes.")
    dashboard.extend(["", "## Resumen por bloque", "| Bloque | Leyes | Items | General | Principios | Apartados | Pendientes | Correctas |", "|---|---:|---:|---:|---:|---:|---:|---:|"])
    for row in blocks:
        dashboard.append(
            f"| {row['Bloque']} | {row['Leyes']} | {row['Items']} | {row['General']} | {row['Principios']} | {row['Apartados']} | {row['Pendientes']} | {row['Correctas']} |"
        )
    dashboard.extend(["", "## Indice de lotes", "| Lote | Items | Primer item | Ultimo item | Leyes | Pendientes | Correctas |", "|---|---:|---|---|---|---:|---:|"])
    for row in batches:
        laws = f"{row['FirstLaw']}-{row['LastLaw']}" if row["FirstLaw"] or row["LastLaw"] else ""
        dashboard.append(
            f"| {row['Batch']} | {row['Count']} | {row['FirstItem']} | {row['LastItem']} | {laws} | {row['Pending']} | {row['Correct']} |"
        )
    (root / DASHBOARD_PATH).write_text("\n".join(dashboard) + "\n", encoding="utf-8")


def cmd_plan(args: argparse.Namespace) -> int:
    root = Path(args.repo_root).resolve()
    _, queue_rows = read_csv(root / QUEUE_PATH)
    selected = [row for row in queue_rows if not is_correct(row)][: args.limit]
    payload = {
        "drive_folder_id": DRIVE_FOLDER_ID,
        "drive_folder_url": DRIVE_FOLDER_URL,
        "limit": args.limit,
        "count": len(selected),
        "items": [queue_item_payload(row) for row in selected],
    }
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    return 0


def cmd_audit(args: argparse.Namespace) -> int:
    root = Path(args.repo_root).resolve()
    _, queue_rows = read_csv(root / QUEUE_PATH)
    _, manifest_rows = read_csv(root / MANIFEST_PATH)
    manifest_correct = {row.get("ItemId") for row in manifest_rows if status_of(row).lower() == "correcta"}
    queue_correct = [row.get("ItemId") for row in queue_rows if is_correct(row)]
    missing_manifest = [item for item in queue_correct if item not in manifest_correct]
    payload = {
        "queue_total": len(queue_rows),
        "queue_status_counts": Counter(status_of(row) or "[vacio]" for row in queue_rows),
        "manifest_rows": len(manifest_rows),
        "correct_items_missing_drive_manifest_count": len(missing_manifest),
        "correct_items_missing_drive_manifest_sample": missing_manifest[:20],
        "next_pending": queue_item_payload(first_pending(queue_rows)) if first_pending(queue_rows) else None,
    }
    print(json.dumps(payload, ensure_ascii=False, indent=2, default=dict))
    return 0


def cmd_record_upload(args: argparse.Namespace) -> int:
    root = Path(args.repo_root).resolve()
    if args.status.lower() == "correcta" and (not args.drive_file_id or not args.drive_url):
        raise SystemExit("--drive-file-id and --drive-url are required when --status Correcta")

    queue_fields, queue_rows = read_csv(root / QUEUE_PATH)
    if not queue_rows:
        raise SystemExit(f"Queue not found or empty: {root / QUEUE_PATH}")

    target = None
    for row in queue_rows:
        if row.get("ItemId") == args.item_id:
            target = row
            break
    if target is None:
        raise SystemExit(f"Item not found in queue: {args.item_id}")

    sha = args.sha256 or ""
    if args.local_file:
        local_file = Path(args.local_file)
        if local_file.exists():
            sha = sha256_file(local_file)

    notes = args.notes or f"Imagen subida a Drive y registrada el {datetime.now().date().isoformat()}."
    target["Status"] = args.status
    target["Notes"] = notes

    manifest_fields, manifest_rows = read_csv(root / MANIFEST_PATH)
    manifest_fields = ensure_manifest_fields(manifest_fields)
    manifest_row = {
        "ItemId": target.get("ItemId", ""),
        "LawNumber": target.get("LawNumber", ""),
        "LawTitle": target.get("LawTitle", ""),
        "ImageKind": target.get("ImageKind", ""),
        "PromptPath": prompt_path_for(target),
        "DriveFolderId": DRIVE_FOLDER_ID,
        "DriveFileId": args.drive_file_id or "",
        "DriveUrl": args.drive_url or "",
        "FileName": args.file_name or file_name_for(target),
        "SHA256": sha,
        "Status": args.status,
        "Notes": notes,
        "CreatedAt": args.created_at or utc_now(),
    }
    manifest_rows = upsert_by_item(manifest_rows, manifest_row)

    write_csv(root / QUEUE_PATH, queue_fields, queue_rows)
    write_csv(root / MANIFEST_PATH, manifest_fields, manifest_rows)
    refresh_next_action(root, queue_rows)
    refresh_summaries(root, queue_rows)

    print(json.dumps({"updated_item": args.item_id, "status": args.status, "drive_url": args.drive_url}, ensure_ascii=False, indent=2))
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Oloverso Drive-first queue helper")
    parser.add_argument("--repo-root", default=".", help="Repository root. Defaults to current directory.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    plan = subparsers.add_parser("plan", help="Print the next pending Drive-first work items as JSON.")
    plan.add_argument("--limit", type=int, default=5)
    plan.set_defaults(func=cmd_plan)

    audit = subparsers.add_parser("audit", help="Print queue/manifest consistency information as JSON.")
    audit.set_defaults(func=cmd_audit)

    record = subparsers.add_parser("record-upload", help="Record a Drive upload and refresh production records.")
    record.add_argument("--item-id", required=True)
    record.add_argument("--drive-file-id", default="")
    record.add_argument("--drive-url", default="")
    record.add_argument("--file-name", default="")
    record.add_argument("--sha256", default="")
    record.add_argument("--local-file", default="")
    record.add_argument("--status", default="Correcta")
    record.add_argument("--notes", default="")
    record.add_argument("--created-at", default="")
    record.set_defaults(func=cmd_record_upload)
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
