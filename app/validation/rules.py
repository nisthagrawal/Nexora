from __future__ import annotations

from datetime import date, datetime
import re
from app.models import Evidence, ModuleResult


def _parse_date(value: str) -> date | None:
    for pattern in ("%d/%m/%Y", "%Y-%m-%d", "%d-%m-%Y"):
        try:
            return datetime.strptime(value, pattern).date()
        except ValueError:
            pass
    return None


def validate_document(fields: dict[str, str]) -> ModuleResult:
    evidence: list[Evidence] = []
    failures: list[str] = []
    expiry = _parse_date(fields.get("expiry_date", ""))
    if expiry:
        expired = expiry < date.today()
        evidence.append(Evidence(module="validation", kind="rule", field="expiry_date", value=fields["expiry_date"], confidence=1.0, severity=0.9 if expired else 0.0, explanation="Document is expired." if expired else "Document expiry date is valid."))
        if expired: failures.append("Document is expired")
    document_number = fields.get("document_number")
    if document_number:
        valid = bool(re.fullmatch(r"[A-Z0-9]{6,14}", document_number.replace(" ", "").upper()))
        evidence.append(Evidence(module="validation", kind="rule", field="document_number", value=document_number, confidence=0.95, severity=0.6 if not valid else 0.0, explanation="Document number format is plausible." if valid else "Document number format is unexpected."))
        if not valid: failures.append("Unexpected document-number format")
    if not evidence:
        evidence.append(Evidence(module="validation", kind="availability", confidence=0.0, severity=0.3, explanation="No structured fields were available for deterministic validation."))
    return ModuleResult(module_name="validation", status="FAIL" if failures else "PASS", confidence=0.98 if evidence else 0.0, evidence=evidence, affected_field="expiry_date" if "Document is expired" in failures else None, explanation="; ".join(failures) if failures else "Deterministic checks passed for available fields.", metadata={"failed_rules": failures})
