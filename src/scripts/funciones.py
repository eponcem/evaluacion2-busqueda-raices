import numpy as np

def f_polinomica(x): return np.power(x, 3) - x - 2.0

def df_polinomica(x): return 3.0 * np.square(x) - 1.0

def ddf_polinomica(x): return 6.0 * x

def g_polinomica(x):
    radicando = x + 2.0
    return np.cbrt(radicando)

def f_raiz_doble(x):
    diferencia = x - 2.0
    return np.square(diferencia)

def df_raiz_doble(x): return 2.0 * (x - 2.0)

def ddf_raiz_doble(x): return 2.0

def g_raiz_doble(x): return (x + 2.0) / 2.0

def f_logaritmica(x): return np.log(x) + x - 4.0

def df_logaritmica(x): return np.divide(1.0, x) + 1.0

def ddf_logaritmica(x): return -np.divide(1.0, np.square(x))

def g_logaritmica(x): return 4.0 - np.log(x)

def f_exponencial(x): return np.exp(-x) - x

def df_exponencial(x): return -np.exp(-x) - 1.0

def ddf_exponencial(x): return np.exp(-x)

def g_exponencial(x): return np.exp(-x)

def f_trigonometrica(x): return np.cos(x) - x

def df_trigonometrica(x): return -np.sin(x) - 1.0

def ddf_trigonometrica(x): return -np.cos(x)

def g_trigonometrica(x): return np.cos(x)