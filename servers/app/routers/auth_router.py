from fastapi import APIRouter, Query, HTTPException, status

from typing import Optional
from .auth_schemas import *
from ..auth import ACCESS_TOKEN_EXPIRE_MINUTE, create_access_token
from datetime import timedelta

auth_router = APIRouter(prefix="/auth")

FAKE_USERS_DB = {
    "admin": {
        "user_id": "1",
        "username": "admin",
        "email": "admin@example.com",
        "password": "secret123"  # En production, utiliser un hash bcrypt !
    },
    "user": {
        "user_id": "2",
        "username": "user",
        "email": "user@example.com",
        "password": "password456"
    }
}


@auth_router.post("/login", status_code=200, response_model=TokenResponse)
def login(*, credentials: LoginRequest) -> dict:
  # vérifier que le username existe
  user = FAKE_USERS_DB.get(credentials.username)
  if not user or user["password"] != credentials.password:
    raise HTTPException(
      status_code=status.HTTP_401_UNAUTHORIZED,
      detail="Identifiants incorrects",
      # pour Oauth2
      headers={"WWW-authenticate": "Bearer"}
    )
  
  # on peut ajouter les permissions dans le payload à partir de la BDD
  token = create_access_token({
      "sub": user["user_id"],
      "username": user["username"],
      "email": user["email"]
    }, 
    expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTE)
  )
  
  ## les paramètres et valeur de ce dictionnaire sont liés à la classe Bearer de fastAPI
  return {
    "access_token": token,
    "token_type": "bearer",
    ## en secondes
    "expires_in": ACCESS_TOKEN_EXPIRE_MINUTE * 60
  }



