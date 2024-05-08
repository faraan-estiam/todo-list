from fastapi import APIRouter, Depends, HTTPException
from typing import List
from classes.models import Task, TaskNoId
from routers.router_auth import get_current_user
from database.firebase import db
from uuid import uuid4

router = APIRouter(
  prefix='/todos',
  tags=["Todolist"]
)

@router.get('', response_model=List[Task])
async def get_todo_list(user_data: dict = Depends(get_current_user)):
  query_result = db.child('users').child(user_data['uid']).child('tasks').get(token=user_data['idToken']).val()
  if not query_result : return []
  return [task for task in query_result.values()]

@router.post('', response_model=Task,status_code=201)
async def create_task(todo: TaskNoId, user_data: dict = Depends(get_current_user)):
  uid = str(uuid4())
  new_task = Task(uid=uid, **todo.model_dump())
  db.child("users").child(user_data['uid']).child('tasks').child(uid).set(data=new_task.model_dump(), token=user_data['idToken'])
  return new_task

@router.get('/{task_id}', response_model=Task)
async def get_task(task_id:str, user_data: dict = Depends(get_current_user)):
  query_result = db.child('users').child(user_data['uid']).child('tasks').child(task_id).get(token=user_data['idToken']).val()
  if not query_result : raise HTTPException(status_code=404, detail='anime not found in watchlist')
  return query_result

@router.put('/{task_id}', response_model=Task)
async def update_task(task_id, todo: TaskNoId, user_data: dict = Depends(get_current_user)):
  old_task = await get_task(task_id=task_id, user_data=user_data)
  new_task = Task(uid=task_id, **todo.model_dump())
  db.child('users').child(user_data['uid']).child('tasks').child(task_id).set(data=new_task.model_dump(), token=user_data['idToken'])
  return new_task.model_dump()

@router.delete('/{task_id}')
async def delete_task(task_id, user_data: dict = Depends(get_current_user)):
  await get_task(task_id=task_id, user_data=user_data) #check if tasks exists
  db.child('users').child(user_data['uid']).child('tasks').child(task_id).remove(token=user_data['idToken'])