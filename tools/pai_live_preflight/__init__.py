"""Fixture-only PAI live preflight development tooling.

This package is not a runtime adapter and is not approved for live installed
PAI reads. S14C exercises it only against repository fixtures.
"""

from .consent import APPROVED_DECLARED_SOURCE_ROOT, EXACT_CONSENT_PHRASE
from .preflight import run_fixture_preflight
from .report import write_report

__all__ = [
    "APPROVED_DECLARED_SOURCE_ROOT",
    "EXACT_CONSENT_PHRASE",
    "run_fixture_preflight",
    "write_report",
]
