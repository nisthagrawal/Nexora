from __future__ import annotations

from datetime import datetime, timezone
import hashlib
import uuid
from app.pipeline.screen import screen
from app.services import assess_image_quality, ingest_document


def run_screening(content: bytes, filename: str, content_type: str | None, person: bytes | None = None) -> dict[str, object]:
    ingested = ingest_document(content, filename, content_type)
    pages = []
    for entry in ingested["pages"]:
        quality = assess_image_quality(entry["image"])
        report = screen(entry["image"], person)
        pages.append({"page": entry["page"], "quality": quality, "report": report.model_dump()})
    return {"screening_id": f"NX-{uuid.uuid4().hex[:12].upper()}", "timestamp": datetime.now(timezone.utc).isoformat(), "document_hash": hashlib.sha256(content).hexdigest(), "filename": filename, "ingestion": {k: v for k, v in ingested.items() if k != "pages"}, "pages": pages, "audit_note": "Raw document bytes are processed for this request; the response stores only the hash and structured evidence."}
