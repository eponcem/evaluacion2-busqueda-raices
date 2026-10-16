# Evaluación 2: La raíz que se esconde
 
Proyecto individual de Computación Numérica de la Universidad Católica del Maule, basado en el enunciado de la evaluación «La raíz que se esconde».
 
El proyecto implementa seis métodos: bisección, falsa posición, punto fijo, secante, Newton-Raphson clásico y Newton-Raphson mejorado. Para el último se usa la fórmula con segunda derivada enseñada como Newton-Raphson modificado en la Clase 4 (trabajo autónomo) y en el Tema N°2. El análisis de los resultados se presenta en informe.md.
 
```text
x siguiente = x - f(x) f'(x) / ([f'(x)]² - f(x) f''(x))
```
 
Esta variante no requiere conocer la multiplicidad de la raíz. Antes de calcular la corrección se comprueban las derivadas y el denominador, y se reconoce una raíz inicial para evitar dividir por cero en la raíz doble.
 
## Preparación en Windows
 
Se recomienda Python 3.12 y una terminal PowerShell abierta en la carpeta del proyecto. Las únicas dependencias externas son NumPy y Matplotlib, con versiones fijadas en requirements.txt. El proyecto utiliza un entorno virtual venv.
 
Con Python instalado y el lanzador py disponible, ejecutar:
 
```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python -m pip check
python src/scripts/principal.py
python src/scripts/pruebas.py
```
 
Si py no está disponible, pero python sí está en el PATH, comprobar primero su versión y crear el entorno con:
 
```powershell
python --version
python -m venv .venv
```
 
Si PowerShell impide activar el entorno, se puede usar directamente su intérprete. Estos comandos también sirven cuando .venv ya existe:
 
```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m pip check
.\.venv\Scripts\python.exe src/scripts/principal.py
.\.venv\Scripts\python.exe src/scripts/pruebas.py
```
 
Esta alternativa no requiere cambiar la política global de ejecución de PowerShell. Para salir de un entorno que se activó mediante Activate.ps1, ejecutar deactivate.
 
El proyecto se verificó con Python 3.12.14, NumPy 2.3.5 y Matplotlib 3.11.2, incluyendo una instalación desde un entorno virtual vacío. El programa y las pruebas se ejecutan con el intérprete de .venv.
 
## Ejecución y resultados
 
principal.py realiza las ejecuciones principales de los seis métodos sobre las seis funciones, guarda los historiales y produce los gráficos. Genera 36 resultados principales y 93 experimentos de comparación de condiciones iniciales. Los casos no aplicables o con error numérico también se registran como resultados, con su estado y motivo.
 
Los archivos se escriben en src/data y src/assets, independientemente de la carpeta desde donde se invoque el script. Las rutas se calculan a partir de la ubicación del código. Al repetir la ejecución se regeneran los CSV y PNG con los mismos nombres.
 
La tolerancia común es 1e-6 y el máximo es de 100 iteraciones. El criterio oficial de parada es:
 
```text
|f(x_n)| < tolerancia  O  |x_n - x_(n-1)| < tolerancia
```
 
Una evaluación exactamente igual a cero también permite terminar. Las comparaciones con la tolerancia son estrictas. Se informa qué condición produjo la parada y se conserva el residuo obtenido, incluso cuando la diferencia entre iteraciones cumple la tolerancia antes que el residuo.
 
## Funciones y condiciones iniciales
 
| Función | Fórmula | Intervalo | Inicio de Newton y punto fijo | Inicios de secante |
|---|---|---|---|---|
| Polinómica | x^3 - x - 2 | [1, 2] | 1.5 | 1, 2 |
| Raíz doble | (x - 2)^2 | [1, 3], auxiliar | 1.2, oficial | 1.2, 1.3 |
| Logarítmica | ln(x) + x - 4 | [2, 3] | 2.5 | 2, 3 |
| Exponencial | exp(-x) - x | [0, 1] | 0.5 | 0, 1 |
| Trigonométrica | cos(x) - x | [0, 1] | 0.5 | 0, 1 |
| Mixta | sqrt(x) - cos(x) | [0.1, 1] | 0.55 | 0.1, 1 |
 
Para las raíces simples, los intervalos provienen del Word. Newton y punto fijo parten del punto medio, y la secante parte de los extremos. En la raíz doble, el Word proporciona x0 = 1.2; el intervalo [1, 3] y el segundo dato de secante 1.3 son elecciones explícitas del proyecto, registradas en los datos.
 
La función logarítmica exige x > 0. La función mixta exige x >= 0, mientras sus derivadas requieren x > 0. Los ángulos de las funciones trigonométricas están expresados en radianes.
 
Las iteraciones de punto fijo utilizadas son:
 
| Función | g(x) |
|---|---|
| Polinómica | Raíz cúbica de x + 2 |
| Raíz doble | (x + 2) / 2 |
| Logarítmica | 4 - ln(x) |
| Exponencial | exp(-x) |
| Trigonométrica | cos(x) |
| Mixta | x - 0.5 * (sqrt(x) - cos(x)) |
 
La equivalencia de estas transformaciones y las condiciones de convergencia se analizan en el informe y se comprueban mediante las pruebas y los resultados observados.
 
## Interpretación numérica
 
El historial distingue tres cantidades:
 
- **Residuo:** |f(x_n)|. Mide cuánto incumple la aproximación la ecuación.
- **Paso:** |x_n - x_(n-1)|. Mide el cambio entre dos aproximaciones consecutivas.
- **Error absoluto:** |x_n - raiz_referencia|. Compara la aproximación con una referencia numérica independiente.
Las referencias se comprueban por separado con math y hasta 80 pasos de bisección, usando números float. La división termina si se alcanza un cero o si el redondeo impide seguir estrechando el intervalo. Esta precisión es suficiente para comparar con la tolerancia 1e-6. La referencia de la raíz doble es exactamente 2. Las referencias solo sirven para calcular el error: no intervienen en las fórmulas, en los datos iniciales ni en la parada.
 
convergio indica que se cumplió el criterio oficial de parada. La columna precision_raiz del resumen comprueba por separado si el error absoluto es menor que la tolerancia. En particular, para la raíz doble un residuo pequeño puede coexistir con un error de raíz mayor que 1e-6, porque f(x) = (x - 2)^2.
 
La raíz doble existe y tiene multiplicidad dos, aunque no haya cambio de signo. Bisección y falsa posición se registran como no_aplicable en [1, 3]; no se les atribuye una convergencia artificial. Un extremo que sea raíz exacta sí se reconoce como solución.
 
Las iteraciones cuentan aproximaciones nuevas evaluadas correctamente. Newton, punto fijo y secante registran una aproximación inicial en n = 0; en secante esta fila corresponde a x1, mientras x0 se conserva para la fórmula. Los métodos cerrados empiezan su historial en n = 1, salvo una raíz exacta en un extremo, aceptada con cero actualizaciones.
 
Los estados posibles son convergencia, no_aplicable, entrada_invalida, error_numerico y maximo_iteraciones. Las celdas CSV vacías representan datos que no corresponden o no pudieron calcularse; no representan cero.
 
Los gráficos usan el formato básico de Matplotlib, con título, ejes y leyenda. Los de convergencia usan una escala logarítmica para errores positivos y finitos. Un error cero se informa mediante una nota, sin sustituirlo por una cifra inventada. Los métodos no aplicables aparecen identificados en las leyendas y como NA en la leyenda del resumen de iteraciones. En ese resumen no se dibuja un valor cero para esos casos.
 
## Organización de archivos
 
```text
evaluacion2-busqueda-raices/
├── .gitignore
├── requirements.txt
├── README.md
├── informe.md
├── .venv/                         entorno local, excluido
└── src/
    ├── scripts/
    │   ├── configuracion.py
    │   ├── funciones.py
    │   ├── referencias.py
    │   ├── auxiliares.py
    │   ├── metodos_cerrados.py
    │   ├── metodos_abiertos.py
    │   ├── graficos.py
    │   ├── experimentos.py
    │   ├── principal.py
    │   ├── pruebas_metodos.py
    │   ├── pruebas_archivos.py
    │   └── pruebas.py
    ├── data/                      16 archivos CSV
    │   ├── funcion_<nombre>.csv   6 archivos de muestras
    │   ├── historial_<nombre>.csv 6 archivos de iteraciones
    │   ├── ambiente_controlado.csv
    │   ├── referencias.csv
    │   ├── resumen_convergencia.csv
    │   └── experimentos_iniciales.csv
    └── assets/                    13 archivos PNG
        ├── funcion_<nombre>.png   6 gráficos de las funciones
        ├── convergencia_<nombre>.png
        │                          6 gráficos de error
        └── resumen_iteraciones.png
```
 
| Archivo | Función |
|---|---|
| configuracion.py | Rutas, tolerancia, máximo de iteraciones y nombres de los métodos. |
| funciones.py | Las seis funciones, sus derivadas, mapas de punto fijo y condiciones iniciales. |
| referencias.py | Evaluación independiente con math y cálculo de las raíces de referencia. |
| auxiliares.py | Validaciones, historial y preparación del resultado de los métodos. |
| metodos_cerrados.py | Bisección y falsa posición. |
| metodos_abiertos.py | Punto fijo, secante, Newton clásico y Newton mejorado. |
| graficos.py | Gráficos de funciones, convergencia e iteraciones. |
| experimentos.py | Ejecución de métodos, resumen de resultados y variación de condiciones iniciales. |
| principal.py | Punto de entrada: coordina las ejecuciones y guarda los CSV y gráficos. |
| pruebas_metodos.py | Comprobaciones de funciones, métodos y casos de error. |
| pruebas_archivos.py | Lectura y comprobación de los resultados generados. |
| pruebas.py | Punto de entrada de los cinco grupos de comprobaciones. |
| informe.md | Análisis de resultados, respuestas a las preguntas de convergencia y conclusión. |
| requirements.txt | Versiones de NumPy y Matplotlib utilizadas. |
| .gitignore | Excluye entornos virtuales, cachés y archivos temporales; conserva los CSV y PNG finales. |
 
Solo es necesario ejecutar principal.py para generar los resultados y pruebas.py para comprobarlos. Los otros archivos se importan desde esos puntos de entrada.
 
Las rutas se calculan en configuracion.py con pathlib. Esto permite ejecutar el programa desde distintas carpetas sin escribir rutas absolutas. La tolerancia, el máximo y los nombres de los métodos se declaran en ese mismo archivo.
 
El código usa funciones, ciclos y condicionales. Las funciones de la evaluación usan NumPy; math se utiliza para las referencias y algunas comprobaciones numéricas. Matplotlib se configura con el backend Agg antes de importar pyplot para guardar los PNG sin abrir ventanas. Se utiliza su ubicación normal de caché.
 
Los métodos comprueban los datos antes de calcular. Si una función NumPy del proyecto produce nan o infinito por su dominio o por desbordamiento, un condicional registra error_numerico. También se comprueban los denominadores y las derivadas antes de dividir.
 
Cada método muestra su fórmula, las actualizaciones de las aproximaciones, el paso y la condición de parada. Los auxiliares breves reutilizan las validaciones, el registro del historial y la preparación de la salida.
 
## Reproducción de los experimentos y verificación
 
Los experimentos de experimentos_iniciales.csv comparan los casos base con intervalos más estrechos, aproximaciones más cercanas y distintos inicios de ambos métodos de Newton y de punto fijo. También incluyen la secante con estimaciones simétricas para la raíz doble y ambos métodos de Newton logarítmicos desde x0=1000. Cada fila conserva los datos iniciales, las iteraciones, las métricas y el estado observado.
 
En el código, cada caso tiene un nombre, como base o intervalo_estrecho. Primero se asignan los datos iniciales de la función; luego un if o elif cambia el dato que se quiere estudiar. Así se puede seguir directamente qué valores reciben los métodos en cada comparación.
 
Para reproducirlos, ejecutar principal.py sin editar sus datos. Después, ejecutar pruebas.py. Las comprobaciones se agrupan en funciones, primeros pasos, resultados e historiales, casos de error y archivos generados. Revisan las raíces, las derivadas, los criterios de parada y los errores importantes. Si una condición no se cumple, assert detiene el programa e indica la línea afectada. Si todas se cumplen, se imprime Todas las comprobaciones aprobaron.
 
Si se modifican las funciones, los datos iniciales, la tolerancia o el máximo de iteraciones, deben regenerarse los resultados y repetirse las pruebas. Después se debe actualizar manualmente informe.md con los nuevos CSV y gráficos: el informe no se genera automáticamente.