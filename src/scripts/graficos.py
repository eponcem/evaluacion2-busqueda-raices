import numpy as np
import matplotlib
from configuracion import carpeta_graficos, nombres_metodos

# Los gráficos se guardan en PNG sin abrir ventanas.
matplotlib.use("Agg")
import matplotlib.pyplot as plt

def graficar_funcion(funcion, referencia, x, y):
    plt.figure()
    plt.plot(x, y, label=funcion["formula"])
    etiqueta = f"Raíz: {referencia:.6f}"
    if funcion["doble"]:
        etiqueta = "Raíz doble: x = 2 (tangencia)"
    plt.plot(referencia, 0, "ro", label=etiqueta)
    plt.axhline(0, color="black", linewidth=0.8)
    plt.title(funcion["nombre"])
    plt.xlabel("x")
    plt.ylabel("f(x)")
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.savefig(carpeta_graficos / f"funcion_{funcion['id']}.png")
    plt.close()

def graficar_convergencia(funcion, resultados):
    plt.figure()
    notas = []
    for nombre in nombres_metodos:
        resultado = resultados[nombre]
        iteraciones = []
        errores = []
        ceros = []
        for registro in resultado["historial"]:
            error = registro["error_absoluto"]
            if error is not None and np.isfinite(error):
                if error > 0:
                    iteraciones.append(registro["iteracion"])
                    errores.append(error)
                elif error == 0:
                    ceros.append(registro["iteracion"])
        etiqueta = nombre
        if resultado["estado"] == "no_aplicable":
            etiqueta += " (no aplica)"
        elif not resultado["convergio"]:
            etiqueta += " (no converge)"
        if ceros:
            notas.append(f"{nombre}: error cero en n={ceros[0]}")
        estilo = ".-"
        if nombre == "Newton-Raphson":
            estilo = ".--"
        plt.semilogy(iteraciones, errores, estilo, label=etiqueta)
    plt.title(f"Convergencia: {funcion['nombre']}")
    plt.xlabel("Iteración")
    plt.ylabel("Error absoluto")
    plt.grid(True)
    plt.legend(fontsize=9)
    if notas:
        plt.figtext(0.5, 0.01, "; ".join(notas), ha="center", fontsize=8)
        plt.tight_layout(rect=(0, 0.05, 1, 1))
    else:
        plt.tight_layout()
    plt.savefig(carpeta_graficos / f"convergencia_{funcion['id']}.png")
    plt.close()

def graficar_resumen(funciones, resumen):
    plt.figure(figsize=(9, 5))
    nombres_funciones = []
    for funcion in funciones:
        nombres_funciones.append(funcion["nombre"])
    for nombre in nombres_metodos:
        cantidades = []
        no_aplica = False
        no_converge = False
        for funcion in funciones:
            for fila in resumen:
                if fila["funcion"] == funcion["id"] and fila["metodo"] == nombre:
                    if fila["estado"] == "no_aplicable":
                        cantidades.append(np.nan)
                        no_aplica = True
                    else:
                        cantidades.append(fila["iteraciones"])
                        if not fila["convergio"]:
                            no_converge = True
                    break
        etiqueta = nombre
        if no_aplica:
            etiqueta += " (NA: sin cambio de signo)"
        if no_converge:
            etiqueta += " (incluye casos sin convergencia)"
        plt.plot(nombres_funciones, cantidades, ".-", label=etiqueta)
    plt.title("Iteraciones por método y función")
    plt.xlabel("Función")
    plt.ylabel("Iteraciones")
    plt.grid(True)
    plt.legend(fontsize=8)
    plt.tight_layout()
    plt.savefig(carpeta_graficos / "resumen_iteraciones.png")
    plt.close()
