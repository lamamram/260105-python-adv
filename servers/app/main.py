# pip install fastapi[standard]
# lancer le serveur de dev avec fastapi dev /path/to/main.py
from fastapi import FastAPI
# redirection http d'une route avec/ sur sans 
from fastapi.responses import RedirectResponse
from starlette.middleware.trustedhost import TrustedHostMiddleware
from starlette.middleware.base import BaseHTTPMiddleware

class RedirectSlashMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        path = request.url.path
        if path.endswith('/') and path != '/':
            # Construire l'URL manuellement
            query = f"?{request.url.query}" if request.url.query else ""
            redirect_url = f"{path.rstrip('/')}{query}"
            return RedirectResponse(url=redirect_url, status_code=307)
        return await call_next(request)

# import direct à partir d'un package routers grâce à son __init__.py
from .routers import user_router

app = FastAPI(title="User API")

# Ajouter le middleware AVANT d'inclure les routers
app.add_middleware(RedirectSlashMiddleware)

@app.get("/", status_code=200)
def root() -> dict:
  return {"msg": "Hello World"}

app.include_router(user_router)
