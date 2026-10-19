"""Helpers for Elasticsearch query building."""


def escape_wildcard(value: str) -> str:
    """Escape characters that have special meaning in ES wildcard queries."""
    for char in ("\\", "*", "?"):
        value = value.replace(char, f"\\{char}")
    return value
