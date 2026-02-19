from langgraph import Graph, GraphNode
from app.agent.nodes import detect_intent
from app.agent.router import intent_router


def create_agent_graph() -> Graph:
    graph = Graph(name="clinic_agent")

    # initial node for intent detection
    intent_node = GraphNode(func=detect_intent, name="detect_intent")
    graph.add_node(intent_node)

    # register all possible terminal nodes so they exist in graph
    from app.agent.nodes import booking_node, reschedule_node, cancel_node, faq_node
    graph.add_node(GraphNode(func=booking_node, name="booking"))
    graph.add_node(GraphNode(func=reschedule_node, name="reschedule"))
    graph.add_node(GraphNode(func=cancel_node, name="cancel"))
    graph.add_node(GraphNode(func=faq_node, name="faq"))

    # routing will be done dynamically based on state
    def routing(state):
        intent = state.get("intent")
        return intent_router(intent)

    graph.set_router(routing)

    return graph
