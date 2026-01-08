"""
modèles de données avec SQLAlchemy 2+
Approche déclarative => représente un état
"""



# pip install SQLAlchemy
# pip install bcrypt
import enum
import bcrypt

from typing import List

# classes principales pour générer un modèle de données
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

# classes principales pour décrire des champs de données (colonnes)
from sqlalchemy import String, Enum, Integer, Float, Text, ForeignKey, ForeignKeyConstraint


class StatusEnum(enum.Enum):
  active = 1
  inactive = 0

class Base(DeclarativeBase):
  """classe de base pour tous les modèles (tables)"""
  pass

class User(Base):
  """
  Modèle User: pour authentification
  Relation: un User peut avoir un Person (One to One)
  """
  __tablename__ = "users"

  id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
  # String => VARCHAR (SQL) pour CHAR (SQL) utiliser CHAR (SQLAlchemy)
  username: Mapped[str] = mapped_column(String(50), unique=True, nullable=False, index=True)
  password: Mapped[str] = mapped_column(String(255), nullable=False)

  # relations: one to one => ici on travaille sur le python donc pas sur la base de données
  # si user est supprimé je veux conserver la personne
  person: Mapped["Person"] = relationship(back_populates="user", cascade="save-update")


class Person(Base):

  __tablename__ = "persons"

  id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
  name: Mapped[str] = mapped_column(String(100), nullable=False)
  email: Mapped[str] = mapped_column(String(100), nullable=False, unique=True, index=True)
  gender: Mapped[str] = mapped_column(String(20), nullable=True)
  status: Mapped[int] = mapped_column(Enum(StatusEnum))
  # clé étrangère dans la base de données: 
  # ondelete="SET NULL" si person est supprimé => user_id est mis à NULL
  user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
  
  # relations
  # cascade delete, delete-orphan: si une personne est supprimée on suprime le user
  user: Mapped["User"] = relationship(back_populates="person", cascade="delete, delete-orphan")
  # one to many
  addresses: Mapped[List["Address"]] = relationship(back_populates="person", cascade="save-update")


class Address(Base):

  __tablename__ = "addresses"

  id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
  street: Mapped[str] = mapped_column(String(255), nullable=False)
  zipcode: Mapped[str] = mapped_column(String(20), nullable=False)
  city: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
  user_id: Mapped[int] = mapped_column(ForeignKey("persons.id"))

  # relations
  person: Mapped["Person"] = relationship(back_populates="addresses", cascade="save-update")

