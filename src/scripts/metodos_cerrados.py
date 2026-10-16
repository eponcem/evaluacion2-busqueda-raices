import math
import numpy as np
from auxiliares import evaluar_funcion, es_numero_finito, validar_parametros, crear_resultado, terminar, registrar_paso, motivo_parada

def biseccion(f, a, b, tol=1e-6, max_iter=100, raiz_referencia=None):
    resultado = crear_resultado("Bisección")
    motivo = validar_parametros(tol, max_iter)
    if motivo is not None:
        return terminar(resultado, "entrada_invalida", motivo)
    if not es_numero_finito(a) or not es_numero_finito(b) or a >= b:
        return terminar(resultado, "entrada_invalida", "Los extremos deben ser finitos y satisfacer a < b.")
    a = float(a)
    b = float(b)
    fa = evaluar_funcion(f, a)
    fb = evaluar_funcion(f, b)
    if not es_numero_finito(fa) or not es_numero_finito(fb):
        return terminar(resultado, "error_numerico", "La evaluación no es finita o está fuera del dominio.")
    fa = float(fa)
    fb = float(fb)
    if fa == 0 or fb == 0:
        if fa == 0:
            x = a
            fx = fa
        else:
            x = b
            fx = fb
        registrar_paso(resultado, 0, x, fx, None, raiz_referencia)
        return terminar(resultado, "convergencia", "Se encontró una raíz exacta en un extremo del intervalo.")
    if np.signbit(fa) == np.signbit(fb):
        return terminar(resultado, "no_aplicable", "No hay cambio de signo entre los extremos del intervalo.")

    x_anterior = None
    for iteracion in range(1, max_iter + 1):
        x = a / 2.0 + b / 2.0
        paso = None
        if x_anterior is not None:
            paso = np.abs(x - x_anterior)
            if not math.isfinite(paso):
                return terminar(resultado, "error_numerico", "La diferencia entre las aproximaciones no es finita.")
        fx = evaluar_funcion(f, x)
        if not es_numero_finito(fx):
            return terminar(resultado, "error_numerico", "La evaluación no es finita o está fuera del dominio.")
        fx = float(fx)
        registrar_paso(resultado, iteracion, x, fx, paso, raiz_referencia)
        if np.abs(fx) < tol or (paso is not None and paso < tol):
            return terminar(resultado, "convergencia", motivo_parada(fx, tol))
        if np.signbit(fa) != np.signbit(fx):
            b = x
            fb = fx
        else:
            a = x
            fa = fx
        x_anterior = x
    return terminar(resultado, "maximo_iteraciones", "Se alcanzó el máximo de iteraciones sin cumplir el criterio de parada.")