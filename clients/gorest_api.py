"""
client for interacting with the GoRest API => gorest.co.in
utilisant la bibliothèque requests
en POO

objectifs cas d'usage:
----------

1/ une requête GET pour récupérer une page d'utilisateurs paramétrable (nombre de résultats, page)
2/ utiliser la méthode précédente pour récupérer tous les utilisateurs (itérateur)
3/ améliorer la méthide précédente pour accélérer la récupération avec du multithreading
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
