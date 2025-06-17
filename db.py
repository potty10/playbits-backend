from motor.motor_asyncio import AsyncIOMotorClient
from bson import ObjectId

from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel, EmailStr, Field

from llm import get_flashcards as generate_flashcards

# Models
class LessonBase(BaseModel):
    id: Optional[str] = None
    title: str
    summary: str
    content: str
    date_created: str

class FlashcardBase(BaseModel):
    lesson_id: str
    question: str
    answer: str

class GamecardBase(BaseModel):
    lesson_id: str
    content: str
    pair_number: int

class QuestionBase(BaseModel):
    lesson_id: str
    question: str
    options: List[str]
    answer: str



# Class
class DBManager:
    # Initialisation
    def __init__(self, uri: str, database_name: str):
        self.client = AsyncIOMotorClient(uri)
        self.db = self.client.get_database(database_name)
        self.lessons_collection = self.db.get_collection("lessons")
        self.flashcards_collection = self.db.get_collection("flashcards")
        self.gamecards_collection = self.db.get_collection("gamecards")
        self.questions_collection = self.db.get_collection("questions")


    # CRUD operations for lessons
    async def create_lesson(self, data: dict):
        lesson_model = LessonBase(**data)
        lessonbase_dict = lesson_model.model_dump()
        result = await self.lessons_collection.insert_one(lessonbase_dict)
        
        lessonbase_dict["id"] = str(result.inserted_id)
        return LessonBase(**lessonbase_dict)



    async def read_lesson_by_id(self, item_id: str):
        obj_id = ObjectId(item_id)
        item = await self.lessons_collection.find_one({"_id": obj_id})
        if item:
            # Convert _id ObjectId to string id if needed
            item["id"] = str(item["_id"])
            del item["_id"]
        return item

    
    async def read_all_lessons(self) -> list:
        items = []
        cursor = self.lesson_collection.find({})
        async for item in cursor:
            item["id"] = str(item["_id"]) 
            del item["_id"]
            items.append(item)
        return items

    # TODO: Update this again
    async def create_lesson_llm(self, title, content, summary=None):
        flashcards = generate_flashcards(content).questions
        new_item = {
            "title": title,
            "flashcards": [{"question": a.question, "answer": a.answer} for a in flashcards],
            "date_created": datetime.now()
        }
        if summary:
            new_item["summary"] = summary

        result = await self.lesson_collection.insert_one(new_item)
        return await self.read_lesson_by_id(result.inserted_id)
    


    # CRUD operations for flashcards
    async def create_flashcard(self, data: FlashcardBase) -> FlashcardBase:
        flashcard_dict = data.model_dump()
        result = await self.flashcards_collection.insert_one(flashcard_dict)

        flashcard_dict["id"] = str(result.inserted_id)
        return FlashcardBase(**flashcard_dict)



    async def create_flashcards_for_lesson(self, lesson_id: str, flashcards: List[dict]):
        # Add lesson_id to each flashcard dict
        flashcards_to_insert = []
        for fc in flashcards:
            flashcards_to_insert.append({
                "lesson_id": lesson_id,
                "question": fc["front_content"],
                "answer": fc["back_content"]
            })
        
        result = await db_manager.flashcards_collection.insert_many(flashcards_to_insert)
        return result.inserted_ids
    


  

    async def create_gamecards_for_lesson(self, lesson_id: str, gamecards: List[dict]):
        try:
            gamecards_to_insert = []
            for gc in gamecards:
                gamecards_to_insert.append({
                    "lesson_id": lesson_id,
                    "content": gc["content"],  # or gc.get("front_content")
                    "pair_number": int(gc["pair"])
                })

            result = await self.gamecards_collection.insert_many(gamecards_to_insert)
            return result.inserted_ids
        except Exception as e:
            return []
        

    

    async def create_questions_for_lesson(self, lesson_id: str, questions: List[dict]):
        try:
            questions_to_insert = []
            for q in questions:
                questions_to_insert.append({
                    "lesson_id": lesson_id,
                    "question": q["question"],
                    "options": q["options"],  # Ensure this is a list of 4 strings
                    "answer": q["answer"]
                })

            if not questions_to_insert:
                raise ValueError("No valid questions to insert.")

            result = await self.questions_collection.insert_many(questions_to_insert)
            return result.inserted_ids

        except Exception as e:
            print(f"Error inserting questions: {e}")
            return []






























    async def read_flashcards_by_lesson_id(self, lesson_id: str) -> List[FlashcardBase]:
        cursor = self.flashcards_collection.find({"lesson_id": lesson_id})
        flashcard_results = []

        async for document in cursor:
            document["id"] = str(document["_id"])
            del document["_id"]
            flashcard_results.append(FlashcardBase(**document))
        
        return flashcard_results
    

    # CRUD operations for game cards
    async def create_gamecard(self, data: GamecardBase) -> GamecardBase:
        gamecard_dict = data.model_dump()
        result = await self.gamecards_collection.insert_one(gamecard_dict)

        gamecard_dict["id"] = str(result.inserted_id)
        return GamecardBase(**gamecard_dict)

    async def read_gamecards_by_lesson_id(self, lesson_id: str) -> List[GamecardBase]:
        cursor = self.gamecards_collection.find({"lesson_id": lesson_id})
        gamecard_results = []

        async for document in cursor:
            document["id"] = str(document["_id"])
            del document["_id"]
            gamecard_results.append(GamecardBase(**document))
        
        return gamecard_results
    

    # CRUD operations for questions
    async def create_question(self, data: QuestionBase) -> QuestionBase:
        question_dict = data.model_dump()
        result = await self.questions_collection.insert_one(question_dict)

        question_dict["id"] = str(result.inserted_id)
        return QuestionBase(**question_dict)

    async def read_questions_by_lesson_id(self, lesson_id: str) -> List[QuestionBase]:
        cursor = self.questions_collection.find({"lesson_id": lesson_id})
        question_results = []

        async for document in cursor:
            document["id"] = str(document["_id"])
            del document["_id"]
            question_results.append(QuestionBase(**document))
        
        return question_results


db_manager = DBManager(uri="mongodb://localhost:27017", database_name="db_local")