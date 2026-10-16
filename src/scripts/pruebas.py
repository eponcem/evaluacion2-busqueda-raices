from funciones import obtener_funciones
from referencias import obtener_referencias
from pruebas_metodos import comprobar_funciones, comprobar_primeros_pasos, comprobar_resultados, comprobar_errores
from pruebas_archivos import comprobar_archivos

if __name__ == "__main__":
    funciones = obtener_funciones()
    referencias = obtener_referencias()
    comprobar_funciones(funciones, referencias)
    print("Funciones, derivadas y referencias: correctas.")
    comprobar_primeros_pasos(funciones[0])
    print("Primeros pasos de los seis métodos: correctos.")
    comprobar_resultados(funciones, referencias)
    print("Raíces, criterios de parada e historiales: correctos.")
    comprobar_errores(funciones)
    print("Casos de error y no convergencia: correctos.")
    comprobar_archivos(funciones, referencias)
    print("Archivos de resultados: correctos.")
    print("Todas las comprobaciones aprobaron.")
