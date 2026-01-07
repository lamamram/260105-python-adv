"""
Gestion de l'authentification OAuth2 avec JWT
"""

# pip install jose
from jose import jwt, JWTError
from datetime import datetime, timedelta, timezone
from typing import Optional
from dotenv import load_dotenv
from pathlib import Path
import os
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from fastapi import Depends, HTTPException, status

# fixer l'emplacement du fichier .env et portable avec Path (unix/windows)
env_path = Path(__file__).parent / ".env"
load_dotenv(dotenv_path=env_path)

SECRET_KEY=os.environ["SECRET_KEY"]
ACCESS_TOKEN_EXPIRE_MINUTE=os.environ["ACCESS_TOKEN_EXPIRE_MINUTE"] or 30
ALGORITHM=os.environ["ALGORITHM"]

if not SECRET_KEY: raise ValueError("SECRET_KEY inexistante !!!!")
ACCESS_TOKEN_EXPIRE_MINUTE = int(ACCESS_TOKEN_EXPIRE_MINUTE)

# schéma de sécurité: => capable de récolter le jeton JWT à partir de l'entête HTTP
# Authorization: Bearer <token>
security = HTTPBearer()


def create_access_token(payload: dict, expires_delta: Optional[timedelta]) -> str:
  # copie pour agrémenter le jeton
  to_encode = payload.copy()
  # vous ne savez pas où se trouve le client d'ou utc !!!
  expires = datetime.now(timezone.utc)
  expires += expires_delta if expires_delta else timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTE) 
  # fusion de dictionnaires
  ## le champs exp est le terme attendu dans le jeton JWT
  to_encode.update({"exp": expires})

  return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def verify_token(credentials: HTTPAuthorizationCredentials=Depends(security)) -> dict:
  """
  :crendentials de type HTTPAuthorizationCredentials de FastAPI généré 
  par la classe HTTPBearer de gestion de jeton JWT dans FastAPI 
  """
  token = credentials.credentials

  credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Token invalide ou expiré",
    headers={"WWW-authenticate": "Bearer"}
  )

  try:
    payload = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)
    user_id: str = payload.get("sub") # la valeur ou None

    if user_id is None: raise credentials_exception

    # retourne les infos d'utilisateur authentifié
    return {
      "user_id": user_id,
      "username": payload.get("username"),
      "email": payload.get("email")
    }
  except JWTError:
    raise credentials_exception
