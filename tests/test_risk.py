from app.evidence import find_contradictions
from app.models import Evidence, ModuleResult, Outcome
from app.risk import assess_risk


def test_conflicting_high_confidence_claims_require_review():
    results = [
        ModuleResult(module_name="ocr", status="COMPLETE", confidence=.9, explanation="ok", evidence=[Evidence(module="ocr", field="dob", value="12/05/2002", confidence=.94, explanation="OCR DOB")]),
        ModuleResult(module_name="mrz", status="COMPLETE", confidence=.9, explanation="ok", evidence=[Evidence(module="mrz", kind="mrz", field="dob", value="12/05/2007", confidence=.99, explanation="MRZ DOB")]),
    ]
    contradictions = find_contradictions(results)
    assessment = assess_risk(results, contradictions)
    assert len(contradictions) == 1
    assert assessment.outcome in {Outcome.REVIEW, Outcome.HIGH}


def test_no_adverse_evidence_is_low_risk():
    results = [ModuleResult(module_name="validation", status="PASS", confidence=1, explanation="checks passed")]
    assert assess_risk(results, []).outcome == Outcome.LOW
