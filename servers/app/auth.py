"""
Gestion de l'authentification OAuth2 avec JWT
"""

# pip install jose
from jose import jwt
from datetime import datetime, timedelta, timezone
from typing import Optional
from dotenv import load_dotenv
from pathlib import Path
import os

# fixer l'emplacement du fichier .env et portable avec Path (unix/windows)
env_path = Path(__file__).parent / ".env"
load_dotenv(dotenv_path=env_path)

SECRET_KEY=os.environ["SECRET_KEY"]
ACCESS_TOKEN_EXPIRE_MINUTE=os.environ["ACCESS_TOKEN_EXPIRE_MINUTE"] or 30
ALGORITHM=os.environ["ALGORITHM"]

if not SECRET_KEY: raise ValueError("SECRET_KEY inexistante !!!!")
ACCESS_TOKEN_EXPIRE_MINUTE = int(ACCESS_TOKEN_EXPIRE_MINUTE)

def create_access_token(payload: dict, expires_delta: Optional[timedelta]) -> str:
  # copie pour agrémenter le jeton
  to_encode = payload.copy()
  # vous ne savez pas où se trouve le client d'ou utc !!!
  expires = datetime.now(timezone.utc)
  expires += expires_delta if expires_delta else timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTE) 
  # fusion de dictionnaires
  to_encode.update({"exp": expires})

  return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def verify_token():
  pass