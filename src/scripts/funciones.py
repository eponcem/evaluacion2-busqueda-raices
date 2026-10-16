import numpy as np

def f_polinomica(x): return np.power(x, 3) - x - 2.0

def df_polinomica(x): return 3.0 * np.square(x) - 1.0

def ddf_polinomica(x): return 6.0 * x

def g_polinomica(x):
    radicando = x + 2.0
    return np.cbrt(radicando)