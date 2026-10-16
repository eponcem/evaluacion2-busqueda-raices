from pathlib import Path as path

carpeta_src = path(__file__).resolve().parent.parent
carpeta_datos = carpeta_src / "data"
carpeta_graficos = carpeta_src / "assets"
tolerancia = 1e-6
max_iteraciones = 100
nombres_metodos = ["Bisección", "Falsa posición", "Punto fijo", "Secante", "Newton-Raphson", "Newton mejorado"]