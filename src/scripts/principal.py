import csv
import numpy as np
from configuracion import carpeta_datos, carpeta_graficos, tolerancia, max_iteraciones, nombres_metodos
from funciones import obtener_funciones
from referencias import obtener_referencias
from experimentos import ejecutar_metodo, resumir_resultado, ejecutar_experimentos
from graficos import graficar_funcion, graficar_convergencia, graficar_resumen

def guardar_csv(nombre, columnas, filas):
    ruta = carpeta_datos / nombre
    with ruta.open("w", newline="", encoding="utf-8") as archivo:
        escritor = csv.DictWriter(archivo, fieldnames=columnas)
        escritor.writeheader()
        escritor.writerows(filas)

if __name__ == "__main__":
    carpeta_datos.mkdir(parents=True, exist_ok=True)
    carpeta_graficos.mkdir(parents=True, exist_ok=True)
    funciones = obtener_funciones()
    referencias = obtener_referencias()
    resumen = []
    ambiente = []
    filas_referencias = []
    columnas_resumen = ["funcion", "metodo", "iteraciones", "raiz", "error", "residuo", "paso", "convergio", "precision_raiz", "estado", "motivo", "raiz_referencia", "tolerancia", "max_iteraciones"]
    for funcion in funciones:
        referencia = float(referencias[funcion["id"]])
        a = funcion["a"]
        b = funcion["b"]
        fa = float(funcion["f"](a))
        fb = float(funcion["f"](b))
        demostracion = "Cambio de signo y continuidad"
        if funcion["doble"]:
            demostracion = "f(2)=0, f'(2)=0, f''(2)=2; f(x)>=0; tangencia"
        ambiente.append({"funcion": funcion["id"], "formula": funcion["formula"], "a": a, "b": b, "x0": funcion["x0"], "secante_x0": funcion["secante_x0"], "secante_x1": funcion["secante_x1"], "tolerancia": tolerancia, "max_iteraciones": max_iteraciones, "f(a)": fa, "f(b)": fb, "producto": fa * fb, "demostracion": demostracion, "g(x)": funcion["formula_g"]})
        filas_referencias.append({"funcion": funcion["id"], "raiz_referencia": referencia})
        x = np.linspace(a, b, 401)
        y = funcion["f"](x)
        muestras = []
        for i in range(len(x)):
            muestras.append({"x": float(x[i]), "f(x)": float(y[i])})
        guardar_csv(f"funcion_{funcion['id']}.csv", ["x", "f(x)"], muestras)
        resultados = {}
        historial = []
        for nombre in nombres_metodos:
            resultado = ejecutar_metodo(nombre, funcion, referencia, a, b, funcion["x0"], funcion["secante_x0"], funcion["secante_x1"])
            resultados[nombre] = resultado
            fila = resumir_resultado(funcion, nombre, resultado, referencia)
            resumen.append(fila)
            for registro in resultado["historial"]:
                fila_historial = {"metodo": nombre, "iteracion": registro["iteracion"], "x": registro["x"], "fx": registro["fx"], "residuo": registro["residuo"], "paso": registro["paso"], "error_absoluto": registro["error_absoluto"],}
                historial.append(fila_historial)
            print(f"{funcion['id']:14} | {nombre:16} | n={resultado['iteraciones']:3} | {resultado['estado']}")
        guardar_csv(f"historial_{funcion['id']}.csv", ["metodo", "iteracion", "x", "fx", "residuo", "paso", "error_absoluto"], historial)
        graficar_funcion(funcion, referencia, x, y)
        graficar_convergencia(funcion, resultados)
    guardar_csv("resumen_convergencia.csv", columnas_resumen, resumen)
    guardar_csv("ambiente_controlado.csv", list(ambiente[0]), ambiente)
    guardar_csv("referencias.csv", ["funcion", "raiz_referencia"], filas_referencias)
    experimentos = ejecutar_experimentos(funciones, referencias)
    columnas_experimentos = ["caso", "a", "b", "x0", "secante_x0", "secante_x1"] + columnas_resumen
    guardar_csv("experimentos_iniciales.csv", columnas_experimentos, experimentos)
    graficar_resumen(funciones, resumen)
    print(f"Generados {len(resumen)} resultados principales y {len(experimentos)} experimentos.")
    print("Datos: src/data. Gráficos: src/assets.")
    print("Newton mejorado: variante con segunda derivada indicada en Clase 4 y Tema N°2.")
