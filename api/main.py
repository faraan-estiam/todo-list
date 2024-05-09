from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Documentation
from documentation.description import api_description
from documentation.tags import tags_metadata

#Importing routes
import routers.router_auth
import routers.router_todos

api = FastAPI(
  title="todo-list-api",
  description=api_description,
  openapi_tags=tags_metadata,
  docs_url='/'
)

origins = [
    "*"
]

api.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

api.include_router(routers.router_auth.router)
api.include_router(routers.router_todos.router)