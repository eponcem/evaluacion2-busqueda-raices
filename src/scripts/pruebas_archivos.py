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

def comprobar_archivos(funciones, referencias):
    columnas, resumen = leer_csv("resumen_convergencia.csv")
    assert len(resumen) == 36
    assert "iteraciones" in columnas and "raiz" in columnas and "error" in columnas
    for datos in funciones:
        columnas, muestras = leer_csv("funcion_" + datos["id"] + ".csv")
        assert columnas == ["x", "f(x)"] and len(muestras) == 401
        for fila in muestras:
            x = float(fila["x"])
            fx = float(fila["f(x)"])
            assert math.isfinite(x) and math.isfinite(fx)
            assert abs(fx - datos["f"](x)) < 1e-13

        resultados = ejecutar_metodos(datos, referencias[datos["id"]])
        for resultado in resultados:
            encontrado = False
            for fila in resumen:
                if fila["funcion"] == datos["id"] and fila["metodo"] == resultado["metodo"]:
                    assert not encontrado, "Hay un resultado repetido en el resumen."
                    encontrado = True
                    assert int(fila["iteraciones"]) == resultado["iteraciones"]
                    assert fila["estado"] == resultado["estado"]
                    if resultado["raiz"] is None:
                        assert fila["raiz"] == "" and fila["error"] == ""
                    else:
                        assert float(fila["raiz"]) == resultado["raiz"]
                        assert float(fila["error"]) == resultado["historial"][-1]["error_absoluto"]
            assert encontrado, "Falta un método en el resumen."

        for prefijo in ("funcion_", "convergencia_"):
            ruta = carpeta_graficos / (prefijo + datos["id"] + ".png")
            assert ruta.is_file(), "Falta un gráfico. Ejecute principal.py."
            assert ruta.stat().st_size > 0, "El gráfico está vacío."
    _, experimentos = leer_csv("experimentos_iniciales.csv")
    assert len(experimentos) == 93
    logaritmica = funciones[2]
    esperado = newton_mejorado(logaritmica["f"], logaritmica["df"], logaritmica["ddf"], 1000.0, raiz_referencia=referencias["logaritmica"])
    encontrado = False
    for fila in experimentos:
        if fila["funcion"] == "logaritmica" and fila["metodo"] == "Newton mejorado" and fila["caso"] == "inicio_lejano":
            assert not encontrado
            encontrado = True
            assert float(fila["x0"]) == 1000.0
            assert int(fila["iteraciones"]) == esperado["iteraciones"]
            assert fila["estado"] == esperado["estado"]
            assert float(fila["raiz"]) == esperado["raiz"]
    assert encontrado
    ruta = carpeta_graficos / "resumen_iteraciones.png"
    assert ruta.is_file() and ruta.stat().st_size > 0
