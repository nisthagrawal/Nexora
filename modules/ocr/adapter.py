from __future__ import annotations

from io import BytesIO
import re
from PIL import Image
from app.models import Evidence, ModuleResult


FIELD_PATTERNS = {
    "document_number": r"(?:passport|document|doc(?:ument)?\s*no\.?)\s*[:#-]?\s*([A-Z0-9]{6,14})",
    "dob": r"(?:date\s*of\s*birth|dob)\s*[:#-]?\s*(\d{1,2}[/-]\d{1,2}[/-]\d{2,4})",
    "expiry_date": r"(?:date\s*of\s*expiry|expiry|expires)\s*[:#-]?\s*(\d{1,2}[/-]\d{1,2}[/-]\d{2,4})",
}


def extract_fields(content: bytes) -> tuple[ModuleResult, dict[str, str]]:
    try:
        import pytesseract
        text = pytesseract.image_to_string(Image.open(BytesIO(content)))
    except Exception as error:
        return ModuleResult(module_name="ocr", status="UNAVAILABLE", confidence=0, explanation="OCR adapter unavailable. Install Tesseract or replace this adapter with PaddleOCR.", metadata={"error": str(error)}), {}
    fields = {}
    for name, pattern in FIELD_PATTERNS.items():
        match = re.search(pattern, text, re.I)
        if match: fields[name] = match.group(1)
    evidence = [Evidence(module="ocr", field=k, value=v, confidence=0.75, explanation=f"OCR extracted {k.replace('_', ' ')}.") for k, v in fields.items()]
    return ModuleResult(module_name="ocr", status="COMPLETE" if fields else "INCONCLUSIVE", confidence=0.75 if fields else 0.25, evidence=evidence, explanation="OCR completed." if fields else "OCR completed but no configured identity fields were found.", metadata={"raw_text": text[:4000]}), fields
