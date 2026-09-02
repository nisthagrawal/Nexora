from app.models import Evidence, ModuleResult


def inspect(content: bytes) -> ModuleResult:
    """Honest Phase-1 adapter: a model hook, not a fabricated detector result."""
    return ModuleResult(module_name="forgery", status="UNAVAILABLE", confidence=0.0, evidence=[Evidence(module="forgery", kind="availability", confidence=0.0, severity=0.0, explanation="No forensic model has been configured for this deployment.")], explanation="Forensic analysis is awaiting a trained/configured model (e.g. SIDTD/FakeIDet adapter).")
