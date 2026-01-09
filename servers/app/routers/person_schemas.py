from pydantic import BaseModel, Field
from typing import Sequence, Optional
from .adress_schemas import Address
from .user_schemas import RegisterUser

# schéma imbriqué de sortie
class Person(BaseModel):
  id: int
  name: str = Field(max_length=100)
  email: str
  gender: Optional[str] = None
  status: str
  addresses: Optional[Sequence[Address]]

# schéma imbriqué d'entrée
class PostPerson(BaseModel):
  user: RegisterUser
  name: str = Field(max_length=100)
  email: str
  gender: Optional[str] = None
  status: str
