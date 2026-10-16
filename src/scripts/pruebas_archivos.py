import csv
import math
from configuracion import carpeta_datos, carpeta_graficos
from metodos_abiertos import newton_mejorado
from pruebas_metodos import ejecutar_metodos

def leer_csv(nombre):
    ruta = carpeta_datos / nombre
    if not ruta.is_file():
        print("Error: falta " + nombre + ". Ejecuta primero principal.py.")
        return None, None
    with ruta.open(encoding="utf-8", newline="") as archivo:
        lector = csv.DictReader(archivo)
        return lector.fieldnames, list(lector)

def comprobar_archivos(funciones, referencias):
    errores = 0
    columnas, resumen = leer_csv("resumen_convergencia.csv")
    if resumen is None:
        return errores + 1
    if len(resumen) != 36:
        print('Error: El resumen debe contener 36 resultados.')
        errores += 1
    if not ("iteraciones" in columnas and "raiz" in columnas and "error" in columnas):
        print('Error: Faltan columnas en el resumen.')
        errores += 1
    for datos in funciones:
        columnas, muestras = leer_csv("funcion_" + datos["id"] + ".csv")
        if muestras is None:
            errores += 1
            continue
        if not (columnas == ["x", "f(x)"] and len(muestras) == 401):
            print('Error: El CSV debe contener las columnas x, f(x) y 401 muestras.')
            errores += 1
        for fila in muestras:
            x = float(fila["x"])
            fx = float(fila["f(x)"])
            if not (math.isfinite(x) and math.isfinite(fx)):
                print('Error: Una muestra contiene un valor no finito.')
                errores += 1
            if abs(fx - datos['f'](x)) >= 1e-13:
                print('Error: Una muestra del CSV no coincide con la función.')
                errores += 1

        resultados = ejecutar_metodos(datos, referencias[datos["id"]])
        for resultado in resultados:
            encontrado = False
            for fila in resumen:
                if fila["funcion"] == datos["id"] and fila["metodo"] == resultado["metodo"]:
                    if encontrado:
                        print('Error: Hay un resultado repetido en el CSV.')
                        errores += 1
                    encontrado = True
                    if int(fila['iteraciones']) != resultado['iteraciones']:
                        print('Error: El número de iteraciones no coincide con lo esperado.')
                        errores += 1
                    if fila['estado'] != resultado['estado']:
                        print('Error: El estado del CSV no coincide con la ejecución.')
                        errores += 1
                    if resultado["raiz"] is None:
                        if not (fila["raiz"] == "" and fila["error"] == ""):
                            print('Error: El caso no aplicable debe tener raíz y error vacíos.')
                            errores += 1
                    else:
                        if float(fila['raiz']) != resultado['raiz']:
                            print('Error: La raíz del CSV no coincide con la ejecución.')
                            errores += 1
                        if float(fila['error']) != resultado['historial'][-1]['error_absoluto']:
                            print('Error: El error del CSV no coincide con el historial.')
                            errores += 1
            if not (encontrado):
                print('Error: Falta un resultado esperado en el CSV.')
                errores += 1

        for prefijo in ("funcion_", "convergencia_"):
            ruta = carpeta_graficos / (prefijo + datos["id"] + ".png")
            if not ruta.is_file():
                print("Error: falta el gráfico " + ruta.name)
                errores += 1
            elif ruta.stat().st_size == 0:
                print("Error: el gráfico está vacío: " + ruta.name)
                errores += 1
    _, experimentos = leer_csv("experimentos_iniciales.csv")
    if experimentos is None:
        return errores + 1
    if len(experimentos) != 93:
        print('Error: Se esperaban 93 experimentos.')
        errores += 1
    logaritmica = funciones[2]
    esperado = newton_mejorado(logaritmica["f"], logaritmica["df"], logaritmica["ddf"], 1000.0, raiz_referencia=referencias["logaritmica"])
    encontrado = False
    for fila in experimentos:
        if fila["funcion"] == "logaritmica" and fila["metodo"] == "Newton mejorado" and fila["caso"] == "inicio_lejano":
            if encontrado:
                print('Error: Hay un resultado repetido en el CSV.')
                errores += 1
            encontrado = True
            if float(fila['x0']) != 1000.0:
                print('Error: El experimento lejano debe comenzar en x0 = 1000.')
                errores += 1
            if int(fila['iteraciones']) != esperado['iteraciones']:
                print('Error: Las iteraciones del CSV no coinciden con la ejecución.')
                errores += 1
            if fila['estado'] != esperado['estado']:
                print('Error: El estado del CSV no coincide con la ejecución.')
                errores += 1
            if float(fila['raiz']) != esperado['raiz']:
                print('Error: La raíz del CSV no coincide con la ejecución.')
                errores += 1
    if not (encontrado):
        print('Error: Falta un resultado esperado en el CSV.')
        errores += 1
    ruta = carpeta_graficos / "resumen_iteraciones.png"
    if not ruta.is_file():
        print("Error: falta el gráfico de resumen.")
        errores += 1
    elif ruta.stat().st_size == 0:
        print("Error: el gráfico de resumen está vacío.")
        errores += 1
    return errores
