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
from ..orm.models import Person as PersonModel, StatusEnum, User as UserModel

# type de donées avec un objet de type donné OU None
from typing import Optional
from .person_schemas import *
from pathlib import Path
from ..auth import verify_token

person_router = APIRouter(prefix="/persons")

@person_router.get("/{person_id}", status_code=200, response_model=Person)
def fetch_person(*, person_id: int, db: Session=Depends(get_db)) -> dict:
  """
  ajout d'un paramètre d'url
  """
  person = db.execute(select(PersonModel).where(PersonModel.id == person_id)).scalar()
  if not person:
    raise HTTPException(
      status_code=status.HTTP_404_NOT_FOUND,
      detail="Personne non trouvée"
    )
  # to_dict demande les relations "addresses" donc le modèle va chercher les entrées d'Address à la volée (Lazy Load)
  person = person.to_dict()
  person["status"] = StatusEnum(person["status"]).name
  return person

### call post pour créer une personne
### déterminer le schéma d'entrée et de sortie et le status code qui veut dire (OK: crée)
@person_router.post("/register", status_code=201, response_model=Person)
def create_person(
  *, 
  new_person: PostPerson,
  db: Session=Depends(get_db)
) -> dict:
  # pour créer une personne on a besoin d'un utilisateur
  user_in = UserModel(
    username=new_person.user.username,
    password=new_person.user.password
  )
  db.add(user_in)
  db.flush()
  # rajoute le nouveau id d'uitlisateur
  db.refresh(user_in)
  # new_id = max(USERS, key=lambda obj: obj["id"])['id'] + 1
  person_in = PersonModel(
    name=new_person.name,
    email=new_person.email,
    gender=new_person.gender,
    status=getattr(StatusEnum, new_person.status),
    user=user_in
  )
  db.add(person_in)
  db.commit()
  # ajoute le nouveau id de personne
  db.refresh(person_in)
  return person_in
