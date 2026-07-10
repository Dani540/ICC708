# Análisis experimental (`experimentos.py`)

## Metodología

* Tiempos medidos con `time.perf_counter()` (el reloj de mayor resolución de
  la librería estándar), reportados en ms totales y µs por operación.
* Todos los generadores aleatorios usan semillas fijas: los experimentos son
  **reproducibles** ejecutando `python experimentos.py`.
* Datos sintéticos para hashing, heap y ordenamiento (tamaños crecientes);
  para grafos se usa la red vial real del proyecto (55 nodos, 115 aristas).
* Entorno de las mediciones citadas: Python 3.13.4 sobre Windows 11.

---

## Experimento 1: Tabla hash

**Pregunta**: ¿la tabla mantiene O(1) al crecer, y cuánto mejora frente a una
búsqueda lineal? Se insertan n claves y luego se ejecutan 500 búsquedas
aleatorias sobre la tabla y sobre una lista de pares.

| n | capacidad | carga | colisiones | buckets | máx | inserción | 500 búsq. hash | 500 búsq. lineal |
|---|-----------|-------|------------|---------|-----|-----------|----------------|------------------|
| 100 | 163 | 0.613 | 47 | 60 | 2 | 0.40 ms | 0.76 ms | 0.86 ms |
| 500 | 673 | 0.743 | 295 | 314 | 3 | 2.08 ms | 0.72 ms | 3.73 ms |
| 1 000 | 1 361 | 0.735 | 750 | 522 | 4 | 3.72 ms | 1.17 ms | 9.42 ms |
| 5 000 | 10 949 | 0.457 | 1 742 | 4 802 | 2 | 40.31 ms | 1.63 ms | 41.79 ms |
| 20 000 | 43 853 | 0.456 | 4 968 | 18 504 | 3 | 106.11 ms | 1.05 ms | 219.74 ms |

**Discusión**: el tiempo de búsqueda en la tabla es plano (~1 ms) mientras el
lineal crece proporcionalmente a n, hasta ser **200× más lento** con 20 000
claves. El redimensionamiento mantiene el factor de carga ≤ 0.75 y el bucket
más largo nunca pasa de 4 entradas: djb2 con capacidades primas distribuye
uniformemente las claves `I-xxxxx` pese a sus prefijos idénticos. La
inserción total crece linealmente con n, confirmando el O(1) amortizado por
elemento aun pagando los redimensionamientos.

---

## Experimento 2: Cola de prioridad (heap)

**Pregunta**: ¿inserción y extracción se comportan como O(log n)? Se insertan
n incidentes sintéticos con prioridades aleatorias, se actualizan 200
prioridades y se extrae todo.

| n | inserción | por elem | 200 updates | extracción | por elem |
|---|-----------|----------|-------------|------------|----------|
| 500 | 4.31 ms | 8.62 µs | 1.83 ms | 18.04 ms | 36.08 µs |
| 2 000 | 20.60 ms | 10.30 µs | 2.87 ms | 76.18 ms | 38.09 µs |
| 10 000 | 118.96 ms | 11.90 µs | 3.99 ms | 624.22 ms | 62.42 µs |
| 50 000 | 773.10 ms | 15.46 µs | 5.43 ms | 4 240.89 ms | 84.82 µs |

**Discusión**: multiplicar n por 100 solo multiplica el costo unitario por
~1.8 (inserción) y ~2.4 (extracción); crecimiento logarítmico, coherente con
log₂(500) ≈ 9 vs log₂(50 000) ≈ 15.6. La extracción es más cara porque
`_hundir` compara con dos hijos por nivel y cada intercambio actualiza el
índice de posiciones en la `TablaHash`; ese es el precio de poder actualizar
prioridades en O(log n), que a cambio hace que 200 actualizaciones cuesten
milisegundos incluso con 50 000 elementos (sin índice serían 200 barridos
O(n)).

---

## Experimento 3: Ordenamiento

**Pregunta**: ¿cómo se comparan MergeSort y QuickSort entre sí y contra el
`sorted()` nativo, incluyendo los casos patológicos clásicos?

| n | caso | merge_sort | quick_sort | sorted() |
|---|------|-----------|------------|----------|
| 1 000 | aleatorio | 4.91 ms | 7.19 ms | 0.27 ms |
| 1 000 | ordenado | 6.00 ms | 6.00 ms | 0.02 ms |
| 1 000 | inverso | 6.72 ms | 4.85 ms | 0.02 ms |
| 5 000 | aleatorio | 22.95 ms | 16.06 ms | 0.53 ms |
| 5 000 | ordenado | 20.32 ms | 15.56 ms | 0.03 ms |
| 5 000 | inverso | 14.48 ms | 11.80 ms | 0.02 ms |
| 15 000 | aleatorio | 73.67 ms | 59.77 ms | 1.94 ms |
| 15 000 | ordenado | 45.30 ms | 38.67 ms | 0.22 ms |
| 15 000 | inverso | 65.70 ms | 38.97 ms | 0.25 ms |

**Discusión**: ambos escalan como n log n (×15 en n ⇒ ×13–15 en tiempo).
QuickSort con pivote central y partición de tres vías **no degenera** en los
casos ordenado/inverso - al contrario, son sus mejores casos - y supera a
MergeSort en listas grandes. `sorted()` (Timsort en C) es ~30× más rápido y
además explota el orden preexistente (0.22 ms para 15 000 ya ordenados); la
brecha mide el costo del intérprete, no un defecto de los algoritmos. Detalle
completo en [04_ordenamiento.md](04_ordenamiento.md).

---

## Experimento 4: Búsqueda en grafos

**Pregunta**: ¿cuánto cuesta la optimalidad (Dijkstra vs BFS) y cuánto ahorra
la heurística (A* vs Dijkstra)? 8 pares centro→zona aleatorios sobre la red
real.

Promedios de los 8 pares:

| Algoritmo | Costo (min) | Nodos visitados | Tiempo |
|-----------|-------------|-----------------|--------|
| BFS | 120.9 | 36.5 | 0.041 ms |
| Dijkstra | **108.8** | 34.1 | 0.190 ms |
| A* | **108.8** | **17.9** | 0.131 ms |

Casos individuales destacados:

| Par | BFS | Dijkstra/A* | Observación |
|-----|-----|-------------|-------------|
| C-SUR → Z-48 | 192.2 min (5 tramos) | 146.8 min (6 tramos) | BFS 31 % más caro con menos tramos |
| C-SUR → Z-02 | 97.0 min (3 tramos) | 86.8 min (6 tramos) | La ruta corta en tramos no es la rápida |
| C-ORIENTE → Z-18 | 74.1 min | 72.0 min; A* visita 7 vs 17 | Heurística recorta 59 % de expansiones |

**Discusión**: BFS es el más veloz por operación (frontera FIFO sin heap)
pero sus rutas cuestan en promedio **11 % más minutos**, inaceptable cuando el
objetivo es tiempo de respuesta. Dijkstra y A*devuelven siempre el mismo
costo óptimo - evidencia empírica de que la heurística euclidiana es
admisible - y A* expande en promedio **47 % menos nodos** que Dijkstra. En
este grafo pequeño eso apenas se nota en milisegundos, pero la reducción de
expansiones es la propiedad que escala a redes viales grandes.

---

## Conclusiones generales

1. **Cada estructura cumple su complejidad teórica de forma medible**: la
   tabla hash busca en tiempo constante, el heap opera en tiempo logarítmico
   y los ordenamientos escalan n log n.
2. **Las constantes importan**: `sorted()` en C es 30× más rápido que
   nuestros O(n log n) en Python; BFS por operación es 4× más barato que
   Dijkstra. La elección correcta depende de qué se optimiza (correctitud del
   costo, trabajo total, simplicidad).
3. **Las estructuras se potencian entre sí**: la tabla hash dentro de la cola
   de prioridad habilita `actualizar_prioridad` O(log n); el heap propio es
   la frontera de Dijkstra/A*; los ordenamientos y la tabla generan los
   reportes. El sistema integrado usa cada pieza donde su complejidad es la
   adecuada.
