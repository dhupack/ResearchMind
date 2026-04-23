import re
from typing import TypedDict

from langgraph.graph import StateGraph, START, END

from agents import build_reader_agent, build_search_agent, writer_chain, critic_chain


class ResearchState(TypedDict, total=False):
    topic: str
    search_results: str
    scraped_content: str
    report: str
    feedback: str
    score: int
    rewrite_count: int
    max_rewrites: int


def extract_text(response) -> str:
    content = response["messages"][-1].content
    if isinstance(content, list) and content:
        first = content[0]
        if isinstance(first, dict) and "text" in first:
            return first["text"]
        return str(content)
    if isinstance(content, dict):
        return content.get("text", str(content))
    return str(content)


def search_node(state: ResearchState) -> ResearchState:
    search_agent = build_search_agent()
    result = search_agent.invoke(
        {
            "messages": [
                (
                    "system",
                    "You are a research assistant. You MUST use the web_search tool. "
                    "Do NOT answer from your own knowledge.",
                ),
                (
                    "human",
                    f"Return at least 3 URLs with titles and snippets for: {state['topic']}.",
                ),
            ]
        }
    )
    return {"search_results": extract_text(result)}


def reader_node(state: ResearchState) -> ResearchState:
    reader_agent = build_reader_agent()
    result = reader_agent.invoke(
        {
            "messages": [
                (
                    "system",
                    "You are a web content extraction assistant. Select the most relevant URL "
                    "and extract detailed, factual content.",
                ),
                (
                    "human",
                    f"Analyze and extract from:\n{state['search_results'][:1000]}",
                ),
            ]
        }
    )
    return {"scraped_content": extract_text(result)}


def writer_node(state: ResearchState) -> ResearchState:
    research = (
        f"SEARCH RESULTS:\n{state['search_results']}\n\n"
        f"SCRAPED CONTENT:\n{state['scraped_content']}"
    )

    # Pass critic feedback during rewrites
    feedback_for_rewrite = state.get("feedback", "") if state.get("rewrite_count", 0) > 0 else ""

    report = writer_chain.invoke(
        {
            "topic": state["topic"],
            "research": research,
            "feedback": feedback_for_rewrite,
        }
    )
    return {"report": report}


def critic_node(state: ResearchState) -> ResearchState:
    feedback = critic_chain.invoke({"report": state["report"]})

    # Parse "Score: X/10"
    match = re.search(r"Score:\s*(\d{1,2})\s*/\s*10", feedback)
    score = int(match.group(1)) if match else 0

    return {"feedback": feedback, "score": score}


def rewrite_counter_node(state: ResearchState) -> ResearchState:
    return {"rewrite_count": state.get("rewrite_count", 0) + 1}


def route_after_critic(state: ResearchState) -> str:
    threshold = 5
    score = state.get("score", 0)
    rewrite_count = state.get("rewrite_count", 0)
    max_rewrites = state.get("max_rewrites", 3)

    if score < threshold and rewrite_count < max_rewrites:
        return "rewrite"
    return "done"


def build_research_graph():
    graph = StateGraph(ResearchState)

    graph.add_node("search", search_node)
    graph.add_node("reader", reader_node)
    graph.add_node("writer", writer_node)
    graph.add_node("critic", critic_node)
    graph.add_node("rewrite_counter", rewrite_counter_node)

    graph.add_edge(START, "search")
    graph.add_edge("search", "reader")
    graph.add_edge("reader", "writer")
    graph.add_edge("writer", "critic")

    graph.add_conditional_edges(
        "critic",
        route_after_critic,
        {
            "rewrite": "rewrite_counter",
            "done": END,
        },
    )

    graph.add_edge("rewrite_counter", "writer")

    return graph.compile()


research_graph = build_research_graph()

# print(research_graph.get_graph().draw_ascii())