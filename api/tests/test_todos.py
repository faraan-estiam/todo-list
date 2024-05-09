from fastapi.testclient import TestClient
import pytest
from main import api
from classes.models import TaskNoId

client = TestClient(api)

#test unauthorized for all routes
@pytest.mark.parametrize("route,method,body", [
  ("/todos", 'GET', None),
  ("/todos", 'POST', TaskNoId(title="title", description="description", status=0).model_dump()),
  ("/todos/taskUID", 'GET', None),
  ("/todos/taskUID", 'PUT', TaskNoId(title="title", description="description", status=0).model_dump()),
  ("/todos/taskUID", 'DELETE', None)
])
def test_unauthorized(route, method, body):
  if (method == "GET"):
    response = client.get(route)
  elif (method == "POST"):
    response = client.post(route, json=body)
  elif (method == "PUT"):
    response = client.put(route, json=body)
  elif (method == "PATCH"):
    response = client.patch(route, json=body)
  elif (method == "DELETE"):
    response = client.delete(route)
  
  assert response.status_code == 401

#tests /todos
def test_get_empty_todos(auth_user):
  response = client.get("/todos", headers= {"Authorization" : f"Bearer {auth_user['access_token']}"})
  assert response.status_code == 200
  assert response.json() == []

def test_post_todos(auth_user):
  response = client.post("/todos", headers= {"Authorization" : f"Bearer {auth_user['access_token']}"}, json=TaskNoId(title="title", description="description", status=0).model_dump())
  assert response.status_code == 201

def test_get_todos(auth_user):
  response = client.get("/todos", headers= {"Authorization" : f"Bearer {auth_user['access_token']}"})
  assert response.status_code == 200
  assert len(response.json()) > 0

#tests /todos/id


@pytest.mark.parametrize("route,method,body", [
  ("/todos/taskUID", 'GET', None),
  ("/todos/taskUID", 'PUT', TaskNoId(title="title", description="description", status=0).model_dump()),
  ("/todos/taskUID", 'DELETE', None)
])
def test_notfound(route, method, body, auth_user):
  if (method == "GET"):
    response = client.get(route, headers= {"Authorization" : f"Bearer {auth_user['access_token']}"})
  elif (method == "POST"):
    response = client.post(route, json=body, headers= {"Authorization" : f"Bearer {auth_user['access_token']}"})
  elif (method == "PUT"):
    response = client.put(route, json=body, headers= {"Authorization" : f"Bearer {auth_user['access_token']}"})
  elif (method == "PATCH"):
    response = client.patch(route, json=body, headers= {"Authorization" : f"Bearer {auth_user['access_token']}"})
  elif (method == "DELETE"):
    response = client.delete(route, headers= {"Authorization" : f"Bearer {auth_user['access_token']}"})
  
  assert response.status_code == 404

def test_get_task(auth_user, task_uid):
  response = client.get(f'/todos/{task_uid}', headers= {"Authorization" : f"Bearer {auth_user['access_token']}"})
  assert response.status_code == 200

def test_put_task(auth_user, task_uid):
  response = client.put(f"/todos/{task_uid}", json=TaskNoId(title="title", description="description", status=0).model_dump(), headers= {"Authorization" : f"Bearer {auth_user['access_token']}"})
  assert response.status_code == 200

def test_delete_task(auth_user, task_uid):
  response = client.delete(f"/todos/{task_uid}", headers= {"Authorization" : f"Bearer {auth_user['access_token']}"})
  assert response.status_code == 200