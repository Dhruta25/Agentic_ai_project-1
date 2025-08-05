import os
from dotenv import load_dotenv
load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
from langchain_groq import ChatGroq
from langchain_openai import ChatOpenAI
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_core.messages import AIMessage
openai_llm = ChatOpenAI(model="gpy-4o", api_key = OPENAI_API_KEY)
groq_llm = ChatGroq(model="llama-3.3-70b-versatile")

search_tool = TavilySearchResults(max_results = 2)
from langgraph.prebuilt import create_react_agent
system_prompt = "Act as an AI chatbot who smart and friendly"
def get_response_from_agent(llm_id, query , allow_search , system_prompt , provider):
    if provider == "Groq":
        llm = ChatGroq(model = llm_id)
    elif provider == "OpenAI":
        llm = ChatOpenAI(model = llm_id)
    tools = [TavilySearchResults(max_results = 2)] if allow_search else []
    agent = create_react_agent(

        model = groq_llm,
        tools = tools,
        state_modifier = system_prompt

    )
    state = {"messages" : query}
    response = agent.invoke(state)
    messages = response.get("messages")
    ai_messages = [message.content for message in messages if isinstance(message, AIMessage)]
    return {"response" : ai_messages[-1]}