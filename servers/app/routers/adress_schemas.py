from pydantic import BaseModel, Field

class Address(BaseModel):
  street: str=Field(max_length=255)
  zipcode: str=Field(max_length=20)
  city: str=Field(max_length=100)
