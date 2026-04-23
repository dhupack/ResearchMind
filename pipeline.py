# from agents import build_reader_agent , build_search_agent , writer_chain , critic_chain

# def run_research_pipeline(topic: str):

#     state = {}

#     def extract_text(response):
#         content = response['messages'][-1].content
#         if isinstance(content, list):
#             return content[0].get('text', str(content))
#         elif isinstance(content, dict):
#             return content.get('text', str(content))
#         return content

#     # STEP 1: SEARCH
#     print("\n" + "="*50)
#     print("STEP 1 - SEARCH AGENT")
#     print("="*50)

#     search_agent = build_search_agent()
#     search_result = search_agent.invoke({
#         "messages": [
#             ("system", "You are a research assistant. You MUST use the web_search tool. Do NOT answer from your own knowledge."),
#             ("human", f"Return at least 3 URLs with titles and snippets for: {topic}.")
#         ]
#     })

#     state["search_results"] = extract_text(search_result)
#     print(state["search_results"])


#     # STEP 2: READER
#     print("\n" + "="*50)
#     print("STEP 2 - READER AGENT")
#     print("="*50)

#     reader_agent = build_reader_agent()
#     reader_result = reader_agent.invoke({
#         "messages": [
#             ("system", 
#             "You are a web content extraction assistant. Your job is to select the most relevant URL and extract detailed, factual information from it. "
#             "Focus only on useful, high-quality content. Avoid irrelevant text, ads, or navigation elements."),
#             ("human", f"Analyze and extract from:\n{state['search_results'][:800]}")
#         ]
#     })

#     state["scraped_content"] = extract_text(reader_result)
#     print(state["scraped_content"])


#     # STEP 3: WRITER
#     print("\n" + "="*50)
#     print("STEP 3 - WRITER")
#     print("="*50)

#     research = f"""
#     SEARCH RESULTS:
#     {state['search_results']}

#     SCRAPED CONTENT:
#     {state['scraped_content']}
#     """

#     state["report"] = writer_chain.invoke({
#         "topic": topic,
#         "research": research
#     })

#     print(state["report"])


#     # STEP 4: CRITIC
#     print("\n" + "="*50)
#     print("STEP 4 - CRITIC")
#     print("="*50)

#     state["feedback"] = critic_chain.invoke({
#         "report": state["report"]
#     })

#     print(state["feedback"])

#     return state

# if __name__ == "__main__":
#     topic = input("\n Enter a research topic : ")
#     run_research_pipeline(topic)

from graph import research_graph


def run_research_pipeline(topic: str, max_rewrites: int):
    print("\n" + "=" * 50)
    print("RUNNING RESEARCH GRAPH")
    print("=" * 50)

    state = research_graph.invoke(
        {
            "topic": topic,
            "rewrite_count": 0,
            "max_rewrites": max_rewrites,
        }
    )

    print("\n" + "=" * 50)
    print("STEP 1 - SEARCH AGENT")
    print("=" * 50)
    print(state.get("search_results", ""))

    print("\n" + "=" * 50)
    print("STEP 2 - READER AGENT")
    print("=" * 50)
    print(state.get("scraped_content", ""))

    print("\n" + "=" * 50)
    print("STEP 3 - WRITER (FINAL)")
    print("=" * 50)
    print(state.get("report", ""))

    print("\n" + "=" * 50)
    print("STEP 4 - CRITIC (FINAL)")
    print("=" * 50)
    print(state.get("feedback", ""))

    print("\n" + "=" * 50)
    print("LOOP STATS")
    print("=" * 50)
    print(f"Final Score: {state.get('score', 'N/A')}/10")
    print(f"Rewrites Used: {state.get('rewrite_count', 0)}")

    return {
        "search_results": state.get("search_results", ""),
        "scraped_content": state.get("scraped_content", ""),
        "report": state.get("report", ""),
        "feedback": state.get("feedback", ""),
        "score": state.get("score", 0),
        "rewrite_count": state.get("rewrite_count", 0),
    }


if __name__ == "__main__":
    topic = input("\nEnter a research topic: ")
    run_research_pipeline(topic, max_rewrites=3)