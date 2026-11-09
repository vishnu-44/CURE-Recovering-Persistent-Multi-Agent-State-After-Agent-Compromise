"""Small data model shared by the reference workflow and recovery methods."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any


@dataclass(frozen=True)
class Record:
    record_id: str
    writer: str
    state_type: str
    text: str
    derived_from: tuple[str, ...] = ()


@dataclass
class AgentState:
    agent_id: str
    records: list[Record] = field(default_factory=list)


@dataclass(frozen=True)
class Claim:
    claim_id: str
    record_id: str
    text: str
    canonical: str
    support_sets: tuple[tuple[str, ...], ...]
    preconditions: tuple[str, ...] = ()


@dataclass(frozen=True)
class Evidence:
    record_id: str
    source: str
    is_root: bool
    supported: bool = True


@dataclass
class RecoveryCertificate:
    revoked_source: str
    retained_claim_ids: list[str]
    quarantined_claim_ids: list[str]
    surviving_support: dict[str, list[str]]
    failed_preconditions: dict[str, list[str]]

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)
