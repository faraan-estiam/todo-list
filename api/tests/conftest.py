from firebase_admin import auth
from main import api
from fastapi.testclient import TestClient
import pytest
from database.firebase import db
from classes.models import Task
from uuid import uuid4

client = TestClient(api)

@pytest.fixture()
def create_user():
  client.post("/auth/signup", json= {
    "email": "test.useralreadyexists@gmail.com",
    "password": "password"
  })

@pytest.fixture()
def auth_user(create_user):
  user_credentials = client.post("auth/login", data={
    "username": "test.useralreadyexists@gmail.com",
    "password": "password"
  })
  return user_credentials.json()

@pytest.fixture()
def task_uid(auth_user):
  user_data = client.get("auth/me", headers= {'Authorization': f"Bearer {auth_user['access_token']}"}).json()
  uid= str(uuid4())
  db.child('users').child(user_data['uid']).child('tasks').child(uid).set(data=Task(uid=uid, title="title", description="description", status=0).model_dump(), token=user_data['idToken'])
  return uid

def remove_test_todos():
  user_credentials = client.post("auth/login", data={
    "username": "test.useralreadyexists@gmail.com",
    "password": "password"
  })
  user_token = f"Bearer {user_credentials.json()['access_token']}"
  user_data = client.get("auth/me", headers= {'Authorization': user_token}).json()
  db.child('users').child(user_data['uid']).remove(token=user_data['idToken'])

def remove_test_users():
  remove_test_todos()
  users = auth.list_users().iterate_all()
  for user in users:
    if user.email.startswith("test."):
      auth.delete_user(user.uid)

@pytest.fixture(scope="module", autouse=True)
def cleanup(request):
  request.addfinalizer(remove_test_users)
