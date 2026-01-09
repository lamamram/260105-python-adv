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

### scenarios de chargements de données en cas de relation ou jointure

1. relationship(... `lazy="select"`)
  + **Lazy loading** par défaut
  + a besoin d'une session
  + économise la mémoire Mais bcp de requêtes

```python
class Person(Base):
    __tablename__ = "persons"
    addresses: Mapped[List["Address"]] = relationship(
        back_populates="person",
        lazy="select"  # Par défaut
    )

# Charger une personne
person = db.execute(select(Person).where(Person.id == 1)).scalar()
# SQL: SELECT * FROM persons WHERE id = 1

# Premier accès à person.addresses => déclenche une nouvelle requête
addresses = person.addresses
# SQL: SELECT * FROM addresses WHERE person_id = 1
```

2. `lazy="joined"`
  + **Eager Loading**
  + sans session
  + une seule requête Mais bcp de données (voire inutiles)
  + possibles jointures complexes => lent

```python
# Charger une personne
person = db.execute(select(Person).where(Person.id == 1)).scalar()
# Les addresses sont DÉJÀ chargées en une seule requête
addresses = person.addresses  # Pas de requête SQL supplémentaire

# UNE SEULE requête avec LEFT OUTER JOIN
# SELECT persons.*, addresses.*
# FROM persons 
# LEFT OUTER JOIN addresses ON persons.id = addresses.person_id
# WHERE persons.id = 1;
```

3. `lazy="selectin"`
  + **Eager Loading** avec l'operateur **IN SQL**
  + et plus performant pour charger plusieurs objets
  + plus simple que Join
  + uniquement 2 requêtes pour une collection de données

```python
# Charger plusieurs personnes
persons = db.execute(select(Person).limit(3)).scalars().all()
# Les addresses sont chargées avec un SELECT IN

# -- Requête 1: Charger les personnes
# SELECT * FROM persons LIMIT 3;
# -- Résultat: persons avec id = 1, 2, 3

# -- Requête 2: Charger TOUTES les adresses en une fois
# SELECT * FROM addresses 
# WHERE addresses.person_id IN (1, 2, 3);
```

4. `lazy="immediate"`
  + **Eager Loading** avec deux requêtes pour chaque élément
  + plus simple que join Mais trop de requêtes pour une collection

```python
# Charger une personne (pas pour plusieurs !!!)
person = db.execute(select(Person).where(Person.id == 1)).scalar()
# Les addresses sont automatiquement chargées

# -- Requête 1: Charger la personne
# SELECT * FROM persons WHERE id = 1;

# -- Requête 2: Charger ses adresses (automatiquement, immédiatement après)
# SELECT * FROM addresses WHERE person_id = 1;
```

<ins>5. Recommandations</ins>

|Situation|lazy recommandé|Raison|
|---------|---------------|------|
|Relations rarement utilisées|select|Économise ressources|
|Toujours besoin des relations|joined|Une seule requête|
|Charger liste d'objets|selectin|Évite N+1, performant|
|Petites collections simples|joined|Simple et efficace|
|Relations complexes/volumineuses|select + explicite|Contrôle manuel|

<ins>6. jointures explicites - contrôle manuel</ins>

```python
from sqlalchemy.orm import joinedload, selectinload

# Forcer joined pour cette requête uniquement
persons = db.execute(
    select(Person)
    .options(joinedload(Person.addresses))
    .limit(3)
).scalars().all()

# Ou avec selectin
persons = db.execute(
    select(Person)
    .options(selectinload(Person.addresses))
    .limit(3)
).scalars().all()
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

