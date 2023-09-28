from motor.motor_asyncio import AsyncIOMotorClient
from models import Task, UpdateTask
from pymongo.server_api import ServerApi
import asyncio
from bson import ObjectId

DB_URI = 'mongodb+srv://farm-admin:0AVDhYfewlNgjFRq@hellomongo.v37cvu2.mongodb.net/?authSource=HelloMongo&authMechanism=SCRAM-SHA-1' # 'mongodb://localhost:27017'

client = AsyncIOMotorClient(DB_URI, server_api=ServerApi('1'))
database = client['FirstMongo']
collection = database.get_collection('Task')

def task_handler(task):
    return {
        'id': str(task['_id']),
        'title': task['title'],
        'description': task['description'],
        'completed': task['completed']
    }

async def fetch_all_tasks():
    tasks = []
    async for document in collection.find({}):
        tasks.append(task_handler(document))
    return tasks    

# async def fetch_task(title: str):
async def fetch_task(query_dict: dict):
    document = await collection.find_one(query_dict)
    if document:
        return task_handler(document)
    return False

async def create_task(task: Task):
    new_task = await collection.insert_one(task)
    created_task = await collection.find_one({'_id': new_task.inserted_id})
    return task_handler(created_task)

async def update_task_data(id: str, data: UpdateTask):
    task = {k:v for k, v in data.model_dump().items() if v is not None}
    await collection.update_one({'_id': ObjectId(id)}, {'$set': task}) # update task
    document = await collection.find_one({'_id': ObjectId(id)}) # Find the updated task
    return task_handler(document)

async def delete_task(id: str):
    task = await collection.find_one({'_id': ObjectId(id)})
    if task:
        await collection.delete_one({'_id': ObjectId(id)}) # delete task
        return True
    return False