from configuracion import tolerancia, max_iteraciones, nombres_metodos
from metodos_cerrados import biseccion, falsa_posicion
from metodos_abiertos import punto_fijo, secante, newton_raphson, newton_mejorado

def ejecutar_metodo(nombre, funcion, referencia, a, b, x0, secante_x0, secante_x1):
    f = funcion["f"]
    if nombre == "Bisección":
        resultado = biseccion(f, a, b, tolerancia, max_iteraciones, referencia)
    elif nombre == "Falsa posición":
        resultado = falsa_posicion(f, a, b, tolerancia, max_iteraciones, referencia)
    elif nombre == "Punto fijo":
        resultado = punto_fijo(f, funcion["g"], x0, tolerancia, max_iteraciones, referencia)
    elif nombre == "Secante":
        resultado = secante(f, secante_x0, secante_x1, tolerancia, max_iteraciones, referencia)
    elif nombre == "Newton-Raphson":
        resultado = newton_raphson(f, funcion["df"], x0, tolerancia, max_iteraciones, referencia)
    elif nombre == "Newton mejorado":
        resultado = newton_mejorado(f, funcion["df"], funcion["ddf"], x0, tolerancia, max_iteraciones, referencia)
    else:
        raise ValueError("Método desconocido.")
    return resultado

def resumir_resultado(funcion, nombre, resultado, referencia):
    error = None
    residuo = None
    paso = None
    if resultado["historial"]:
        ultimo = resultado["historial"][-1]
        error = ultimo["error_absoluto"]
        residuo = ultimo["residuo"]
        paso = ultimo["paso"]
    precision_raiz = False
    if error is not None:
        precision_raiz = error < tolerancia
    return {"funcion": funcion["id"], "metodo": nombre, "iteraciones": resultado["iteraciones"], "raiz": resultado["raiz"], "error": error, "residuo": residuo, "paso": paso, "convergio": resultado["convergio"], "precision_raiz": precision_raiz, "estado": resultado["estado"], "motivo": resultado["motivo"], "raiz_referencia": referencia, "tolerancia": tolerancia, "max_iteraciones": max_iteraciones,}

def ejecutar_experimentos(funciones, referencias):
    filas = []
    intervalos_estrechos = {"polinomica": [1.4, 1.6], "raiz_doble": [1.5, 2.5], "logaritmica": [2.8, 3.0], "exponencial": [0.5, 0.7], "trigonometrica": [0.7, 0.8], "mixta": [0.6, 0.7],}
    for funcion in funciones:
        referencia = float(referencias[funcion["id"]])
        a_estrecho = intervalos_estrechos[funcion["id"]][0]
        b_estrecho = intervalos_estrechos[funcion["id"]][1]
        for nombre in nombres_metodos:
            casos = ["base"]
            if nombre in ("Bisección", "Falsa posición"):
                casos.append("intervalo_estrecho")
            elif nombre == "Secante":
                casos.append("estimaciones_cercanas")
                if funcion["doble"]:
                    casos.append("estimaciones_simetricas")
            else:
                casos.append("inicio_inferior")
                casos.append("inicio_superior")
                if funcion["id"] == "logaritmica" and nombre in ("Newton-Raphson", "Newton mejorado"):
                    casos.append("inicio_lejano")

            for caso in casos:
                a = funcion["a"]
                b = funcion["b"]
                x0 = funcion["x0"]
                secante_x0 = funcion["secante_x0"]
                secante_x1 = funcion["secante_x1"]

                if caso == "intervalo_estrecho":
                    a = a_estrecho
                    b = b_estrecho
                elif caso == "estimaciones_cercanas":
                    if funcion["doble"]:
                        secante_x0 = 1.9
                        secante_x1 = 1.95
                    else:
                        secante_x0 = a_estrecho
                        secante_x1 = b_estrecho
                elif caso == "estimaciones_simetricas":
                    secante_x0 = 1.0
                    secante_x1 = 3.0
                elif caso == "inicio_inferior":
                    if funcion["doble"]:
                        x0 = 1.9
                    else:
                        x0 = a + 0.05 * (b - a)
                elif caso == "inicio_superior":
                    if funcion["doble"]:
                        x0 = 3.0
                    else:
                        x0 = b - 0.05 * (b - a)
                elif caso == "inicio_lejano":
                    x0 = 1000.0

                resultado = ejecutar_metodo(nombre, funcion, referencia, a, b, x0, secante_x0, secante_x1)
                fila = resumir_resultado(funcion, nombre, resultado, referencia)
                fila["caso"] = caso
                fila["a"] = a
                fila["b"] = b
                fila["x0"] = x0
                fila["secante_x0"] = secante_x0
                fila["secante_x1"] = secante_x1
                filas.append(fila)
    return filas
