import math
import numpy as np

def evaluar_funcion(funcion, x):
    with np.errstate(all="ignore"):
        return funcion(np.float64(x))

def es_numero_finito(valor):
    return math.isfinite(valor)


def validar_parametros(tol, max_iter):
    if not es_numero_finito(tol) or tol <= 0:
        return "La tolerancia debe ser positiva y finita."
    if max_iter <= 0:
        return "El máximo de iteraciones debe ser positivo."
    return None


def crear_resultado(metodo):
    return {"metodo": metodo, "raiz": None, "iteraciones": 0, "convergio": False, "estado": "entrada_invalida", "motivo": "", "historial": []}

def terminar(resultado, estado, motivo):
    resultado["estado"] = estado
    resultado["motivo"] = motivo
    resultado["convergio"] = estado == "convergencia"
    return resultado

def registrar_paso(resultado, iteracion, x, fx, paso, raiz_referencia):
    error_absoluto = None
    if raiz_referencia is not None and es_numero_finito(raiz_referencia):
        error_absoluto = np.abs(x - float(raiz_referencia))
        if not math.isfinite(error_absoluto):
            error_absoluto = None
    resultado["historial"].append({"iteracion": iteracion, "x": x, "fx": fx, "residuo": np.abs(fx), "paso": paso, "error_absoluto": error_absoluto})
    resultado["raiz"] = x
    resultado["iteraciones"] = iteracion

def motivo_parada(fx, tol):
    if fx == 0:
        return "Se encontró una raíz exacta en la aritmética utilizada."
    if np.abs(fx) < tol:
        return "El residuo es menor que la tolerancia."
    return "El paso es menor que la tolerancia; el residuo aún no cumple la tolerancia."