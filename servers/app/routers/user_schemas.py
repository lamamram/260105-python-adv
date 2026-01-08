from pydantic import BaseModel, Field

from typing import Sequence, Optional

class User(BaseModel):
  id: int
  username: str

class UserSearchResults(BaseModel):
  results: Sequence[User]