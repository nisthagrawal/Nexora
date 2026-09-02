from __future__ import annotations

from app.models import Contradiction, ModuleResult, Outcome, RiskAssessment

DEFAULT_CONFIG = {"contradiction_weight": 28, "anomaly_weight": 34, "validation_failure_weight": 24, "face_non_match_weight": 35, "uncertainty_weight": 12, "review_threshold": 30, "high_threshold": 65}


def assess_risk(results: list[ModuleResult], contradictions: list[Contradiction], config: dict | None = None) -> RiskAssessment:
    cfg = {**DEFAULT_CONFIG, **(config or {})}
    anomaly = max((e.severity for r in results for e in r.evidence), default=0.0)
    validation_failure = any(r.module_name == "validation" and r.status == "FAIL" for r in results)
    face_failure = any(r.module_name == "face" and r.status == "NON_MATCH" for r in results)
    unavailable = sum(1 for r in results if r.status in {"UNAVAILABLE", "NOT_PROVIDED"})
    breakdown = {"contradictions": min(40, len(contradictions) * cfg["contradiction_weight"]), "forensic_anomaly": anomaly * cfg["anomaly_weight"], "validation_failure": cfg["validation_failure_weight"] if validation_failure else 0, "face_non_match": cfg["face_non_match_weight"] if face_failure else 0, "uncertainty": min(cfg["uncertainty_weight"], unavailable * 4)}
    score = round(min(100, sum(breakdown.values())))
    outcome = Outcome.HIGH if score >= cfg["high_threshold"] else Outcome.REVIEW if score >= cfg["review_threshold"] or contradictions else Outcome.LOW
    reasons = [c.explanation for c in contradictions]
    reasons += [r.explanation for r in results if r.status in {"FAIL", "NON_MATCH", "SUSPICIOUS"}]
    if unavailable: reasons.append(f"{unavailable} module(s) did not provide conclusive evidence.")
    if not reasons: reasons.append("Available evidence agrees and no material anomaly was detected.")
    action = "ESCALATE FOR MANUAL VERIFICATION" if outcome != Outcome.LOW else "CLEAR SUBJECT TO NORMAL OPERATIONAL PROCEDURES"
    return RiskAssessment(score=score, outcome=outcome, reasons=reasons, recommended_action=action, score_breakdown={k: round(v, 1) for k, v in breakdown.items()})
