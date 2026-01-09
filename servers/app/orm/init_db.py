"""
initialisation de la bdd et de ses tables à partir du moteur / session et les modèles
"""

from models import Base, User, Person, Address, StatusEnum
from database import engine, SessionLocal
# func => tous les aggrégats (count, average, max, ...)
from sqlalchemy import select, func

def init_database():
  print("Création des tables...")
  # Créer les tables liées aux modèles héritant de Base
  # CREATE TABLE IF NOT EXISTS
  Base.metadata.create_all(bind=engine)

  # tests
  # par défaut, l''objet session créé une transaction (BEGIN en SQL)
  # donc les jeux d'écritures (INSERT, UPDATE, DELETE) ne sont directement écrits en bdd
  # pas avant qu'on exécute explicitement un db.commit()
  db = SessionLocal()

  try:
    # vérifier si les données existent déjà
    # SELECT count(1) from users; # != 0 ?
    user_count = select(func.count()).select_from(User)
    # par défaut execute retourne des objets "Rows" => tuples donc pas de nom de champs
    # si on veut clé / valeur pour les résultats alors on utilise les méthodes .scalar() ou scalars()
    # scalars() retourne une liste d'objets de résultats qu'on peut convertir en dict
    # scalar() retourne un objet de résultat (le premier) ou le scalaire s'il ya une colonne !!
    if db.execute(statement=user_count).scalar() > 0:
      print("base de données déjà alimentée !")
      return
    
    print("Insertion des utilisateurs...")
    users = [
      User(username="admin", password="secret123"),
      User(username="user", password="password456")
    ]

    # INSERT INTO users (username, password) Values ('', ''), ...
    db.add_all(users)

    print("Insertion des personnes...")
    persons = [
      # REM: on aurait pu utiliser user_id=users[0].id à la place de user=users[0] mais les objets sont "lazy_loaded" 
      Person(name="matt LAMAM", email="matt@example.com", gender="male", status=StatusEnum.active, user=users[0]),
      Person(name="gars", email="gars@example.com", gender="male", status=StatusEnum.inactive, user=users[1])
    ]

    # INSERT INTO persons (...) Values ('', '', ...), ...
    db.add_all(persons)

    print("Insertion des adresses...")
    addresses = [
      Address(street="3 rue des trembles", zipcode="44600", city="St Nazaire", person=persons[0]),
      Address(street="22 avenue de la rep", zipcode="13002", city="Marseille", person=persons[1]),
    ]

    # INSERT INTO persons (...) Values ('', '', ...), ...
    db.add_all(addresses)
    # j'ai mets en cache toutes les insertions ...
    db.flush()

    # pour que les derniers selects utilisent le nouvelles données
    print("Bdd initialisée correctement !")
    user_count = db.execute(select(func.count()).select_from(User)).scalar()
    person_count = db.execute(select(func.count()).select_from(Person)).scalar()
    address_count = db.execute(select(func.count()).select_from(Address)).scalar()
    print(f"   - {user_count} utilisateurs créés")
    print(f"   - {person_count} personnes créées")
    print(f"   - {address_count} adresses créées")
    
    # si toutes les insertions sont OK alors on va en bdd
    db.commit()
    
  # Exception capture tout !!
  except Exception as e:
    print(e)
    # on supprime les données de transaction (unflush)
    db.rollback()
  finally:
    # si try ok, si exception capturée, si aussi avant plantage !!!
    db.close()

if __name__ == "__main__":
  init_database()

