from langchain_core.pydantic_v1 import BaseModel, Field
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama import ChatOllama
from typing import List
# Instantiate the LLM model

model = ChatOllama(model="llama3.1")

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