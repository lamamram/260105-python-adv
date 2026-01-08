# pip install fastapi[standard]
# lancer le serveur de dev avec fastapi dev /path/to/main.py
from fastapi import FastAPI

# charger les middlewares (mécanismes internes de FastAPI customisés )
from .middlewares import RedirectSlashMiddleware

# import direct à partir d'un package routers grâce à son __init__.py
from .routers import *

# debug = True => affiche les prints dans le terminal
app = FastAPI(title="Person API", debug=True)

# Ajouter le middleware AVANT d'inclure les routers
app.add_middleware(RedirectSlashMiddleware)

# par défaut la réponse utilise la classe response_class=JSONResponse
@app.get("/", status_code=200)
def root() -> dict:
  return {"msg": "Hello World"}

app.include_router(user_router)
app.include_router(auth_router)
