"""
ensemble de routes concerant les ressources utilisateurs
attention: les routes sont détectées par des regex
par défaut écrivez les routes dans l'ordre des plus singuliers vers les plus générique
"""
from fastapi import APIRouter, Query, HTTPException, status, Request, Depends
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from sqlalchemy import select
from ..orm.database import get_db
from ..orm.models import User as UserModel

# type de donées avec un objet de type donné OU None
from typing import Optional
from .user_schemas import *
from pathlib import Path
from ..auth import verify_token

user_router = APIRouter(prefix="/users")

BASE_PATH = Path(__file__).resolve().parent.parent
TEMPLATES = Jinja2Templates(directory=str(BASE_PATH / "templates"))

@user_router.get("/home", status_code=200)
def home(request: Request, db: Session=Depends(get_db)) -> str:
  # select * from users LIMIT 2
  stmt = select(UserModel).limit(2)
  users = db.execute(stmt).scalars().all()
  users_data = list(map(lambda u: u.to_dict(), users))
  # changer la réponse de base avec ici injection de templates jinja2
  return TEMPLATES.TemplateResponse(
    "index.html",
    {
      "request": request,
      "users": users_data
    }
)

@user_router.get("/search", status_code=200, response_model=UserSearchResults)
def search_users(*, 
      keyword: Optional[str]=Query(None, min_length=3, openapi_examples={
        "name_exemple": {
          "summary": "matt LAMAM",
          "value": "matt"
        }
      }),
      max_results: Optional[int]=10,
      db: Session=Depends(get_db)) -> dict:
  """
  utilisation de la querystring
  utilisation des méta types optional qui autorise la valeur None
  """
  # SELECT * FROM users Where username LIKE '%keyword%' LIMIT max_results
  stmt = select(UserModel)
  stmt = stmt if not keyword else stmt.where(UserModel.username.like(f"%{keyword}%"))
  stmt = stmt.limit(max_results)
  users = db.execute(stmt).scalars().all()
  users = list(map(lambda u: u.to_dict(), users)) if users else []
  return {"results": users}

@user_router.get("/{user_id}", status_code=200, response_model=User)
def fetch_user(*, user_id: int, db: Session=Depends(get_db)) -> dict:
  """
  ajout d'un paramètre d'url
  """
  user = db.execute(select(UserModel).where(UserModel.id == user_id)).scalar()
  if not user:
    raise HTTPException(
      status_code=status.HTTP_404_NOT_FOUND,
      detail="Utilisateur non trouvé"
    )
  return user.to_dict()

### call post pour créer un utilisateur ( pas de persitance )
### déterminer le schéma d'entrée et de sortie et le status code qui veut dire (OK: crée)
# TODO: ajouter l'authentification sur cette route
# @user_router.post("/create", status_code=201, response_model=User)
# def create_user(*, new_user: PostUser, auth_user: dict=Depends(verify_token)) -> dict:
#   new_id = max(USERS, key=lambda obj: obj["id"])['id'] + 1
#   user_in = User(
#     id=new_id,
#     name=new_user.name,
#     email=new_user.email,
#     gender=new_user.gender,
#     status=new_user.status
#   )
#   # en mémoire donc volatile
#   USERS.append(dict(user_in))
#   return user_in
