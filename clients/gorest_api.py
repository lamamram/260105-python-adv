"""
client for interacting with the GoRest API => gorest.co.in
utilisant la bibliothèque requests
en POO

objectifs cas d'usage:
----------

1/ une requête GET pour récupérer une page d'utilisateurs paramétrable (nombre de résultats, page)
2/ utiliser la méthode précédente pour récupérer tous les utilisateurs (itérateur)
3/ améliorer la méthode précédente pour accélérer la récupération avec du multithreading
4/ une requête POST pour créer un utilisateur avec authentification de type bearer token

objectifs techniques:
----------
- gestion des erreurs HTTP
- gestion des exceptions réseau
- documentation des méthodes
- séparation entre 
  méthodes publiques qui réalise le cas d'usage
  méthode privée centrale qui manipule requests (gestion du verbe HTTP, des headers, des paramètres, du corps de la requête, etc.)
Bonus: travailler avec une session requests pour optimiser les appels répétés au cas où
"""

# %%
## utilisation de requests sans POO
## cherche une page d'utilisateurs par nombre de résultats et numéro de page
## sans POO
## gestion des erreurs HTTP et des exceptions réseau et status code et header Content-Type et gestion du JSON

import requests
from requests.exceptions import ConnectionError, HTTPError, Timeout, RequestException

nb_results = 10
page_number = 2

try:
  response = requests.get(
    "https://gorest.co.in/public/v2/users", 
    params={"page": page_number, "per_page": nb_results}
  )
  if 200 <= response.status_code < 300:
    # gestion de la forme des données reçues
    if "Content-Type" in response.headers and "application/json" in response.headers["Content-Type"]:
      data = response.json()
      print(data)
  # gestion des codes HTTP d'erreur
  else:
    # raise HTTPError(f"erreur HTTP: {response.status_code}")
    response.raise_for_status()
## gérer plusieurs exceptions réseau avec le même bloc except
except (ConnectionError, RequestException) as e:
  print("erreur réseau:", e)


# %%
## utilisation de requests avec POO
# 1/ créer une classe GoRestClient
# 2/ gérer les paramètres d'instanciation du client dans le __init__
# 3/ créer une méthode publique get_users_page pour insérer les paramétres et retourner la réponse
# 4/ créer une méthode privée __call qui manipule requests
import requests, os
from requests.exceptions import ConnectionError, HTTPError, Timeout, RequestException
from concurrent.futures import ThreadPoolExecutor as TPE
from multiprocessing import cpu_count

from typing import List, Dict

from abc import ABC, abstractmethod
# pip install python_dotenv
from dotenv import load_dotenv

# charge les variables du .env local en tant que variables d'environnment temporaires
load_dotenv()

TOKEN = os.environ["GO_REST_TOKEN"]

# classe abstraite qui fait office d'interface sur le sujet API user
class UserAPIClient(ABC):
  @abstractmethod
  def get_users_page(self, page: int) -> List[Dict] | Dict: pass
  @abstractmethod
  def get_all_users(self, limit=10) -> dict: pass
  @abstractmethod
  def get_all_users_multi(self) -> dict: pass
  @abstractmethod
  def create_user(self, user_data: dict) -> dict: pass
class GoRestClient(UserAPIClient):
  def __init__(self, version: str= "v2", **conf):
    self.__base = "https://gorest.co.in/public/"
    self.__version = version
    self.__per_page = conf.get("per_page", 10)
    self.__token = TOKEN
  
  def get_users_page(self, page: int) -> List[Dict] | Dict:
    return self.__call(
      "users", 
      "GET", 
      params={"page": page, "per_page": self.__per_page}
    )
  
  def get_all_users(self, limit=10) -> dict:
    data, errors, page = [], [], 1
    while True:
      r = self.get_users_page(page)
      if not r or page > limit:
        return {"data": data, "errors": errors}
      if isinstance(r, dict):
        errors.append(r)
      else:
        data += r
      page += 1
  
  def get_all_users_multi(self) -> dict:
    """
    ajouter la classe ThreadPoolExecutor pour accélérer le téléchargement
    des objets utilisateurs par batch de pages
    """
    data, errors, i = [], [], 0
    nb_cpus = cpu_count() - 2
    with TPE(nb_cpus) as pool:
      while True:
        print(f"fetch pages {nb_cpus*i + 1} to {nb_cpus*(i+1) + 1} !")
        for r in pool.map(self.get_users_page, list(range(nb_cpus*i + 1, nb_cpus*(i+1) + 1))):
          # map liste les appels DANS l'ORDRE
          if not r:
            return {"data": data, "errors": errors}
          if isinstance(r, dict):
            errors.append(r)
          else:
            data += r
        i += 1
    
  def create_user(self, user_data: dict) -> dict:
    return self.__call("users", "POST", data=user_data)

  def __call(self, endpoint: str, method: str, 
             params: Dict= {}, 
             data: Dict={}, 
             headers: Dict={},
             files={}) -> List[Dict] | Dict:
    """
    exécuter toutes les requêtes http du client
    """
    try:
      if method.lower() in ("post", "put", "patch", "delete"):
        headers["Authorization"] = f"Bearer {self.__token}"
      call_fn = getattr(requests, method.lower())
      response = call_fn(
        f"{self.__base}/{self.__version}/{endpoint}",
        params=params,
        data=data,
        headers=headers,
        files=files
      )
      if 200 <= response.status_code < 300:
        if "Content-Type" in response.headers and "application/json" in response.headers["Content-Type"]:
          return response.json()
      else:
        response.raise_for_status()
    except (ConnectionError, RequestException) as e:
      return {type(e): str(e)}

# %%
# programme principal
from decorators import timer

@timer
def main(client: UserAPIClient):
  # client.get_users_page(2)
  # client.get_all_users()
  # print(list(map(len, client.get_all_users_multi().values())))
  print(client.create_user({
    "name": "matt LAMAM",
    "email": "bob@example.com",
    "gender": "male",
    "status": "active"
  }))
  

if __name__ == "__main__":
  # configuration du bon client (ajouter une factory)
  client = GoRestClient(per_page=20)
  main(client)
# %%
