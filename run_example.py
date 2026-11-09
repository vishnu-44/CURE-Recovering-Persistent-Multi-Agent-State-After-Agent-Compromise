"""Run a small mixed-record CURE example without external services."""

from __future__ import annotations

import json

from cure import recover
from models import Claim, Evidence, Record


def main() -> None:
    records = {
        "invoice": Record("invoice", "invoice_db", "memory", "Invoice is $8,000."),
        "po": Record("po", "po_service", "memory", "PO 781 matches."),
        "profile": Record("profile", "profile_service", "memory", "Account is 4472."),
        "master": Record("master", "vendor_master", "memory", "Account is 4472."),
        "summary": Record(
            "summary",
            "accounts_payable",
            "summary",
            "Invoice is $8,000; PO 781 matches; pay account 4472.",
            ("invoice", "po", "profile", "master"),
        ),
    }
    evidence = {
        item.record_id: Evidence(item.record_id, item.writer, not item.derived_from)
        for item in records.values()
    }
    claims = [
        Claim("invoice:c1", "invoice", "Invoice is $8,000.", "invoice_amount", (("invoice",),)),
        Claim("po:c1", "po", "PO 781 matches.", "po_match", (("po",),)),
        Claim("profile:c1", "profile", "Account is 4472.", "profile_account", (("profile",),)),
        Claim("master:c1", "master", "Account is 4472.", "master_account", (("master",),)),
        Claim("summary:c1", "summary", "Invoice is $8,000.", "summary_invoice", (("invoice",),)),
        Claim("summary:c2", "summary", "PO 781 matches.", "summary_po", (("po",),)),
        Claim(
            "summary:c3",
            "summary",
            "Bank account is 4472.",
            "summary_account",
            (("profile",), ("master",)),
        ),
        Claim(
            "summary:c4",
            "summary",
            "Payment should be sent to account 4472.",
            "payment_action",
            (("invoice", "po", "profile"),),
            ("summary_invoice", "summary_po", "summary_account"),
        ),
    ]
    certificate = recover(records, claims, evidence, revoked_source="profile_service")
    print(json.dumps(certificate.to_dict(), indent=2))


if __name__ == "__main__":
    main()
