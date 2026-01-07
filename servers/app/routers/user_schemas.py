from pydantic import BaseModel, Field

from typing import Sequence, Optional

class User(BaseModel):
  id: int
  name: str
  email: str
  gender: Optional[str] = None
  status: str

class PostUser(BaseModel):
  name: str = Field(max_length=100)
  email: str
  # rendre un champs non required: Optional + valeur défaut
  gender: Optional[str] = Field(default=None)
  status: str

class UserSearchResults(BaseModel):
  results: Sequence[User]