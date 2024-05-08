from pydantic import BaseModel

class Todo(BaseModel):
  uid: str
  title: str
  description: str
  status: int

class TodoNoId(BaseModel):
  title: str
  description: str
  status: int

class User(BaseModel):
  email: str
  password: str