# %%
## RAPPEL: gestion dynamique des attributs des objets
class T:
  pass

t = T()

setattr(t, "param", "value")
# print(t.param)
hasattr(t, "param"), getattr(t, "param")

# %%
# rappels sur les dictionnaires

d = {"k1": 1, "k2": 2}
third_value = None
# if "k3" in d:
#   third_value = d["k3"]
# else:
#   third_value = 33
d.get("k3", 33)


# %%
# rappels sur les paramètres "variadics" *args **kwargs

def func (p1, *params):
  print(p1, params)

func(10)
func(10, "bonjour", "tout", "le monde")

def kw_func(p1, **opts):
  print(p1, opts)

kw_func(10)
kw_func(10, k1=2, k2="machin")
# %%

# utilisation des variadics à l'appel

def func(p1, p2, p3):
  print(p1, p2, p3)

params = {"p1": 1, "p3": 3, "p2": 2}

func(**params)

# %%
## signatures remarquables

def my_func(p1, /, p2, opt="dft1", *, opt2="dft2", **conf):
  print(p1, p2, opt, opt2)


my_func(1, 2)
# appel nommé impossible avec p1 car à gauche de /
# my_func(p2=2, p1=1)
my_func(1, opt="truc", p2=2)
my_func(1, 2, "truc")
# appel positionnel impossible avec opt2 à droite de *
# my_func(1, 2, "truc", "machin")
my_func(1, 2, "truc", opt2="machin")


# %%
## "polymorphisme naturel"


def troisfois(x: int) -> int:
  '''
  Docstring for troisfois
  
  :param x: Description
  :type x: int
  :return: Description
  :rtype: int
  '''
  if not isinstance(x, int):
    raise ValueError(f"{x} not int")
  return 3 * x

troisfois(3)
# troisfois("rien")
troisfois.__annotations__, troisfois.__doc__
# %%
## exemple de pool de thread python

from concurrent.futures import ThreadPoolExecutor as TPE
from multiprocessing import cpu_count
import requests

## pool de threads: pool de connexions => mutualisation de connexions
## un pool çà s'ouvre et çà se ferme

def worker(param):
  return requests.get("https://www.dawan.fr/formations/python/python-debutants/" + param).status_code

with TPE(cpu_count() - 2,) as pool:
  # faire des appels individuels asynchrone => pool.submit
  # exécuter une fonction sur une grappe d'appels, avec paramètres différents => pool.map
  # map est synchrone => tous les appels doivent être terminés pour avancer dans le programme
  for response in pool.map(worker, ["python-initiation", "python-approfondissement"]):
    print(response)
  # print(list(responses))
  
# %%
## rappel sur la programmation fonctionnelle

def my_map(func, lst: list) -> list:
  for i in range(len(lst)):
    lst[i] = func(lst[i])
  return lst

def square(x: int) -> int:
  return x**2

my_map(square, [1, 3, 5])

# avec le véritable map => cablé en C !! plus rapide qu'un for    
list(map(square, [1, 3, 5]))
# %%
## rappel sur les fonctions lambdas
list(map(lambda x: x**2, [1, 3, 5]))


# %%
## exemple tri complexe
import random

rows = [ f"row_{i}" for i in range(1, 21) ]
random.shuffle(rows)
sorted(rows, key=lambda r: int(r[4:]))

# %%
# notion de générateurs en python

# différence entre itérateur, fonction, générateur

lst = list(range(5))

# un itérateur est un objet qui implémente les 3 méthodes magiques: __init__, __iter__, __next__
# for i in lst: print(i)

def my_func(param):
  return param

# une fonction par défaut n'est pas itérable
# for p in my_func(1): print(p)

def my_gen(param):
  yield param
  yield param + 2

# générateur est un itérateur
# c'est une "fonction" qui exécute ses instruction
# avec certaines instruction yield qui vont retourne une valeur
# dans une boucle for ou dans la fonction next()
for p in my_gen(1): print(p)

# appeler une fonction génératrice retourne le générateur
gn = my_gen(5)

print(next(gn))
# après une itération, le générateur mémorise sont état
print(next(gn))

# %%
