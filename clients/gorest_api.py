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


