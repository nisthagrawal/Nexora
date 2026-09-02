"""Append-only, PII-minimised audit records.

Use a managed immutable event store in production; optionally anchor batches of
record hashes to a permissioned ledger. Do not put document images or PII on-chain.
"""
from __future__ import annotations

from datetime import datetime, timezone
import hashlib
import json
from pydantic import BaseModel


class AuditEvent(BaseModel):
    event_type: str
    actor_id: str
    case_id: str
    payload_digest: str
    timestamp: datetime
    previous_hash: str
    record_hash: str


class AuditChain:
    def __init__(self) -> None:
        self._last_hash = "GENESIS"

    @staticmethod
    def digest(payload: object) -> str:
        encoded = json.dumps(payload, sort_keys=True, separators=(",", ":"), default=str).encode()
        return hashlib.sha256(encoded).hexdigest()

    def append(self, event_type: str, actor_id: str, case_id: str, redacted_payload: object) -> AuditEvent:
        timestamp = datetime.now(timezone.utc)
        payload_digest = self.digest(redacted_payload)
        record_hash = self.digest({"event_type": event_type, "actor_id": actor_id, "case_id": case_id, "payload_digest": payload_digest, "timestamp": timestamp.isoformat(), "previous_hash": self._last_hash})
        event = AuditEvent(event_type=event_type, actor_id=actor_id, case_id=case_id, payload_digest=payload_digest, timestamp=timestamp, previous_hash=self._last_hash, record_hash=record_hash)
        self._last_hash = record_hash
        return event
