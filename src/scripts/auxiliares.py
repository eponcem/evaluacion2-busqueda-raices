import math
import numpy as np

def evaluar_funcion(funcion, x):
    with np.errstate(all="ignore"):
        return funcion(np.float64(x))

def es_numero_finito(valor):
    if not isinstance(valor, (int, float, np.integer, np.floating)):
        return False
    limite = float(np.finfo(float).max)
    if valor < -limite or valor > limite:
        return False
    return math.isfinite(valor)

def validar_parametros(tol, max_iter):
    if not es_numero_finito(tol) or tol <= 0:
        return "La tolerancia debe ser positiva y finita."
    if isinstance(max_iter, bool) or not isinstance(max_iter, (int, np.integer)) or max_iter <= 0:
        return "El máximo de iteraciones debe ser un entero positivo."
    return None

def crear_resultado(metodo):
    return {"metodo": metodo, "raiz": None, "iteraciones": 0, "convergio": False, "estado": "entrada_invalida", "motivo": "", "historial": []}

def terminar(resultado, estado, motivo):
    resultado["estado"] = estado
    resultado["motivo"] = motivo
    resultado["convergio"] = estado == "convergencia"
    return resultado