# Evaluación 2: La raíz que se esconde

Trabajo individual de Computación Numérica de la Universidad Católica del Maule. Se comparan seis métodos de búsqueda de raíces: bisección, falsa posición, punto fijo, secante, Newton-Raphson y Newton mejorado. El análisis está en `informe.md`.

## Preparación y ejecución

Desde la carpeta del proyecto, en PowerShell y con Python 3.12 instalado:

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe src/scripts/principal.py
.\.venv\Scripts\python.exe src/scripts/pruebas.py
```

Si no está disponible `py`, se puede crear el entorno con `python -m venv .venv`. Si el entorno ya existe, no hace falta crearlo otra vez. Las dependencias son NumPy y Matplotlib; sus versiones se indican en `requirements.txt`.

`principal.py` genera 36 resultados principales, 93 experimentos sobre condiciones iniciales, los CSV de `src/data` y los gráficos PNG de `src/assets`. Al ejecutarlo otra vez se reemplazan los resultados anteriores. Los gráficos se guardan sin abrir ventanas.

`pruebas.py` revisa las funciones y sus derivadas, los primeros pasos, las raíces, los historiales y los archivos generados. Utiliza condicionales `if`, mensajes y un contador de errores. Solo anuncia que todas las comprobaciones aprobaron si el contador total es cero; si hay errores, termina con código 1.

## Funciones y datos iniciales

| Función | Fórmula | Intervalo | Inicio de Newton y punto fijo | Inicios de secante |
|---|---|---|---|---|
| Polinómica | x³ − x − 2 | [1, 2] | 1.5 | 1, 2 |
| Raíz doble | (x − 2)² | [1, 3], auxiliar | 1.2 | 1.2, 1.3 |
| Logarítmica | ln(x) + x − 4 | [2, 3] | 2.5 | 2, 3 |
| Exponencial | exp(−x) − x | [0, 1] | 0.5 | 0, 1 |
| Trigonométrica | cos(x) − x | [0, 1] | 0.5 | 0, 1 |
| Mixta | √x − cos(x) | [0.1, 1] | 0.55 | 0.1, 1 |

Los intervalos de las raíces simples y el inicio 1.2 de la raíz doble provienen del enunciado. El intervalo auxiliar [1, 3] y el segundo inicio de secante 1.3 son elecciones del proyecto. Los ángulos están en radianes.

Para punto fijo se usan, respectivamente: raíz cúbica de (x + 2), (x + 2)/2, 4 − ln(x), exp(−x), cos(x) y x − 0.5(√x − cos(x)). Su justificación está en el informe.

## Cálculos y comprobaciones

La tolerancia es `1e-6` y el máximo es de 100 iteraciones. El criterio de parada es:

```text
|f(x_n)| < tolerancia  O  |x_n − x_(n−1)| < tolerancia
```

Se distinguen el residuo `|f(x)|`, el paso entre aproximaciones y el error absoluto respecto a una raíz de referencia. La referencia se calcula por separado y no interviene en la parada. Cumplir el criterio no garantiza que el error de la raíz sea menor que la tolerancia: esto se observa especialmente en la raíz doble.

Bisección y falsa posición se registran como no aplicables en [1, 3] para la raíz doble porque no hay cambio de signo. Si un extremo ya es una raíz exacta, se acepta como solución.

Newton mejorado utiliza la fórmula con segunda derivada de Clase 4 y Tema N°2:

```text
x siguiente = x − f(x) f'(x) / ([f'(x)]² − f(x) f''(x))
```

Los datos se definen como números dentro del programa y el máximo de iteraciones debe ser entero. Se comprueban tolerancias positivas y finitas, máximos positivos, intervalos válidos, valores no finitos, dominios y divisiones por cero. La función logarítmica requiere x > 0; la mixta requiere x ≥ 0 y sus derivadas x > 0.

Los resultados indican convergencia, caso no aplicable, entrada inválida, error numérico o máximo de iteraciones. Las celdas vacías representan datos que no corresponden o no pudieron calcularse. El error cero se señala en los gráficos de convergencia, ya que no se puede representar en escala logarítmica.

## Archivos del trabajo

| Archivo o carpeta | Contenido |
|---|---|
| `src/scripts/configuracion.py` | Rutas, tolerancia, máximo y nombres de los métodos. |
| `src/scripts/funciones.py` | Funciones, derivadas, transformaciones de punto fijo y datos iniciales. |
| `src/scripts/metodos_cerrados.py` | Bisección y falsa posición. |
| `src/scripts/metodos_abiertos.py` | Punto fijo, secante y los dos métodos de Newton. |
| `src/scripts/auxiliares.py` | Validaciones, registro del historial y resultados. |
| `src/scripts/referencias.py` | Cálculo separado de las raíces de referencia. |
| `src/scripts/experimentos.py` | Comparación de métodos y condiciones iniciales. |
| `src/scripts/graficos.py` | Gráficos de funciones, errores e iteraciones. |
| `src/scripts/principal.py` | Ejecución y guardado de los resultados. |
| `src/scripts/pruebas*.py` | Comprobaciones del cálculo y los archivos. |
| `src/data/` | 16 archivos CSV con muestras, historiales, referencias y comparaciones. |
| `src/assets/` | 13 gráficos PNG. |
| `informe.md` | Análisis y conclusiones. |

Si se cambian las funciones, los datos iniciales o la tolerancia, hay que ejecutar nuevamente el programa y las pruebas. El informe se actualiza manualmente con los resultados obtenidos.
