from agents import build_reader_agent , build_search_agent , writer_chain , critic_chain

def run_research_pipeline(topic : str) -> dict:

    state = {}

    #search agent working 
    print("\n"+" ="*50)
    print("step 1 - search agent is working ...")
    print("="*50)

    search_agent = build_search_agent()
    search_result = search_agent.invoke({
        "messages" : [
            ("user", f"You MUST use the web_search tool to answer. Do NOT answer from your own knowledge. Return at least 3 URLs with titles and snippets for: {topic}.")
        ]
    })
    # state["search_results"] = search_result['messages'][-1].content
    content = search_result['messages'][-1].content
    if isinstance(content, list) and len(content) > 0 and isinstance(content[0], dict) and 'text' in content[0]:
        state["search_results"] = content[0]['text']
    elif isinstance(content, dict) and 'text' in content:
        state["search_results"] = content['text']
    else:
        state["search_results"] = content

    print("\n search result ",state['search_results'])

    #step 2 - reader agent 
    print("\n"+" ="*50)
    print("step 2 - Reader agent is scraping top resources ...")
    print("="*50)


    reader_agent = build_reader_agent()
    reader_result = reader_agent.invoke({
        "messages": [("user",
            f"Based on the following search results about '{topic}', "
            f"pick the most relevant URL and scrape it for deeper content.\n\n"
            f"Search Results:\n{state['search_results'][:800]}"
        )]
    })

    # state['scraped_content'] = reader_result['messages'][-1].content
    content = reader_result['messages'][-1].content
    if isinstance(content, list) and len(content) > 0 and isinstance(content[0], dict) and 'text' in content[0]:
        state['scraped_content'] = content[0]['text']
    elif isinstance(content, dict) and 'text' in content:
        state['scraped_content'] = content['text']
    else:
        state['scraped_content'] = content

    print("\nscraped content: \n", state['scraped_content'])

    #step 3 - writer chain 

    print("\n"+" ="*50)
    print("step 3 - Writer is drafting the report ...")
    print("="*50)

    research_combined = (
        f"SEARCH RESULTS : \n {state['search_results']} \n\n"
        f"DETAILED SCRAPED CONTENT : \n {state['scraped_content']}"
    )

    state["report"] = writer_chain.invoke({
        "topic" : topic,
        "research" : research_combined
    })

    print("\n Final Report\n",state['report'])

    #critic report 

    print("\n"+" ="*50)
    print("step 4 - critic is reviewing the report ")
    print("="*50)

    state["feedback"] = critic_chain.invoke({
        "report":state['report']
    })

    print("\n critic report \n", state['feedback'])

    return state



if __name__ == "__main__":
    topic = input("\n Enter a research topic : ")
    run_research_pipeline(topic)
