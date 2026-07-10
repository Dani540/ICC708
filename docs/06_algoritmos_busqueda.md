# Parte 6: Algoritmos de búsqueda (`algoritmos/busqueda.py`)

Se implementaron los dos algoritmos obligatorios -**BFS** y **UCS/Dijkstra**-
y la extensión opcional **A\***. Los tres devuelven un `ResultadoBusqueda`
con los campos exigidos por el enunciado:

| Campo | Contenido |
|-------|-----------|
| `ruta` | Secuencia de nodos desde el origen hasta el destino (vacía si no hay ruta) |
| `costo` | Costo acumulado de la ruta en minutos (`inf` si no hay ruta) |
| `nodos_visitados` | Nodos **expandidos**, en orden de expansión |
| `tramos` | Número de aristas de la ruta (propiedad derivada) |

"Visitado" significa aquí *expandido*: el nodo salió de la frontera y se
procesaron sus vecinos. Es la métrica estándar para comparar cuánto trabajo
hizo cada algoritmo.

## BFS: búsqueda en anchura

Explora el grafo por niveles con una cola FIFO (`collections.deque`),
marcando cada nodo al descubrirlo. Garantiza la ruta con **menos tramos**,
pero **ignora los pesos**: una ruta de 3 tramos lentos puede costar más
minutos que una de 6 tramos rápidos.

* Complejidad: **O(V + E)** tiempo, O(V) memoria.
* El costo en minutos se calcula *a posteriori* sumando los pesos de la ruta
  encontrada (`_costo_de_ruta`), solo con fines de comparación.

## Dijkstra / UCS: costo uniforme

Expande siempre el nodo de **menor costo acumulado** usando el `MinHeap`
propio como frontera. Al expandir un nodo su costo es definitivo (con pesos
no negativos), así que al llegar al destino la ruta es **óptima en minutos**.

Detalles de implementación:

* **Eliminación perezosa**: si se encuentra un camino mejor hacia un nodo que
  ya está en la frontera, se inserta una nueva entrada en vez de reubicar la
  vieja; las entradas obsoletas se descartan al salir (`if actual in
  expandidos: continue`). Es la variante estándar cuando el heap no soporta
  *decrease-key*, y mantiene el heap simple.
* Complejidad: **O((V + E) log V)** tiempo, O(V + E) memoria.

Dijkstra desde un origen único hacia un destino es exactamente **UCS**
(búsqueda de costo uniforme): misma frontera ordenada por g(n), misma
garantía de optimalidad.

## A*: costo uniforme guiado por heurística

A*ordena la frontera por `f(n) = g(n) + h(n)`, donde g es el costo acumulado
y h una **estimación optimista** de lo que falta. Se implementó con un motor
común (`_busqueda_de_costo_minimo`) que reciben tanto Dijkstra (con `h = 0`)
como A*: la única diferencia entre ambos algoritmos es la heurística, y el
código lo refleja literalmente.

### La heurística y su admisibilidad

```
h(n) = distancia_euclidiana(n, destino) / VELOCIDAD_MAXIMA_KMH × 60   [minutos]
```

Es el tiempo que tomaría volar en línea recta a la velocidad máxima teórica
(60 km/h). Es **admisible** (nunca sobreestima) porque:

1. Ninguna ruta real es más corta que la línea recta (desigualdad
   triangular de la distancia euclidiana), y
2. ninguna vía supera los 55 km/h reales < 60 km/h de referencia (el margen
   absorbe además el redondeo de pesos a un decimal).

También es **consistente** (`h(a) ≤ peso(a,b) + h(b)`), por lo que la
variante con conjunto de expandidos preserva la optimalidad. Resultado: A*
encuentra siempre la misma ruta óptima que Dijkstra, expandiendo menos nodos
porque descarta direcciones que alejan del destino.

## Comparación teórica

| | BFS | Dijkstra/UCS | A* |
|---|-----|--------------|-----|
| Frontera | Cola FIFO | MinHeap por g(n) | MinHeap por g(n) + h(n) |
| Óptimo en tramos | **Sí** | No necesariamente | No necesariamente |
| Óptimo en minutos | No | **Sí** | **Sí** (h admisible) |
| Complejidad | O(V + E) | O((V+E) log V) | O((V+E) log V), menos expansiones |
| Necesita | - | pesos ≥ 0 | pesos ≥ 0 + coordenadas |

## Resultados reales

### Escenario integrado (C-SUR → Z-18)

```
Algoritmo       Tramos  Costo (min)  Visitados
BFS                  3         67.9         33
Dijkstra/UCS         3         67.9         23
A*                   3         67.9          9
```

Aquí la ruta con menos tramos coincide con la óptima, pero el trabajo
realizado difiere: A* expandió **9 nodos contra 33 de BFS** para llegar a la
misma respuesta.

### Promedios del experimento 4 (8 pares centro→zona)

| Algoritmo | Costo promedio (min) | Nodos visitados | Tiempo |
|-----------|----------------------|-----------------|--------|
| BFS | 120.9 | 36.5 | 0.041 ms |
| Dijkstra | **108.8** | 34.1 | 0.190 ms |
| A* | **108.8** | **17.9** | 0.131 ms |

Casos ilustrativos del experimento:

* `C-SUR → Z-48`: BFS eligió 5 tramos con costo **192.2**; la ruta óptima de
  Dijkstra/A* usa 6 tramos pero cuesta **146.8**; un 24 % menos. Menos
  tramos no significa menos tiempo.
* `C-ORIENTE → Z-18`: A* expandió 7 nodos donde Dijkstra necesitó 17, con el
  mismo costo (72.0).

Conclusiones:

1. **BFS** es el más barato de ejecutar pero entrega rutas en promedio 11 %
   más costosas: solo es correcto cuando todas las aristas pesan lo mismo.
2. **Dijkstra** garantiza la ruta de tiempo mínimo, el criterio que importa en
   una emergencia.
3. **A\*** entrega exactamente la misma ruta óptima expandiendo la mitad de
   los nodos que Dijkstra (y hasta 4 veces menos). En un grafo de 55 nodos la
   diferencia de milisegundos es irrelevante, pero la reducción de expansiones
   es la que escala a redes viales reales de millones de nodos.
