# Lab 5 — Algoritmos de Búsqueda (BFS, DFS, UCS, A*)

Implementación y comparación de **BFS, DFS, UCS y A\*** sobre dos escenarios: **grafos/árboles**
y **laberintos** (matrices de `0` y `1`). La idea de fondo es que los 4 algoritmos
están escritos una sola vez y sirven para ambos escenarios (ver `Informe.pdf`).

## Qué necesita para correrlo

```bash
pip install -r requirements.txt   # matplotlib, numpy, networkx
```

Igual no es obligatorio, si falta matplotlib, el programa cae solo a una visualización en texto y sigue funcionando.

## Cómo se ejecute

### 1. Menú interactivo

```bash
python main.py
```

Deja elegir escenario (grafo/laberinto), de dónde sacar los datos (predefinido o
CSV), el algoritmo, el nodo inicial y el objetivo. Muestra el orden de visita, el
camino, el costo y la visualización gráfica. (Si elije "Todos", las ventanas
gráficas van apareciendo a medida que cierra la anterior.)

### 2. Modo demo (genera todas las capturas de una)

```bash
python main.py --demo
```

Corre los 4 algoritmos en los dos escenarios, imprime la tabla comparativa y guarda
los PNG en `capturas/`.

### 3. Pruebas

```bash
python tests/test_algoritmos.py        # sin depender de pytest
# o:  python -m pytest tests/
```

## Cómo está organizado

| Archivo | Para qué |
| --- | --- |
| `src/problema.py` | La interface común `Problema` + la clase `Resultado` |
| `src/algoritmos.py` | BFS, DFS, UCS, A\* (el corazón del lab, los algoritmos) |
| `src/grafo.py` | El grafo + lectura de CSV (lista y matriz de adyacencia) |
| `src/laberinto.py` | El laberinto (matriz 0/1) + lectura de CSV |
| `src/escenarios.py` | Los escenarios que dejé hardcodeados |
| `src/visualizacion.py` | Visualización con matplotlib + respaldo en texto |
| `main.py` | El menú interactivo y el modo `--demo` |
| `data/` | Los CSV de prueba (grafo lista/matriz, coordenadas, laberinto) |
| `tests/` | Las pruebas automáticas |
| `capturas/` | Las imágenes que genera (PNG) |
| `Informe.pdf` | El informe completo |

## Formato de los CSV

- **Grafo lista de adyacencia** (`data/grafo_lista.csv`): `origen,destino,costo`
- **Grafo matriz de adyacencia** (`data/grafo_matriz.csv`): tabla NxN, `0` = sin arista
- **Coordenadas** (`data/grafo_coords.csv`): `nodo,x,y` (opcional, le da heurística a A\*)
- **Laberinto** (`data/laberinto.csv`): filas de `0` (libre) y `1` (barrera)

## Conclusión

Los 4 algoritmos son agnósticos al problema: no saben si están sobre un grafo o un
laberinto, solo preguntan `vecinos()`, `es_objetivo()` y `heuristica()`. Por eso el
mismo BFS me sirve para los dos escenarios, que al final es la misma idea sin
importar el escenario o problema. El detalle completo está en el informe.
