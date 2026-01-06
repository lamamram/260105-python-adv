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
  responses = pool.map(worker, ["python-initiation", "python-approfondissement"])
  print(list(responses))
# %%
