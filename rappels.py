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
