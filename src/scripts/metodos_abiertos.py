import math
import numpy as np
from auxiliares import evaluar_funcion, es_numero_finito, validar_parametros, crear_resultado, terminar, registrar_paso, motivo_parada

def punto_fijo(f, g, x0, tol=1e-6, max_iter=100, raiz_referencia=None):
    resultado = crear_resultado("Punto fijo")
    motivo = validar_parametros(tol, max_iter)
    if motivo is not None:
        return terminar(resultado, "entrada_invalida", motivo)
    if not es_numero_finito(x0):
        return terminar(resultado, "entrada_invalida", "La aproximación inicial debe ser finita.")
    x = float(x0)
    fx = evaluar_funcion(f, x)
    if not es_numero_finito(fx):
        return terminar(resultado, "error_numerico", "La evaluación no es finita o está fuera del dominio.")
    fx = float(fx)
    registrar_paso(resultado, 0, x, fx, None, raiz_referencia)
    if np.abs(fx) < tol:
        return terminar(resultado, "convergencia", motivo_parada(fx, tol))
    for iteracion in range(1, max_iter + 1):
        x_nuevo = evaluar_funcion(g, x) 
        if not es_numero_finito(x_nuevo):
            return terminar(resultado, "error_numerico", "Error al evaluar g. La evaluación no es finita o está fuera del dominio.")
        x_nuevo = float(x_nuevo)
        paso = np.abs(x_nuevo - x)
        if not math.isfinite(paso):
            return terminar(resultado, "error_numerico", "La diferencia entre las aproximaciones no es finita.")
        fx_nuevo = evaluar_funcion(f, x_nuevo)
        if not es_numero_finito(fx_nuevo):
            return terminar(resultado, "error_numerico", "La evaluación no es finita o está fuera del dominio.")
        x = x_nuevo
        fx = float(fx_nuevo)
        registrar_paso(resultado, iteracion, x, fx, paso, raiz_referencia)
        if np.abs(fx) < tol or paso < tol:
            return terminar(resultado, "convergencia", motivo_parada(fx, tol))
    return terminar(resultado, "maximo_iteraciones", "Se alcanzó el máximo de iteraciones sin cumplir el criterio de parada.")
