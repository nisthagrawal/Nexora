from app.models import Evidence, ModuleResult


def verify(document: bytes, person: bytes | None) -> ModuleResult:
    if not person:
        return ModuleResult(module_name="face", status="NOT_PROVIDED", confidence=0.0, explanation="No presented-person image was supplied.")
    return ModuleResult(module_name="face", status="UNAVAILABLE", confidence=0.0, evidence=[Evidence(module="face", kind="availability", confidence=0.0, explanation="Face embedding adapter is not configured. Replace with an ArcFace/AdaFace implementation.")], explanation="A person image was supplied, but face verification is not configured.")
