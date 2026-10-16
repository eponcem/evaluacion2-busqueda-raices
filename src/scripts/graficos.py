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
