from bson import ObjectId
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
from uuid import UUID, uuid4
from db import db_manager
from typing import List

# import the .env file
from dotenv import load_dotenv
load_dotenv()
class Item(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    on_offer: bool = False


class Lesson(BaseModel):
    title: str
    content: str

app = FastAPI()



@app.post("/lessons/")
async def create_lesson(lesson: Lesson):   
    new_item = await db_manager.create_lesson_llm(lesson.title, lesson.content)
    return new_item

# Get all lessons
@app.get("/lessons/")
async def read_lessons():
    return await db_manager.read_all_lessons()

@app.get("/lessons/{lesson_id}")
async def read_lesson(lesson_id: str):
    item = await db_manager.read_lesson_by_id(lesson_id)
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return item


@app.get("/flashcards/{lesson_id}")
async def read_flashcards(lesson_id: str):
    item = await db_manager.read_flashcards_by_lesson_id(lesson_id)
    if item is None:
        raise HTTPException(status_code=404, detail="Flashcards not found")
    return item


@app.get("/gamecards/{lesson_id}")
async def read_gamecards(lesson_id: str):
    item = await db_manager.read_gamecards_by_lesson_id(lesson_id)
    if item is None:
        raise HTTPException(status_code=404, detail="Gamecards not found")
    return item


@app.get("/questions/{lesson_id}")
async def read_questions(lesson_id: str):
    item = await db_manager.read_questions_by_lesson_id(lesson_id)
    if item is None:
        raise HTTPException(status_code=404, detail="Questions not found")
    return item
