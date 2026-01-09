# APIs et ORMs

## intro: architecture

<ins>1. service</ins>

* un objet qui délivre une valeur pour un client
  + dont il ne connaît que l'interface / signature publique
  + et dont il est dégagé des problématiques de maintenabilité et évolutivité

* inforatique: une unité d'exécution isolé du reste d'un système
   + via bare-metal / VM / conteneur
   + communique sur le réseau


<ins>2. interface (POO)</ins>

* ensemble de définitions / signatures publiques abstraites
  + nom / paramètres / types de retours
  + à implémenter dans les classes / types de données
  + pour standardiser une activité

* dans les langages de programmation on a comme interfaces les
  + interfaces au sens Java / Php (implements)
  + classes abstraites
  + contrats d'API (REST / SOAP / GRAPHQL / gRPC)

<ins>3. Injection de dépendances</ins>

> dans un couple utilisateur / dépendance,
> un utilisateur ne doit connaître que l'interface publique de sa dépendace
> en particulier ne connaît pas le moyen de créer sa dépendance

<ins>4. Principe d'Inversion de dépendances</ins>

> dans un couple utilisateur / dépendance,
> un utilisateur ne devrait utiliser que des abstractions (interfaces/classes abstraites...)
> et les dépendances implémentent ces abstractions

<ins>5. architecture hexagonale</ins>

* dans une architecture distribuée en couche
  + la logique serveur (code métier / backend)
  + devrait être indépendante des autres couches (présentation / données / fournisseurs d'APIs)

* cette indépendance est réalisée par un ensemble d'outils présentant une Inversion de dépendance
  + client d'api
  + ORMs: Object Relational Mapper


<ins>6. archi µservices classiques</ins>

![alt text](µservices.png)

## authentification Oauth2 avec un jeton JWT: Json Web Token


### principe du jeton JWT

![alt text](jwt.png)

### stratégie

1. création du jeton `auth.create_access_token`
2. création du router `auth_router`
  + ajouter la route `/login`
3. vérification du jeton: `auth.verify_token`
  + un test du token avec la route `/me`


## faire persister les données avec une bdd sqlite3 et l'ORM SQLAlchemy

### Object Relational Mapper

* outil de manipulation de la couche de donnée relationnelle à partir d'interfaces dédiée
* l'ORM doit réaliser une **inversion de dépendance**

```
|                        indépendant                        |            remplaçables          
|------------------------Logique Serveur -------------------|-------DAO----------|---DATA-----
 FASTAPI -> Route -> Interface (classe abstraite) ASSEZ FIXE -> ORM(SQLAlchemy) -> DB(sqlite3)
```

### capacités d'un ORM: SqlAlchemy 2+



1. décrire un modèle de données avec leurs relations
2. en déduire une base de donnée Relationnelle selon une configuration (sqlite3)
3. exécuter/mettre en cache les lectures/écritures vers/depuis la bdd
4. organiser les migrations de données en utilisant le composant **alembic**


### gestion des couches de données

```python

# un objet python: n'existe pas en cache ni en bdd
user = User(username="admin", password="secret123")

# çà nous créé la requête d'insertion mais l'enregistrement n'est pas mis en cache ni en bdd
db.add(user)

# mise en cache => d'autres requêtes peuvent lire la table à partir du cache, dans la session courante
db.flush()

# mise en bdd => for REAL
db.commit()

user.username = "Admin"
db.refresh(user) # "admin" => on restaure l'état du cache après le dernier flush

# parallèlement, on pourrait enlever explicitement les modifications non flushées
db.expire(user) # "admin" aussi

```

## migrations de données avec Alembic

### stratégie

1. install: `pip install alembic`
2. initialiser: `alembic init alembic` **alembic/** et **alembic.ini** dans orm/
3. charger les modèles dans **alembic/env.py**: 
  + `from model import Base`
  + `target_metadata = Base.metadata`
  + dans `context.configure`: `render_as_batch: True` => SQLITE
4. déterminer le delta entre python <=> bdd: génère migration dans **alembic/versions/**
  + `alembic revision --autogenerate -m "preciser les modifs"`
5. exécuter la migration: `alembic upgrade head`

### autre types de migrations

```bash
# Aller à une version spécifique (ID de révision)
alembic upgrade 11a65d7cf638

# Avancer d'un certain nombre de migrations (+1, +2, etc.)
alembic upgrade +1

# Revenir en arrière d'une migration
alembic downgrade -1

# Revenir à une version spécifique
alembic downgrade 11a65d7cf638

# Revenir au début (supprimer toutes les migrations)
alembic downgrade base

# Voir la version actuelle
alembic current

# Voir l'historique des migrations
alembic history
```

