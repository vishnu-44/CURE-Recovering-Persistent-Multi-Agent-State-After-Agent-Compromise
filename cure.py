"""Trace validation and deterministic claim-level CURE revocation."""

from __future__ import annotations

from models import Claim, Evidence, Record, RecoveryCertificate


def affected_records(records: dict[str, Record], revoked_source: str) -> set[str]:
    affected = {item.record_id for item in records.values() if item.writer == revoked_source}
    while True:
        expanded = affected | {
            item.record_id
            for item in records.values()
            if any(parent in affected for parent in item.derived_from)
        }
        if expanded == affected:
            return affected
        affected = expanded


def validate(
    records: dict[str, Record],
    claims: list[Claim],
    evidence: dict[str, Evidence],
) -> None:
    claim_ids = {claim.claim_id for claim in claims}
    canonicals = {claim.canonical for claim in claims}
    if len(claim_ids) != len(claims):
        raise ValueError("Claim IDs must be unique")
    if len(canonicals) != len(claims):
        raise ValueError("Canonical claim IDs must be unique")
    covered_records = {claim.record_id for claim in claims}
    if covered_records != set(records):
        raise ValueError("Every record must have at least one extracted claim")

    for claim in claims:
        if not claim.support_sets or any(not support for support in claim.support_sets):
            raise ValueError(f"Claim {claim.claim_id} has an empty support structure")
        if any(item not in canonicals for item in claim.preconditions):
            raise ValueError(f"Claim {claim.claim_id} has an unknown precondition")
        for support in claim.support_sets:
            for record_id in support:
                item = evidence.get(record_id)
                if item is None or record_id not in records or not item.is_root:
                    raise ValueError(
                        f"Claim {claim.claim_id} cites missing or non-root evidence"
                    )


def recover(
    records: dict[str, Record],
    claims: list[Claim],
    evidence: dict[str, Evidence],
    revoked_source: str,
) -> RecoveryCertificate:
    """Apply deterministic revocation to a validated semantic representation."""
    validate(records, claims, evidence)
    affected = affected_records(records, revoked_source)
    affected_claims = [claim for claim in claims if claim.record_id in affected]
    unaffected_claims = [claim for claim in claims if claim.record_id not in affected]
    retained = {claim.canonical for claim in unaffected_claims}
    retained_ids = [claim.claim_id for claim in unaffected_claims]
    surviving_support: dict[str, list[str]] = {}

    pending = list(affected_claims)
    changed = True
    while changed:
        changed = False
        for claim in list(pending):
            clean_sets = [
                support
                for support in claim.support_sets
                if all(
                    evidence[item].supported
                    and evidence[item].is_root
                    and evidence[item].source != revoked_source
                    for item in support
                )
            ]
            if clean_sets and set(claim.preconditions) <= retained:
                retained.add(claim.canonical)
                retained_ids.append(claim.claim_id)
                surviving_support[claim.claim_id] = list(clean_sets[0])
                pending.remove(claim)
                changed = True

    failed = {
        claim.claim_id: sorted(set(claim.preconditions) - retained)
        for claim in pending
        if set(claim.preconditions) - retained
    }
    return RecoveryCertificate(
        revoked_source=revoked_source,
        retained_claim_ids=sorted(retained_ids),
        quarantined_claim_ids=sorted(claim.claim_id for claim in pending),
        surviving_support=surviving_support,
        failed_preconditions=failed,
    )
