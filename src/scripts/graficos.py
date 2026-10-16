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
