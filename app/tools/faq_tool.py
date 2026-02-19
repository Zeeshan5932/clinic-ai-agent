from typing import Dict, Any
from langchain.llms import OpenAI
from app.config import settings

llm = OpenAI(model_name="gpt-4o", openai_api_key=settings.OPENAI_API_KEY)

PROMPT_TEMPLATE = """
You are a helpful assistant for a clinic. Answer the following question concisely:
{question}
"""

def answer_faq(state: Dict[str, Any]) -> str:
    question = state.get("question")
    if not question:
        return "I didn't get a question to answer."
    prompt = PROMPT_TEMPLATE.format(question=question)
    response = llm(prompt)
    return response
