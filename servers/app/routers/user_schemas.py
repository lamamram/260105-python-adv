from pydantic import BaseModel

from typing import Sequence

class User(BaseModel):
  id: int
  name: str
  email: str
  gender: str
  status: str

class UserSearchResults(BaseModel):
  results: Sequence[User]