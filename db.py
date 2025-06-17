from motor.motor_asyncio import AsyncIOMotorClient
from bson import ObjectId

from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel, EmailStr, Field

from llm import get_flashcards as generate_flashcards


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

# class LessonBase(BaseModel):
#     title: str
#     summary: Optional[str] = None
#     content: str
#     date_created: datetime = Field(default_factory=datetime.now(datetime.timezone.utc))
#     flashcards: List[FlashcardBase]
#     game_cards: List[GamecardBase]
#     questions: List[QuestionBase]

class DBManager:
    def __init__(self, uri: str, database_name: str):
        self.client = AsyncIOMotorClient(uri)
        self.db = self.client.get_database(database_name)
        self.lesson_collection = self.db.get_collection("lessons")

    async def create_item(self, item):
        result = await self.lesson_collection.insert_one(item)
        return await self.read_item(result.inserted_id)

    async def read_item(self, item_id: ObjectId):
        item = await self.lesson_collection.find_one({"_id": item_id})
        if item:
            item["id"] = str(item["_id"])
            del item["_id"]
        return item

    async def read_items(self) -> list:
        items = []
        cursor = self.lesson_collection.find({})
        async for item in cursor:
            item["id"] = str(item["_id"])
            del item["_id"]
            items.append(item)
        return items

    async def update_item(self, item_id: ObjectId, item):
        await self.lesson_collection.update_one({"_id": item_id}, {"$set": item})
        return await self.read_item(item_id)

    async def delete_item(self, item_id: ObjectId) -> bool:
        result = await self.lesson_collection.delete_one({"_id": item_id})
        return result.deleted_count > 0

    async def create_lesson(self, title, content, summary=None):
        flashcards = generate_flashcards(content).questions
        new_item = {
            "title": title,
            "flashcards": [{"question": a.question, "answer": a.answer} for a in flashcards],
            "date_created": datetime.now()
        }
        if summary:
            new_item["summary"] = summary

        result = await self.lesson_collection.insert_one(new_item)
        return await self.read_item(result.inserted_id)
    
    async def read_lessons(self) -> list:
        items = []
        cursor = self.lesson_collection.find({})
        async for item in cursor:
            item["id"] = str(item["_id"])
            del item["_id"]
            items.append(item)
        return items
    
    async def read_lesson(self, item_id: ObjectId):
        item = await self.lesson_collection.find_one({"_id": item_id})
        if item:
            item["id"] = str(item["_id"])
            del item["_id"]
        return item
    
db_manager = DBManager(uri="mongodb://localhost:27017", database_name="db_local")