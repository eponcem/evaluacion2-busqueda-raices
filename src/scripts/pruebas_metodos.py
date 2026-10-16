import math
import numpy as np
from referencias import evaluar_referencia
from metodos_cerrados import biseccion, falsa_posicion
from metodos_abiertos import punto_fijo, secante, newton_raphson, newton_mejorado

def ejecutar_metodos(datos, referencia=None, tol=1e-6, max_iter=100):
    f = datos["f"]
    resultados = [
        biseccion(f, datos["a"], datos["b"], tol, max_iter, referencia),
        falsa_posicion(f, datos["a"], datos["b"], tol, max_iter, referencia),
        punto_fijo(f, datos["g"], datos["x0"], tol, max_iter, referencia),
        secante(f, datos["secante_x0"], datos["secante_x1"], tol, max_iter, referencia),
        newton_raphson(f, datos["df"], datos["x0"], tol, max_iter, referencia),
        newton_mejorado(f, datos["df"], datos["ddf"], datos["x0"], tol, max_iter, referencia),
    ]
    return resultados

def comprobar_funciones(funciones, referencias):
    assert len(funciones) == 6
    for datos in funciones:
        referencia = referencias[datos["id"]]
        assert abs(evaluar_referencia(datos["id"], referencia)) < 2e-14
        assert abs(datos["g"](referencia) - referencia) < 2e-14

        if datos["doble"]:
            assert datos["f"](2.0) == 0
            assert datos["df"](2.0) == 0
            h = 1e-5
            segunda = (datos["df"](2.0 + h) - datos["df"](2.0 - h)) / (2 * h)
            assert abs(segunda - 2.0) < 1e-8
        else:
            assert datos["f"](datos["a"]) * datos["f"](datos["b"]) < 0

        h = 1e-5
        for x in np.linspace(datos["a"], datos["b"], 7):
            primera = (datos["f"](x + h) - datos["f"](x - h)) / (2 * h)
            assert abs(primera - datos["df"](x)) < 1e-8
            segunda = (datos["df"](x + h) - datos["df"](x - h)) / (2 * h)
            assert abs(segunda - datos["ddf"](x)) < 1e-7

        a = datos["a"]
        b = datos["b"]
        if datos["id"] == "logaritmica":
            b = 3.5
        for x in np.linspace(a, b, 51):
            assert a - 1e-14 <= datos["g"](x) <= b + 1e-14
        derivada_g = (datos["g"](referencia + h) - datos["g"](referencia - h)) / (2 * h)
        assert abs(derivada_g) < 1

def comprobar_primeros_pasos(datos):
    assert biseccion(datos["f"], 1.0, 2.0, max_iter=1)["raiz"] == 1.5
    assert abs(falsa_posicion(datos["f"], 1.0, 2.0, max_iter=1)["raiz"] - 4.0 / 3.0) < 1e-14
    assert abs(secante(datos["f"], 1.0, 2.0, max_iter=1)["raiz"] - 4.0 / 3.0) < 1e-14
    assert abs(newton_raphson(datos["f"], datos["df"], 1.5, max_iter=1)["raiz"] - 35.0 / 23.0) < 1e-14
    assert abs(newton_mejorado(datos["f"], datos["df"], datos["ddf"], 1.5, max_iter=1)["raiz"] - 832.0 / 547.0) < 1e-14
    assert abs(punto_fijo(datos["f"], datos["g"], 1.5, max_iter=1)["raiz"] - math.cbrt(3.5)) < 1e-14

def comprobar_resultados(funciones, referencias):
    for datos in funciones:
        referencia = referencias[datos["id"]]
        resultados = ejecutar_metodos(datos, referencia)
        for resultado in resultados:
            if datos["doble"] and resultado["metodo"] in ("Bisección", "Falsa posición"):
                assert resultado["estado"] == "no_aplicable"
                assert resultado["raiz"] is None
                continue

            assert resultado["convergio"], (datos["id"], resultado["metodo"])
            ultimo = resultado["historial"][-1]
            assert resultado["iteraciones"] == ultimo["iteracion"]
            assert resultado["raiz"] == ultimo["x"]
            assert ultimo["residuo"] < 1e-6 or ultimo["paso"] < 1e-6
            if not datos["doble"]:
                assert abs(resultado["raiz"] - referencia) < 1e-6

            anterior = None
            for fila in resultado["historial"]:
                assert abs(fila["fx"] - datos["f"](fila["x"])) < 1e-13
                assert fila["residuo"] == abs(fila["fx"])
                assert fila["error_absoluto"] == abs(fila["x"] - referencia)
                if anterior is not None:
                    assert fila["iteracion"] == anterior["iteracion"] + 1
                    assert fila["paso"] == abs(fila["x"] - anterior["x"])
                anterior = fila

        sin_referencia = ejecutar_metodos(datos)
        for i in range(len(resultados)):
            assert resultados[i]["raiz"] == sin_referencia[i]["raiz"]
            assert resultados[i]["iteraciones"] == sin_referencia[i]["iteraciones"]

    doble = funciones[1]
    resultado = newton_raphson(doble["f"], doble["df"], 1.2, raiz_referencia=2.0)
    assert resultado["iteraciones"] == 10
    assert resultado["historial"][-1]["residuo"] < 1e-6
    assert resultado["historial"][-1]["error_absoluto"] > 1e-6
    resultado = newton_mejorado(doble["f"], doble["df"], doble["ddf"], 1.2, raiz_referencia=2.0)
    assert resultado["convergio"] and resultado["iteraciones"] == 1
    assert abs(resultado["raiz"] - 2.0) < 1e-14

def f_sin_raiz(x): return x * x + 1

def df_sin_raiz(x): return 2 * x

def ddf_sin_raiz(x): return 2.0

def f_constante(x): return 1.0

def g_paso_pequeno(x): return x + 1e-8

def g_paso_cuarto(x): return x + 0.25
