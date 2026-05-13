def normalize_priority(value):
    text = str(value).strip().lower()
    if text in {"low", "lo", "l", "minor"}:
        return "low"
    if text in {"medium", "med", "normal", "m"}:
        return "medium"
    if text in {"high", "hi", "h", "important", "urgent", "critical", "blocker", "p0"}:
        return "high"
    return "medium"
