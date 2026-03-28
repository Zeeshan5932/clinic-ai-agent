"""
Router for conditional workflow routing based on intent
"""


def intent_router(intent: str) -> str:
    """
    Route to the appropriate node based on detected intent.
    Returns the node key as a string.
    """
    mapping = {
        "booking": "booking",
        "reschedule": "reschedule",
        "cancel": "cancel",
        "faq": "faq",
    }
    # Default to FAQ if intent is not recognized
    return mapping.get(intent.lower(), "faq")


__all__ = ["intent_router"]
