from fastapi import FastAPI

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

api.include_router(routers.router_auth.router)
api.include_router(routers.router_todos.router)