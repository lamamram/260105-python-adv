# pip install fastapi[standard]
# lancer le serveur de dev avec fastapi dev /path/to/main.py
from fastapi import FastAPI
# import direct à partir d'un package routers grâce à son __init__.py
from .routers import user_router

app = FastAPI(title="User API")

@app.get("/", status_code=200)
def root() -> dict:
  return {"msg": "Hello World"}

app.include_router(user_router)
