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
