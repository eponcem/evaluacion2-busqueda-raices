import math
from funciones import obtener_funciones

def evaluar_referencia(identificador, x):
    if identificador == "polinomica":
        valor = x**3 - x - 2.0
    elif identificador == "raiz_doble":
        valor = (x - 2.0)**2
    elif identificador == "logaritmica":
        valor = math.log(x) + x - 4.0
    elif identificador == "exponencial":
        valor = math.exp(-x) - x
    elif identificador == "trigonometrica":
        valor = math.cos(x) - x
    elif identificador == "mixta":
        valor = math.sqrt(x) - math.cos(x)
    else:
        raise ValueError("Identificador de función desconocido.")
    return valor

def obtener_referencias():
    referencias = {}
    funciones = obtener_funciones()
    for datos in funciones:
        identificador = datos["id"]
        if datos["doble"]:
            referencias[identificador] = 2.0
            continue

        a = datos["a"]
        b = datos["b"]
        fa = evaluar_referencia(identificador, a)
        fb = evaluar_referencia(identificador, b)
        if fa * fb >= 0:
            raise ValueError("La referencia requiere un cambio de signo.")

        for paso in range(80):
            punto_medio = (a + b) / 2.0
            valor_medio = evaluar_referencia(identificador, punto_medio)
            if valor_medio == 0:
                break
            if punto_medio == a or punto_medio == b:
                break
            if fa * valor_medio < 0:
                b = punto_medio
            else:
                a = punto_medio
                fa = valor_medio

        referencias[identificador] = punto_medio
    return referencias