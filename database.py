from typing import Union

import motor.motor_asyncio
from bson import ObjectId
from decouple import config

MONGO_API_KEY = config("MONGO_API_KEY")

client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_API_KEY)
database = client.API_DB
collenction_todo = database.todo
collenction_user = database.user


def todo_serializer(todo) -> dict:
    return {
        "id": str(todo["_id"]),
        "title": todo["title"],
        "description": todo["description"],
    }


async def db_create_todo(data: dict) -> Union[dict, bool]:
    todo = await collenction_todo.insert_one(data)
    new_todo = await collenction_todo.find_one({"_id": todo.inserted_id})
    if new_todo:
        return todo_serializer(new_todo)
    return False


async def db_get_todos() -> list:
    todos = []
    for todo in await collenction_todo.find().to_list(length=100):
        todos.append(todo_serializer(todo))
    return todos


async def db_get_single_todo(id: str) -> Union[dict, bool]:
    todo = await collenction_todo.find_one({"_id": ObjectId(id)})
    if todo:
        return todo_serializer(todo)
    return False


async def db_update_todo(id: str, data: dict) -> Union[dict, bool]:
    todo = await collenction_todo.find_one({"_id": ObjectId(id)})
    if todo:
        updated_todo = await collenction_todo.update_one(
            {"_id": ObjectId(id)}, {"$set": data}
        )
        if(updated_todo.modified_count > 0):
            new_todo = await collenction_todo.find_one({"_id": ObjectId(id)})
            return todo_serializer(new_todo)
    return False


async def db_delete_todo(id: str) -> bool:
    todo = await collenction_todo.find_one({"_id": ObjectId(id)})
    if todo:
        deleted_todo = await collenction_todo.delete_one({"_id": ObjectId(id)})
        if(deleted_todo.deleted_count > 0):
            return True
    return False
