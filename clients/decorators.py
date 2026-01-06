from time import time

def timer(f):
  # *, ** => signature universelle
  def wrapper(*args, **opts):
    start = time()
    ret = f(*args, **opts)
    print(f"{time() - start:.2f} s")
    return ret
  return wrapper