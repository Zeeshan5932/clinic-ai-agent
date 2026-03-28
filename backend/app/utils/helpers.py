"""
General utility functions
"""


def sanitize_string(text: str, max_length: int = 500) -> str:
    """
    Sanitize user input by stripping whitespace and limiting length.
    """
    return text.strip()[:max_length]


__all__ = ["sanitize_string"]
