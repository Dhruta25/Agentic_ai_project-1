from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
from ai_agent import get_response_from_agent

app = FastAPI(title="LangGraph AI Agent")

ALLOWED_MODEL_NAMES = [
    "llama3-70b-8192",
    "mixtral-8x7b-32768",
    "llama-3.3-70b-versatile",
    "gpt-4o"
]

class RequestState(BaseModel):
    model_name: str
    model_provider: str
    model_prompt: str
    messages: List[str]
    allow_search: bool

@app.post("/chat")
def chat_endpoint(request: RequestState):
    if request.model_name not in ALLOWED_MODEL_NAMES:
        return {"error": "Kindly select a valid model name"}
    
    llm_id = request.model_name
    query = request.messages[-1]
    allow_search = request.allow_search
    system_prompt = request.model_prompt
    provider = request.model_provider

    return get_response_from_agent(
        llm_id=llm_id,
        query=query,
        allow_search=allow_search,
        system_prompt=system_prompt,
        provider=provider
    )
    


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=9999 )
