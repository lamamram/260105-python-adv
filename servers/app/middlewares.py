# redirection http d'une route avec/ sur sans 
from fastapi.responses import RedirectResponse
# fastapi repose sur le serveur HTTP starlette
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