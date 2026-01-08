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

USERS = [
    {
        "id": 8115171,
        "name": "Damodara Naik DO",
        "email": "damodara_naik_do@schaden.example",
        "gender": "male",
        "status": "inactive"
    },
    {
        "id": 8115170,
        "name": "Anandamayi Achari",
        "email": "achari_anandamayi@stracke-rowe.test",
        "gender": "female",
        "status": "active"
    },
    {
        "id": 8115169,
        "name": "Sanka Namboothiri MD",
        "email": "namboothiri_sanka_md@grady-graham.test",
        "gender": "female",
        "status": "active"
    },
    {
        "id": 8115168,
        "name": "Prof. Bilwa Chopra",
        "email": "prof_chopra_bilwa@greenfelder.example",
        "gender": "female",
        "status": "active"
    },
    {
        "id": 8115163,
        "name": "Mr. Deevakar Guneta",
        "email": "deevakar_guneta_mr@jaskolski.example",
        "gender": "female",
        "status": "active"
    },
    {
        "id": 8115161,
        "name": "Amrita Kapoor",
        "email": "kapoor_amrita@roob.test",
        "gender": "female",
        "status": "active"
    },
    {
        "id": 8115160,
        "name": "Tushar Deshpande",
        "email": "tushar_deshpande@braun-schuster.example",
        "gender": "male",
        "status": "inactive"
    },
    {
        "id": 8115159,
        "name": "Vishnu Saini",
        "email": "vishnu_saini@hansen.test",
        "gender": "female",
        "status": "active"
    },
    {
        "id": 8115158,
        "name": "Ekadant Khatri",
        "email": "ekadant_khatri@hagenes.test",
        "gender": "female",
        "status": "active"
    },
    {
        "id": 8115155,
        "name": "Mr. Mangala Achari",
        "email": "mr_mangala_achari@stracke.test",
        "gender": "female",
        "status": "active"
    }
]

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
      max_results: Optional[int]=10) -> dict:
  """
  utilisation de la querystring
  utilisation des méta types optional qui autorise la valeur None
  """
  if not keyword:
    return {"results": USERS[:max_results]}
  results = filter(lambda user: keyword.lower() in user["name"].lower(), USERS)
  return {"results": list(results)[:max_results]}

@user_router.get("/{user_id}", status_code=200, response_model=User)
def fetch_user(*, user_id: int) -> dict:
  """
  ajout d'un paramètre d'url
  """
  result = [user for user in USERS if user["id"] == user_id]
  if not result:
    raise HTTPException(
      status_code=status.HTTP_404_NOT_FOUND,
      detail="Utilisateur non trouvé"
    )
  return result[0]

### call post pour créer un utilisateur ( pas de persitance )
### déterminer le schéma d'entrée et de sortie et le status code qui veut dire (OK: crée)
# TODO: ajouter l'authentification sur cette route
@user_router.post("/create", status_code=201, response_model=User)
def create_user(*, new_user: PostUser, auth_user: dict=Depends(verify_token)) -> dict:
  new_id = max(USERS, key=lambda obj: obj["id"])['id'] + 1
  user_in = User(
    id=new_id,
    name=new_user.name,
    email=new_user.email,
    gender=new_user.gender,
    status=new_user.status
  )
  # en mémoire donc volatile
  USERS.append(dict(user_in))
  return user_in
