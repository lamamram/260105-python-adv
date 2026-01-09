from pydantic import BaseModel, Field

from typing import Sequence, Optional

class User(BaseModel):
  id: int
  username: str

class UserSearchResults(BaseModel):
  results: Sequence[User]

class RegisterUser(BaseModel):
  username: str = Field(max_length=100)
  password: str = Field(max_length=100)