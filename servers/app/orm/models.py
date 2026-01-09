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
# Declarative => une façon de structurer les modèle pour déterminer un état défini
# déclaratif (état / participe passé) != impératif (transition / infinitif)
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

# classes principales pour décrire des champs de données (colonnes)
from sqlalchemy import String, Enum, Integer, Float, Text, ForeignKey


class StatusEnum(enum.Enum):
  active = 1
  inactive = 0

class Base(DeclarativeBase):
  """classe de base pour tous les modèles (tables)"""
  # comportement générique embarqué dans tous les modèles héritant de cette classe
  display_fields = ()

  def to_dict(self) -> dict:
    return { f: getattr(self, f) for f in self.display_fields }

class User(Base):
  """
  Modèle User: pour authentification
  Relation: un User peut avoir un Person (One to One)
  """
  __tablename__ = "users"
  display_fields = ("id", "username")
  

  id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
  # String => VARCHAR (SQL) pour CHAR (SQL) utiliser CHAR (SQLAlchemy)
  username: Mapped[str] = mapped_column(String(50), unique=True, nullable=False, index=True)
  password: Mapped[str] = mapped_column(String(255), nullable=False)

  # relations: one to one => ici on travaille sur le python donc pas sur la base de données
  # uselist=False indique que c'est une relation one-to-one (pas une liste)
  # si user est supprimé je veux conserver la personne
  person: Mapped["Person"] = relationship(back_populates="user", cascade="save-update", uselist=False)
  
  # méthode magique qui rend l'objet convertible en chaine caractère 
  # => str(user) et donc print(user) car print utilise str
  def __str__(self):
    return f"User#{self.id}: {self.username}/****"
  
  # def to_dict(self) -> dict:
  #   return { f: getattr(self, f) for f in ("id", "username") }

class Person(Base):

  __tablename__ = "persons"
  display_fields = ("id", "name", "email", "gender", "status", "addresses")

  id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
  name: Mapped[str] = mapped_column(String(100), nullable=False)
  email: Mapped[str] = mapped_column(String(100), nullable=False, unique=True, index=True)
  gender: Mapped[str] = mapped_column(String(20), nullable=True)
  status: Mapped[int] = mapped_column(Enum(StatusEnum))
  # clé étrangère dans la base de données: 
  # unique=True garantit qu'un User ne peut avoir qu'une seule Person (one-to-one)
  # ondelete="SET NULL" si user est supprimé => user_id est mis à NULL
  user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="SET NULL"), nullable=True, unique=True)
  
  # relations
  # cascade="delete" : si Person est supprimée, User est aussi supprimé
  # Si le User est supprimé, la Person reste (grâce à ondelete="SET NULL")
  user: Mapped["User"] = relationship(back_populates="person", cascade="save-update, delete")
  # one to many
  # par défaut la relationship contient le paramètre lazy="select" 
  # => lazy loading => les données quand person.addresses est demandé
  # => lazy="joined" => eager loading :données immédiatement chargée avec une jointure SQL
  # => lazy="immediate" => idem mais avec 2 SELECT et un mapping
  # => lazy="selectin" => idem mais avec 2 SELECT imbriqués : SELECT * FROM xxxx join zzzz as [...] where yyyy in (SELECT * FROM zzzz) 
  addresses: Mapped[List["Address"]] = relationship(back_populates="person", cascade="save-update")


class Address(Base):

  __tablename__ = "addresses"

  id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
  street: Mapped[str] = mapped_column(String(255), nullable=False)
  zipcode: Mapped[str] = mapped_column(String(20), nullable=False)
  city: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
  person_id: Mapped[int] = mapped_column(ForeignKey("persons.id"))

  # relations
  person: Mapped["Person"] = relationship(back_populates="addresses", cascade="save-update")

