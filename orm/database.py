"""
module de création du moteur de connexion sqlite3 et des sessions sqlite3
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

from pathlib import Path

DB_PATH = Path(__file__).parent / "persons.db"
# URI (sys. fichier /// ou réseau //) ou URL (réseau //)
DB_URI = f"sqlite:///{DB_PATH}"


engine = create_engine(
  DB_URI,
  # par défaut: on peut réutiliser le même thread pour une nouvelle cnx => pooling possible
  connect_args={"check_same_thread": False},
  # voir les requêtes SQL pour debug
  echo=True
)

# Fabrique de session particulière préconfiguré
# commit: synchroniser définitivement l'état des modèles de la session dans la bdd, dans le cadre une transaction
# flush: de mettre l'état des modèles de la session dans un cache mémoire qui peut être commit
# intérêt du flush: le cache est plus rapide mais volatile
SessionLocal = sessionmaker(autoflush=False, autocommit=False, bind=engine)
