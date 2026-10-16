import numpy as np

def f_polinomica(x):
    return x**3 - x - 2.0

def df_polinomica(x):
    return 3.0 * x**2 - 1.0

def ddf_polinomica(x):
    return 6.0 * x

def g_polinomica(x):
    radicando = x + 2.0
    return np.cbrt(radicando)

def f_raiz_doble(x):
    diferencia = x - 2.0
    return diferencia**2

def df_raiz_doble(x):
    return 2.0 * (x - 2.0)

def ddf_raiz_doble(x):
    return 2.0

def g_raiz_doble(x):
    return (x + 2.0) / 2.0

def f_logaritmica(x):
    return np.log(x) + x - 4.0

def df_logaritmica(x):
    return (1.0 / x) + 1.0

def ddf_logaritmica(x):
    return -(1.0 / x**2)

def g_logaritmica(x):
    return 4.0 - np.log(x)

def f_exponencial(x):
    return np.exp(-x) - x

def df_exponencial(x):
    return -np.exp(-x) - 1.0

def ddf_exponencial(x):
    return np.exp(-x)

def g_exponencial(x):
    return np.exp(-x)

def f_trigonometrica(x):
    return np.cos(x) - x

def df_trigonometrica(x):
    return -np.sin(x) - 1.0

def ddf_trigonometrica(x):
    return -np.cos(x)

def g_trigonometrica(x):
    return np.cos(x)

def f_mixta(x):
    return np.sqrt(x) - np.cos(x)

def df_mixta(x):
    derivada_raiz = 1.0 / (2.0 * np.sqrt(x))
    return derivada_raiz + np.sin(x)

def ddf_mixta(x):
    return -(1.0 / (4.0 * x * np.sqrt(x))) + np.cos(x)

def g_mixta(x):
    correccion = 0.5 * f_mixta(x)
    return x - correccion

def obtener_funciones():
    funciones = [
        {"id": "polinomica", "nombre": "Polinómica", "formula": "x^3 - x - 2", "f": f_polinomica, "df": df_polinomica, "ddf": ddf_polinomica, "g": g_polinomica, "formula_g": "raíz cúbica de (x + 2)", "a": 1.0, "b": 2.0, "x0": 1.5, "secante_x0": 1.0, "secante_x1": 2.0, "doble": False},
        {"id": "raiz_doble", "nombre": "Raíz doble", "formula": "(x - 2)^2", "f": f_raiz_doble, "df": df_raiz_doble, "ddf": ddf_raiz_doble, "g": g_raiz_doble, "formula_g": "(x + 2) / 2", "a": 1.0, "b": 3.0, "x0": 1.2, "secante_x0": 1.2, "secante_x1": 1.3, "doble": True},
        {"id": "logaritmica", "nombre": "Logarítmica", "formula": "ln(x) + x - 4", "f": f_logaritmica, "df": df_logaritmica, "ddf": ddf_logaritmica, "g": g_logaritmica, "formula_g": "4 - ln(x)", "a": 2.0, "b": 3.0, "x0": 2.5, "secante_x0": 2.0, "secante_x1": 3.0, "doble": False},
        {"id": "exponencial", "nombre": "Exponencial", "formula": "exp(-x) - x", "f": f_exponencial, "df": df_exponencial, "ddf": ddf_exponencial, "g": g_exponencial, "formula_g": "exp(-x)", "a": 0.0, "b": 1.0, "x0": 0.5, "secante_x0": 0.0, "secante_x1": 1.0, "doble": False},
        {"id": "trigonometrica", "nombre": "Trigonométrica", "formula": "cos(x) - x", "f": f_trigonometrica, "df": df_trigonometrica, "ddf": ddf_trigonometrica, "g": g_trigonometrica, "formula_g": "cos(x)", "a": 0.0, "b": 1.0, "x0": 0.5, "secante_x0": 0.0, "secante_x1": 1.0, "doble": False},
        {"id": "mixta", "nombre": "Mixta", "formula": "sqrt(x) - cos(x)", "f": f_mixta, "df": df_mixta, "ddf": ddf_mixta, "g": g_mixta, "formula_g": "x - 0.5 * (sqrt(x) - cos(x))", "a": 0.1, "b": 1.0, "x0": 0.55, "secante_x0": 0.1, "secante_x1": 1.0, "doble": False},
    ]
    return funciones