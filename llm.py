from langchain_core.pydantic_v1 import BaseModel, Field
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from typing import List
import os
# Instantiate the LLM model


api_key = os.getenv("OPENAI_API_KEY")

# model = ChatOllama(model="llama3.1")
model = ChatOpenAI(
    model="gpt-4o",
    temperature=0,
    api_key="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"
    # max_tokens=None,
    # timeout=None,
    # max_retries=2,
    # api_key="...",  # if you prefer to pass api key in directly instaed of using env vars
    # base_url="...",
    # organization="...",
    # other params...
)
class Trivia(BaseModel):
    question: str = Field(description="The trivia question")
    answer: str = Field(description="The correct answer to the trivia question")

class QAList(BaseModel):
    questions: List[Trivia] = Field(description="List of question and answer pairs")

# Define the prompt template
template = """
Give me a list of trivia question from the context below, respond in JSON that contains the key `questions`. The value for the `questions` key should an array of at least 2 JSON objects. Each object has `question` and `answer` keys.

context:{topic}
"""

prompt = ChatPromptTemplate.from_template(
    template
)

structured_llm = model.with_structured_output(QAList, method="json_mode")

# Chain the prompt and structured LLM using the pipe operator

trivia_chain = prompt | structured_llm

# Invoke the chain
def get_flashcards(topic: str):
    result = trivia_chain.invoke({"topic": topic})
    return result