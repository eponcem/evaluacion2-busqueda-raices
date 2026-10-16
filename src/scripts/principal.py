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
