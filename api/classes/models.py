from pydantic import BaseModel

class Task(BaseModel):
  uid: str
  title: str
  description: str
  status: int

class TaskNoId(BaseModel):
  title: str
  description: str
  status: int

class User(BaseModel):
  email: str
  password: str