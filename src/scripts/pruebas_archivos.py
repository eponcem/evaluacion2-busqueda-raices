import csv
import math
from configuracion import carpeta_datos, carpeta_graficos
from metodos_abiertos import newton_mejorado
from pruebas_metodos import ejecutar_metodos

def leer_csv(nombre):
    ruta = carpeta_datos / nombre
    assert ruta.is_file(), "Ejecute primero principal.py. Falta " + nombre
    with ruta.open(encoding="utf-8", newline="") as archivo:
        lector = csv.DictReader(archivo)
        return lector.fieldnames, list(lector)
