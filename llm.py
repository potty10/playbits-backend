from langchain_core.pydantic_v1 import BaseModel, Field
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from typing import List
from dotenv import load_dotenv
import json
import os

# Instantiate the LLM model


load_dotenv()

# model = ChatOllama(model="llama3.1")
model = ChatOpenAI(
    model="gpt-4.1",
    temperature=1,
    api_key=os.getenv('OPENAI_API_KEY')
)





### TASK 1: Summary
class FlashcardOutput(BaseModel):
    title: str
    summary: str


summary_prompt = """
### Instructions
Given the context, you intend to create a revision flow for it. Give a title for the revision flow and provide a 3-line summary of the content.

# Output Format
Generate a structured output in the form of JSON with fields for a title and a summary based on the given input.

- The output should be a JSON object with the following format:  
  {{ "title": "Your title here", "summary": "Your summary here" }}

# Notes
- Ensure the output adheres to the JSON structure strictly.
- Provide relevant and concise content for both the title and summary fields.

context: {content}
"""


async def generate_summary(content: str):
    prompt = summary_prompt.format(content=content)

    response = await model.ainvoke([
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": prompt}
    ])

    # Extract text and parse JSON
    try:
        parsed = json.loads(response.content)
        return parsed["title"], parsed["summary"]
    except Exception as e:
        raise ValueError(f"Failed to parse model response: {response.content}") from e
    




### TASK 2: Generate flashcards
flashcard_prompt = """
### Instructions
Given the context below, you intend to create flashcards that identify key concepts.

Context:
{content}

# Output Format
Generate a structured output in JSON with a key "flashcards" that holds an array of flashcard objects. Each flashcard object has "front_content" for the question, and "back_content" for the answer.

Generate as many flashcards as you can, up to a maximum of 6 flashcards. Do not use content outside of the content provided to you. The content of flash cards should be unique and not duplicate information.
If you have not enough content, you can generate less than 6 flashcards.

- The output should be a JSON object like this:
{{
  "flashcards": [
    {{ "front_content": "Your question here", "back_content": "Your answer here" }},
    {{ "front_content": "Another question", "back_content": "Another answer" }}
  ]
}}

# Notes
- Ensure the output adheres strictly to the JSON structure.
- Provide relevant and concise content for the question and answer.


"""


async def generate_flashcards(content: str):
    prompt = flashcard_prompt.format(content=content)

    response = await model.ainvoke([
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": prompt}
    ])

    # Extract text and parse JSON
    try:
        parsed = json.loads(response.content)
        flashcards = parsed.get("flashcards", [])
        return flashcards
    except Exception as e:
        raise ValueError(f"Failed to parse model response: {response.content}") from e





















### TASK 3: Generate game cards
gamecard_prompt = """
### Instructions
Given the context, you intend to create flip-and-match cards for it. The objective is to help the learner to reinforce connections and find patterns.

Context:
{content}

# Output Format
Generate a structured output in JSON with a key "gamecards" that holds an array of gamecard objects. Cards that match form a pair, and should thus share a pair number.

Generate as many pairs as you can, up to a maximum of 8 pairs. Do not use content outside of the content provided to you. The content of game cards should be unique and not duplicate information, where
each pair should aim to reinforce something different.

If you have not enough content, you can generate less than 8 pairs of game cards.

- The output should be a JSON object like this:
{{
  "gamecards": [
    {{ "content": "Your content here", "pair_number": "Your pair number here" }},
    {{ "content": "Your content here", "pair_number": "Your pair number here" }}
  ]
}}

# Notes
- Ensure the output adheres strictly to the JSON structure.
- Provide relevant and concise content for the question and answer.


"""


async def generate_gamecards(content: str):
    prompt = gamecard_prompt.format(content=content)

    response = await model.ainvoke([
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": prompt}
    ])

    # Extract text and parse JSON
    try:
        parsed = json.loads(response.content)
        gamecards = parsed.get("gamecards", [])
        return gamecards
    except Exception as e:
        raise ValueError(f"Failed to parse model response: {response.content}") from e













### TASK 4: Generate questions
questions_prompt = """
### Instructions
Given the context, you intend to create fill-in-the-blank questions for it. The objective is to test the learner's understanding of the main points in the context.

Context:
{content}

### Output Format
Generate a structured output in JSON with a key `"questions"` that holds an array of question objects. Each object must include:

- `"question"`: a string with a single blank represented by **exactly 8 underscores**, e.g., `"Plants make food through ________."`
- `"options"`: an array of **exactly 4 strings** (e.g., `["Option A", "Option B", "Option C", "Option D"]`)
- `"answer"`: one of the strings from the `options` array

If there is not enough content to generate 5 questions, you may generate fewer.

### Constraints
- Each question should test a **distinct** concept from the context. Avoid repeating the same idea in multiple questions.
- Do **not** use information not found in the provided context.
- Strictly follow this JSON structure:

{{
  "questions": [
    {{
      "question": "Your fill-in-the-blank question here",
      "options": ["Option 1", "Option 2", "Option 3", "Option 4"],
      "answer": "Correct option from above"
    }},
    {{
      "question": "Another fill-in-the-blank question here",
      "options": ["Option A", "Option B", "Option C", "Option D"],
      "answer": "Correct option from above"
    }}
  ]
}}
"""

async def generate_questions(content: str):
    prompt = questions_prompt.format(content=content)

    response = await model.ainvoke([
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": prompt}
    ])

    # Extract text and parse JSON
    try:
        parsed = json.loads(response.content)
        questions = parsed.get("questions", [])
        return questions
    except Exception as e:
        raise ValueError(f"Failed to parse model response: {response.content}") from e

























# summary_prompt = ChatPromptTemplate.from_template(summary_template)
# structured_summary_llm = model.with_structured_output(SummaryOutput, method="json_mode")
# summary_chain = summary_prompt | structured_summary_llm

























































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