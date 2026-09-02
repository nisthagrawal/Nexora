"""Safely ingest images and PDFs into page images for the common pipeline."""
from __future__ import annotations

from io import BytesIO
from PIL import Image


def ingest_document(content: bytes, filename: str, content_type: str | None) -> dict[str, object]:
    is_pdf = (content_type == "application/pdf") or filename.lower().endswith(".pdf")
    if is_pdf:
        try:
            import fitz  # PyMuPDF
            pdf = fitz.open(stream=content, filetype="pdf")
            pages = []
            for index, page in enumerate(pdf):
                pix = page.get_pixmap(matrix=fitz.Matrix(2, 2), alpha=False)
                pages.append({"page": index + 1, "image": pix.tobytes("png")})
            if not pages:
                raise ValueError("PDF contains no renderable pages")
            return {"kind": "PDF", "page_count": len(pages), "pages": pages, "native_text": bool("".join(p.get_text() for p in pdf).strip())}
        except ImportError as error:
            raise ValueError("PDF support requires PyMuPDF; install requirements.txt") from error
    try:
        Image.open(BytesIO(content)).verify()
    except Exception as error:
        raise ValueError("Unreadable or unsupported image") from error
    return {"kind": "IMAGE", "page_count": 1, "pages": [{"page": 1, "image": content}], "native_text": False}
