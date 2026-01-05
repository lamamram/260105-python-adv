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