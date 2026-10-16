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
    errores = 0
    if len(funciones) != 6:
        print('Error: Se esperaban seis funciones.')
        errores += 1
    for datos in funciones:
        referencia = referencias[datos["id"]]
        if abs(evaluar_referencia(datos['id'], referencia)) >= 2e-14:
            print('Error: La raíz de referencia no cumple la precisión esperada.')
            errores += 1
        if abs(datos['g'](referencia) - referencia) >= 2e-14:
            print('Error: La referencia no es un punto fijo de g.')
            errores += 1

        if datos["doble"]:
            if datos['f'](2.0) != 0:
                print('Error: La función debe ser cero en x = 2.')
                errores += 1
            if datos['df'](2.0) != 0:
                print('Error: La derivada debe ser cero en la raíz doble.')
                errores += 1
            h = 1e-5
            segunda = (datos["df"](2.0 + h) - datos["df"](2.0 - h)) / (2 * h)
            if abs(segunda - 2.0) >= 1e-08:
                print('Error: La segunda derivada no coincide con la aproximación numérica.')
                errores += 1
        else:
            if datos['f'](datos['a']) * datos['f'](datos['b']) >= 0:
                print('Error: Falta el cambio de signo en el intervalo.')
                errores += 1

        h = 1e-5
        for x in np.linspace(datos["a"], datos["b"], 7):
            primera = (datos["f"](x + h) - datos["f"](x - h)) / (2 * h)
            if abs(primera - datos['df'](x)) >= 1e-08:
                print('Error: La primera derivada no coincide con la aproximación numérica.')
                errores += 1
            segunda = (datos["df"](x + h) - datos["df"](x - h)) / (2 * h)
            if abs(segunda - datos['ddf'](x)) >= 1e-07:
                print('Error: La segunda derivada no coincide con la aproximación numérica.')
                errores += 1

        a = datos["a"]
        b = datos["b"]
        if datos["id"] == "logaritmica":
            b = 3.5
        for x in np.linspace(a, b, 51):
            if not (a - 1e-14 <= datos["g"](x) <= b + 1e-14):
                print('Error: g(x) sale del intervalo estudiado.')
                errores += 1
        derivada_g = (datos["g"](referencia + h) - datos["g"](referencia - h)) / (2 * h)
        if abs(derivada_g) >= 1:
            print('Error: La derivada de g debe tener valor absoluto menor que uno.')
            errores += 1
    return errores

def comprobar_primeros_pasos(datos):
    errores = 0
    if biseccion(datos['f'], 1.0, 2.0, max_iter=1)['raiz'] != 1.5:
        print('Error: El primer paso del método no coincide con el cálculo esperado.')
        errores += 1
    if abs(falsa_posicion(datos['f'], 1.0, 2.0, max_iter=1)['raiz'] - 4.0 / 3.0) >= 1e-14:
        print('Error: El primer paso del método no coincide con el cálculo esperado.')
        errores += 1
    if abs(secante(datos['f'], 1.0, 2.0, max_iter=1)['raiz'] - 4.0 / 3.0) >= 1e-14:
        print('Error: El primer paso del método no coincide con el cálculo esperado.')
        errores += 1
    if abs(newton_raphson(datos['f'], datos['df'], 1.5, max_iter=1)['raiz'] - 35.0 / 23.0) >= 1e-14:
        print('Error: El primer paso del método no coincide con el cálculo esperado.')
        errores += 1
    if abs(newton_mejorado(datos['f'], datos['df'], datos['ddf'], 1.5, max_iter=1)['raiz'] - 832.0 / 547.0) >= 1e-14:
        print('Error: El primer paso del método no coincide con el cálculo esperado.')
        errores += 1
    if abs(punto_fijo(datos['f'], datos['g'], 1.5, max_iter=1)['raiz'] - math.cbrt(3.5)) >= 1e-14:
        print('Error: El primer paso del método no coincide con el cálculo esperado.')
        errores += 1
    return errores

def comprobar_resultados(funciones, referencias):
    errores = 0
    for datos in funciones:
        referencia = referencias[datos["id"]]
        resultados = ejecutar_metodos(datos, referencia)
        for resultado in resultados:
            if datos["doble"] and resultado["metodo"] in ("Bisección", "Falsa posición"):
                if resultado['estado'] != 'no_aplicable':
                    print('Error: El método cerrado no debe aplicarse sin cambio de signo.')
                    errores += 1
                if resultado['raiz'] is not None:
                    print('Error: El caso no aplicable no debe tener una raíz calculada.')
                    errores += 1
                continue

            if not (resultado["convergio"]):
                print('Error: No se obtuvo la convergencia o el resultado esperado.')
                errores += 1
            if not resultado["historial"]:
                print("Error: falta el historial de " + resultado["metodo"] + " en " + datos["id"])
                errores += 1
                continue
            ultimo = resultado["historial"][-1]
            if resultado['iteraciones'] != ultimo['iteracion']:
                print('Error: El número de iteraciones no coincide con el historial.')
                errores += 1
            if resultado['raiz'] != ultimo['x']:
                print('Error: La raíz no coincide con la última aproximación.')
                errores += 1
            if not (ultimo["residuo"] < 1e-6 or (ultimo["paso"] is not None and ultimo["paso"] < 1e-6)):
                print('Error: El resultado no cumple el criterio de parada.')
                errores += 1
            if not datos["doble"]:
                if abs(resultado['raiz'] - referencia) >= 1e-06:
                    print('Error: La raíz calculada no tiene la precisión esperada.')
                    errores += 1

            anterior = None
            for fila in resultado["historial"]:
                if abs(fila['fx'] - datos['f'](fila['x'])) >= 1e-13:
                    print('Error: f(x) no coincide con el valor guardado en el historial.')
                    errores += 1
                if fila['residuo'] != abs(fila['fx']):
                    print('Error: El residuo guardado es incorrecto.')
                    errores += 1
                if fila['error_absoluto'] != abs(fila['x'] - referencia):
                    print('Error: El error absoluto guardado es incorrecto.')
                    errores += 1
                if anterior is not None:
                    if fila['iteracion'] != anterior['iteracion'] + 1:
                        print('Error: Las iteraciones del historial no son consecutivas.')
                        errores += 1
                    if fila['paso'] != abs(fila['x'] - anterior['x']):
                        print('Error: El paso guardado no coincide con la diferencia de aproximaciones.')
                        errores += 1
                anterior = fila

        sin_referencia = ejecutar_metodos(datos)
        for i in range(len(resultados)):
            if resultados[i]['raiz'] != sin_referencia[i]['raiz']:
                print('Error: La referencia está alterando la ejecución del método.')
                errores += 1
            if resultados[i]['iteraciones'] != sin_referencia[i]['iteraciones']:
                print('Error: La referencia está alterando la ejecución del método.')
                errores += 1

    doble = funciones[1]
    resultado = newton_raphson(doble["f"], doble["df"], 1.2, raiz_referencia=2.0)
    if resultado['iteraciones'] != 10:
        print('Error: El número de iteraciones no coincide con lo esperado.')
        errores += 1
    if resultado['historial'][-1]['residuo'] >= 1e-06:
        print('Error: El residuo final no cumple la tolerancia.')
        errores += 1
    if resultado['historial'][-1]['error_absoluto'] <= 1e-06:
        print('Error: La prueba debe distinguir el residuo del error en la raíz doble.')
        errores += 1
    resultado = newton_mejorado(doble["f"], doble["df"], doble["ddf"], 1.2, raiz_referencia=2.0)
    if not (resultado["convergio"] and resultado["iteraciones"] == 1):
        print('Error: No se obtuvo la convergencia o el resultado esperado.')
        errores += 1
    if abs(resultado['raiz'] - 2.0) >= 1e-14:
        print('Error: La raíz calculada no tiene la precisión esperada.')
        errores += 1
    return errores

def f_sin_raiz(x):
    return x * x + 1

def df_sin_raiz(x):
    return 2 * x

def ddf_sin_raiz(x):
    return 2.0

def f_constante(x):
    return 1.0

def g_paso_pequeno(x):
    return x + 1e-8

def g_paso_cuarto(x):
    return x + 0.25

def comprobar_errores(funciones):
    errores = 0
    for tol in (0.0, -1e-6, np.nan):
        for resultado in ejecutar_metodos(funciones[0], tol=tol):
            if resultado['estado'] != 'entrada_invalida':
                print('Error: El método no rechazó los parámetros inválidos.')
                errores += 1
    for maximo in (0, -1):
        for resultado in ejecutar_metodos(funciones[0], max_iter=maximo):
            if resultado['estado'] != 'entrada_invalida':
                print('Error: El método no rechazó los parámetros inválidos.')
                errores += 1
    for resultado in ejecutar_metodos(funciones[0], max_iter=1):
        if resultado['convergio']:
            print('Error: El método indicó convergencia cuando no correspondía.')
            errores += 1
        if resultado['iteraciones'] != 1:
            print('Error: El número de iteraciones no coincide con lo esperado.')
            errores += 1

    for indice in (2, 5):
        datos = funciones[indice]
        if newton_raphson(datos['f'], datos['df'], -1.0)['estado'] != 'error_numerico':
            print('Error: El método no detectó el problema de dominio, derivada o denominador.')
            errores += 1
        if newton_mejorado(datos['f'], datos['df'], datos['ddf'], -1.0)['estado'] != 'error_numerico':
            print('Error: El método no detectó el problema de dominio, derivada o denominador.')
            errores += 1
    if newton_raphson(f_sin_raiz, df_sin_raiz, 0.0)['estado'] != 'error_numerico':
        print('Error: El método no detectó el problema de dominio, derivada o denominador.')
        errores += 1
    if secante(funciones[1]['f'], 1.0, 3.0)['estado'] != 'error_numerico':
        print('Error: El método no detectó el problema de dominio, derivada o denominador.')
        errores += 1
    if biseccion(funciones[0]['f'], 2.0, 1.0)['estado'] != 'entrada_invalida':
        print('Error: El método no rechazó los parámetros inválidos.')
        errores += 1
    if newton_raphson(funciones[0]['f'], funciones[0]['df'], np.inf)['estado'] != 'entrada_invalida':
        print('Error: El método no rechazó los parámetros inválidos.')
        errores += 1
    if newton_raphson(funciones[5]['f'], funciones[5]['df'], 0.0)['estado'] != 'error_numerico':
        print('Error: El método no detectó el problema de dominio, derivada o denominador.')
        errores += 1
    resultado = newton_raphson(funciones[1]["f"], funciones[1]["df"], 2.0)
    if not (resultado["convergio"] and resultado["iteraciones"] == 0):
        print('Error: No se obtuvo la convergencia o el resultado esperado.')
        errores += 1
    resultado = newton_mejorado(funciones[1]["f"], funciones[1]["df"], funciones[1]["ddf"], 2.0)
    if not (resultado["convergio"] and resultado["iteraciones"] == 0):
        print('Error: No se obtuvo la convergencia o el resultado esperado.')
        errores += 1
    if newton_mejorado(f_sin_raiz, df_sin_raiz, ddf_sin_raiz, 1.0)['estado'] != 'error_numerico':
        print('Error: El método no detectó el problema de dominio, derivada o denominador.')
        errores += 1
    if newton_mejorado(f_sin_raiz, df_sin_raiz, ddf_sin_raiz, 0.0)['estado'] != 'error_numerico':
        print('Error: El método no detectó el problema de dominio, derivada o denominador.')
        errores += 1
    if newton_mejorado(funciones[0]['f'], funciones[0]['df'], funciones[0]['ddf'], np.inf)['estado'] != 'entrada_invalida':
        print('Error: El método no rechazó los parámetros inválidos.')
        errores += 1

    resultado = punto_fijo(f_constante, g_paso_pequeno, 0.0)
    if not (resultado["convergio"] and resultado["historial"][-1]["residuo"] == 1.0):
        print('Error: No se obtuvo la convergencia o el resultado esperado.')
        errores += 1
    resultado = punto_fijo(f_constante, g_paso_cuarto, 0.0, tol=0.25, max_iter=1)
    if resultado['convergio']:
        print('Error: El método indicó convergencia cuando no correspondía.')
        errores += 1
    return errores
