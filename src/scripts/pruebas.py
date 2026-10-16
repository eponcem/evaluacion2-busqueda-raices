import sys
from funciones import obtener_funciones
from referencias import obtener_referencias
from pruebas_metodos import comprobar_funciones, comprobar_primeros_pasos, comprobar_resultados, comprobar_errores
from pruebas_archivos import comprobar_archivos

def mostrar_resumen(nombre, errores):
    if errores == 0:
        print(nombre + ": correcto.")
    else:
        print(nombre + ": " + str(errores) + " errores.")


if __name__ == "__main__":
    funciones = obtener_funciones()
    referencias = obtener_referencias()
    total_errores = 0

    errores = comprobar_funciones(funciones, referencias)
    mostrar_resumen("Funciones, derivadas y referencias", errores)
    total_errores += errores

    errores = comprobar_primeros_pasos(funciones[0])
    mostrar_resumen("Primeros pasos de los seis métodos", errores)
    total_errores += errores

    errores = comprobar_resultados(funciones, referencias)
    mostrar_resumen("Raíces, criterios de parada e historiales", errores)
    total_errores += errores

    errores = comprobar_errores(funciones)
    mostrar_resumen("Casos de error y no convergencia", errores)
    total_errores += errores

    errores = comprobar_archivos(funciones, referencias)
    mostrar_resumen("Archivos de resultados", errores)
    total_errores += errores

    if total_errores == 0:
        print("Todas las comprobaciones aprobaron.")
    else:
        print("Se encontraron " + str(total_errores) + " errores en total.")
        sys.exit(1)
