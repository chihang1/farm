from fastapi import FastAPI, Response, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from database import fetch_all_tasks, fetch_task, create_task, delete_task, update_task_data
from models import Task, UpdateTask, TaskResponseModel
from bson import ObjectId

# DB_URL = 'mongodb+srv://mircoservie-admin:OKDyp6FRXzjy8ieP@microservice-cluster.eqwwfmy.mongodb.net/?retryWrites=true&w=majority'
# DB_NAME = 'OSSDB'
# COLLECTION = 'vsot'

app = FastAPI()

origins = ['*'] # 'localhost:port

app.add_middleware(
    CORSMiddleware, 
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*']
    )

# @app.on_event('startup')
# async def InitMDB():
#     app.mongodb_client = AsyncIOMotorClient(DB_URL)
#     app.mongodb = app.mongodb_client[DB_NAME]
#     # app.collection = app.mongodb[COLLECTION]

@app.get('/haha')
async def helloWorld():
    return {'Hello': 'World'}

@app.get('/api/tasks')
async def get_all_tasks(response: Response) -> list[TaskResponseModel]:
    all_tasks = await fetch_all_tasks()
    response.status_code = status.HTTP_200_OK
    return all_tasks

@app.get('/api/tasks/{title}', response_model=TaskResponseModel)
async def get_task(title: str, response: Response) -> dict[TaskResponseModel]:
    task = await fetch_task({'title': title})
    if task:
        response.status_code = status.HTTP_200_OK
        return task
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Task: {title} does not exist.')

@app.post('/api/tasks', response_model=TaskResponseModel)
async def save_task(task: Task, response: Response) -> dict[TaskResponseModel]:
    print('Task: ', task)
    taskFound = await fetch_task({'title': task.title})
    if taskFound:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail='The task already exists.')
    new_task = await create_task(task.model_dump())
    if new_task:
        response.status_code = status.HTTP_201_CREATED
        return new_task
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Cannot create your task. Please check the json input.')

@app.put('/api/tasks/{id}')
async def update_task(id: str, data: UpdateTask, response: Response) -> dict:
    taskFound = await fetch_task({'_id': ObjectId(id)})
    if not taskFound:
        return False
    updated_task = await update_task_data(id, data)
    if updated_task:
        response.status_code = status.HTTP_200_OK
        return updated_task
    raise HTTPException(404, f'The task: {id} does not exist.')

@app.delete('/api/tasks/{id}')
async def remove_task(id: str, response: Response) -> dict:
    deleted_task = await delete_task(id)
    if deleted_task:
        response.status_code = status.HTTP_200_OK
        return {'details': f"Task: {id} is deleted"}
    raise HTTPException(404, f'The task:{id} does not exist.')

# @app.get('/oss-records', response_description='list all the oss files records', response_model=List[OssRecords])
# async def get_all_oss_records():
#     records = await collection.find().to_list()
#     return records
# 
# app.include_router(oss_routes)


