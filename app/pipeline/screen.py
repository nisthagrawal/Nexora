from app.evidence import find_contradictions
from app.models import ScreeningReport
from app.risk import assess_risk
from app.validation import validate_document
from modules.face import verify
from modules.forgery import inspect
from modules.ocr import extract_fields
from modules.preprocessing import preprocess


def screen(document: bytes, person: bytes | None = None, document_type: str = "Identity document") -> ScreeningReport:
    clean_document = preprocess(document)
    ocr_result, fields = extract_fields(clean_document)
    results = [ocr_result, validate_document(fields), inspect(clean_document), verify(clean_document, person)]
    contradictions = find_contradictions(results)
    return ScreeningReport(document_type=document_type, module_results=results, contradictions=contradictions, risk=assess_risk(results, contradictions))
