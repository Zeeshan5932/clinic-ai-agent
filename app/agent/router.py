from langgraph import GraphNode
from app.agent.nodes import (
    booking_node,
    reschedule_node,
    cancel_node,
    faq_node,
)


def intent_router(intent: str) -> GraphNode:
    mapping = {
        "booking": booking_node,
        "reschedule": reschedule_node,
        "cancel": cancel_node,
        "faq": faq_node,
    }
    # default to faq if unknown
    return mapping.get(intent, faq_node)
