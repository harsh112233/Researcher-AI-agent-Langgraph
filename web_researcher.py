from typing import Dict, Any, TypedDict
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage
from langchain_community.tools import DuckDuckGoSearchRun
from langgraph.graph import StateGraph, END
import sys

load_dotenv()

    #tools and models
search_tool = DuckDuckGoSearchRun()
llm = ChatOpenAI(model="gpt-4-turbo-preview")

    #state structure
class ResearchState(TypedDict):
    query: str
    search_results_1: str
    analysis_1: str
    report_1: str

def search_web(state: Dict[str, Any]) -> Dict[str, Any]:
    query = state["query"]
    search_results = search_tool.invoke(query)
    state["search_results_1"] = search_results
    return state

def analyze_results(state: Dict[str, Any]) -> Dict[str, Any]:
    messages = [
        HumanMessage(content=f"""
        Based on these search results about {state['query']}, provide a detailed analysis:
        {state['search_results_1']}
        Focus on key insights, trends, and important information.
        """)
    ]
    response = llm.invoke(messages)
    state["analysis_1"] = response.content
    return state

def generate_report(state: Dict[str, Any]) -> Dict[str, Any]:
    messages = [
        HumanMessage(content=f"""
        Create a comprehensive research report about {state['query']} based on this analysis:
        {state['analysis_1']}
        Format the report with clear sections, key findings, and conclusions.
        """)
    ]
    response = llm.invoke(messages)
    state["report_1"] = response.content
    return state

def should_continue_research(state: Dict[str, Any]) -> str:
    messages = [
        HumanMessage(content=f"""
        Based on the current analysis, determine if more research is needed about {state['query']}.
        Current findings:
        {state['analysis_1']}
        
        Respond with 'continue' if more research is needed, or 'complete' if the information is sufficient.
        """)
    ]
    response = llm.invoke(messages)
    return "continue_research" if "continue" in response.content.lower() else END

def create_research_graph():
    workflow = StateGraph(ResearchState)
    
    # Add nodes
    workflow.add_node("search", search_web)
    workflow.add_node("analyze", analyze_results)
    workflow.add_node("report", generate_report)
    
    # Define edges
    workflow.add_edge("search", "analyze")
    workflow.add_edge("analyze", "report")
    workflow.add_conditional_edges(
        "report",
        should_continue_research,
        {
            "continue_research": "search",
            END: END
        }
    )
    
    workflow.set_entry_point("search")
    return workflow.compile()

def main(query: str) -> Dict[str, Any]:
    graph = create_research_graph()
    state = {"query": query}
    result = graph.invoke(state)
    
    report_filename = f"research_report_{query.replace(' ', '_')}.txt"
    with open(report_filename, "w", encoding="utf-8") as f:
        f.write(result["report_1"])
    
    print(f"\nResearch complete! Report saved to {report_filename}")
    return result

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Please provide a research query.")
        sys.exit(1)
    
    query = " ".join(sys.argv[1:])
    main(query)