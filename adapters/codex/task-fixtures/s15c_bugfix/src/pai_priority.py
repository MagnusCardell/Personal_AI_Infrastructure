"""Priority normalization helpers for the S15C bounded task fixture."""


def normalize_priority(value):
    """Return the canonical PAI priority name for a user supplied value."""
    text = str(value).strip().lower()

    if text in {"low", "lo", "l"}:
        return "low"
    if text in {"medium", "med", "normal", "m"}:
        return "medium"
    if text in {"high", "hi", "h", "urgent", "critical", "blocker"}:
        return "high"

    return "medium"
