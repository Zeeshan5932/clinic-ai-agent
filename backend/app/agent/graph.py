"""
LangGraph workflow definition for the AI receptionist agent
"""
from langgraph.graph import END, StateGraph
from app.agent.nodes import (
    detect_intent,
    booking_node,
    reschedule_node,
    cancel_node,
    faq_node,
)
from app.agent.state import AgentState
from app.agent.router import intent_router


def create_agent_graph():
    """
    Create the LangGraph workflow graph.
    
    Flow:
    1. Start with detect_intent node (detects user intent)
    2. Route conditionally based on intent:
       - booking → booking_node
       - reschedule → reschedule_node
       - cancel → cancel_node
       - faq → faq_node (default)
    3. Each node processes the state and sets the response
    """
    graph = StateGraph(AgentState)

    # Add initial node for intent detection
    graph.add_node("detect_intent", detect_intent)

    # Add terminal nodes
    graph.add_node("booking", booking_node)
    graph.add_node("reschedule", reschedule_node)
    graph.add_node("cancel", cancel_node)
    graph.add_node("faq", faq_node)

    # Conditional routing based on detected intent
    def routing_condition(state):
        intent = state.get("intent", "faq")
        return intent_router(intent)

    graph.add_conditional_edges(
        "detect_intent",
        routing_condition,
        {
            "booking": "booking",
            "reschedule": "reschedule",
            "cancel": "cancel",
            "faq": "faq",
        },
    )

    # Every terminal workflow node must point to END.
    graph.add_edge("booking", END)
    graph.add_edge("reschedule", END)
    graph.add_edge("cancel", END)
    graph.add_edge("faq", END)

    # Set entry point
    graph.set_entry_point("detect_intent")

    return graph.compile()


# Global agent graph instance
agent_graph = create_agent_graph()

__all__ = ["create_agent_graph", "agent_graph"]
