from collections import defaultdict
from app.models import Contradiction, ModuleResult


def find_contradictions(results: list[ModuleResult]) -> list[Contradiction]:
    claims: dict[str, list[tuple[object, str, float]]] = defaultdict(list)
    for result in results:
        for item in result.evidence:
            if item.field and item.value not in (None, "") and item.kind in {"observation", "mrz"}:
                claims[item.field].append((item.value, item.module, item.confidence))
    contradictions: list[Contradiction] = []
    for field, items in claims.items():
        canonical = {str(value).strip().lower() for value, _, _ in items}
        if len(canonical) > 1:
            contradictions.append(Contradiction(field=field, values=[value for value, _, _ in items], sources=[source for _, source, _ in items], severity=min(1.0, sum(conf for _, _, conf in items) / len(items)), explanation=f"Conflicting {field} values were reported by independent evidence sources."))
    return contradictions
