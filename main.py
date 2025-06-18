from bson import ObjectId
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Optional
from uuid import UUID, uuid4
from db import db_manager
from typing import List
from llm import generate_summary, generate_flashcards, generate_gamecards, generate_questions
from datetime import datetime
from fastapi.middleware.cors import CORSMiddleware








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


# Add CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



class LessonRequest(BaseModel):
    content: str

@app.post("/lessons")
async def create_lesson(request: LessonRequest):  
    try:
        # Step 1: Generate title summary
        title, summary = await generate_summary(request.content)
        

        #  Step 2: Store title and summary
        lesson_doc = {
            "title": title,
            "summary": summary,
            "content": request.content,
            "date_created": datetime.now().strftime("%d-%m-%Y")
        }
        lesson_inserted = await db_manager.create_lesson(lesson_doc)


        # Step 3: Generate flash cards
        lesson_id = lesson_inserted.id
        flashcards = await generate_flashcards(request.content)
        inserted_flashcard_ids = await db_manager.create_flashcards_for_lesson(lesson_id, flashcards)


        # Step 4: Generate game cards
        gamecards = await generate_gamecards(request.content)
        inserted_gamecard_ids = await db_manager.create_gamecards_for_lesson(lesson_id, gamecards)


        # Step 5: Generate questions
        questions = await generate_questions(request.content)
        inserted_question_ids = await db_manager.create_questions_for_lesson(lesson_id, questions)

        return JSONResponse(
            status_code=201,
            content= {
                "message": "Lesson created successfully",
                "lesson_title": title,
                "lesson_id": lesson_id,
                "flashcards_inserted": len(inserted_flashcard_ids),
                "gamecards_inserted": len(inserted_gamecard_ids),
                "questions_inserted": len(inserted_question_ids)
            }
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))



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
