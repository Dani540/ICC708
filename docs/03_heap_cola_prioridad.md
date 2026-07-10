# Parte 3: Heap y Priority Queue (`estructuras/heap.py`, `estructuras/cola_prioridad.py`)

El sistema tiene dos estructuras basadas en montículo binario:

* **`MinHeap`**: montículo de mínimos genérico. Lo usan Dijkstra y A* como
  frontera de exploración, y `top_k` de la cola de prioridad.
* **`PriorityQueue`**: cola de prioridad **máxima** especializada en
  incidentes, con actualización de prioridad en O(log n) gracias a un índice
  de posiciones construido con la `TablaHash` propia.

## El montículo binario sobre un arreglo

Un montículo binario es un árbol binario completo guardado en un arreglo, sin
punteros. Las relaciones padre/hijo se calculan con aritmética de índices:

```
padre(i)          = (i - 1) // 2
hijo_izquierdo(i) = 2i + 1
hijo_derecho(i)   = 2i + 2

arreglo:  [A, B, C, D, E, F]          A
índices:   0  1  2  3  4  5         /   \
                                   B     C
                                  / \   /
                                 D   E F
```

**Invariante de montículo (mín)**: todo nodo es ≤ que sus hijos. Por lo tanto
el mínimo global siempre está en la raíz (índice 0).

Las dos operaciones de reparación restauran el invariante moviéndose por un
solo camino raíz–hoja, de longitud ⌊log₂ n⌋:

* **Flotar** (*sift up*): tras insertar al final, el nuevo elemento sube
  intercambiándose con su padre mientras lo viole.
* **Hundir** (*sift down*): tras extraer la raíz se coloca el último elemento
  arriba y baja intercambiándose con el menor de sus hijos.

## `MinHeap`

Guarda tuplas `(prioridad, elemento)` y **compara únicamente la prioridad**,
por lo que los elementos no necesitan ser comparables entre sí.

| Operación | Precondición | Postcondición | Complejidad |
|-----------|--------------|---------------|-------------|
| `insertar(prioridad, elemento)` | prioridad comparable | El par queda en el montículo; invariante restaurado | O(log n) |
| `extraer_minimo()` | montículo no vacío (si no, `IndexError`) | Devuelve el par de menor prioridad y lo elimina | O(log n) |
| `minimo()` | montículo no vacío | Devuelve el par mínimo sin extraerlo | O(1) |

## `PriorityQueue` (cola de prioridad máxima de incidentes)

Cada entrada del arreglo es un par mutable `[prioridad, incidente]` y el
invariante es de **máximos**: la raíz es siempre el incidente más urgente.
La prioridad con la que se inserta cada incidente es su
`prioridad_efectiva = base × (1 + horas_de_espera)` (ver
[01_diseno_adt.md](01_diseno_adt.md)).

### El índice de posiciones

Para `actualizar_prioridad` hace falta localizar un incidente dentro del
arreglo; una búsqueda lineal costaría O(n). La cola mantiene una `TablaHash`
`id → índice` que se actualiza en cada intercambio (`_intercambiar`), de modo
que localizar cuesta O(1) y la operación completa O(log n). Es el mismo
truco que usan los *indexed heaps* de los libros de texto, construido aquí
sobre la tabla hash de la Parte 2.

### Operaciones

| Operación | Precondición | Postcondición | Complejidad |
|-----------|--------------|---------------|-------------|
| `insertar(incidente, prioridad)` | `incidente.id` no está en la cola | El incidente queda encolado e indexado | O(log n) |
| `extraer_mas_urgente()` | cola no vacía (si no, `IndexError`) | Devuelve `(prioridad, incidente)` con prioridad máxima y lo elimina del heap y del índice | O(log n) |
| `actualizar_prioridad(id, nueva)` | - | Si el id existe: prioridad cambiada e invariante restaurado (flota si subió, se hunde si bajó); devuelve `True`/`False` | O(log n) |
| `top_k(k)` | `k ≥ 0` | Lista de los k pares más urgentes en orden descendente, **sin modificar la cola** | O(n log n) |

`top_k` copia las entradas en un `MinHeap` auxiliar con prioridades negadas y
extrae k veces. Se aceptó O(n log n) a cambio de no mutar la cola real ni
duplicar la lógica del heap; para los tamaños del sistema (n = 520, k = 10) es
instantáneo.

### Por qué máximos y no mínimos

La urgencia crece con la prioridad efectiva, así que la extracción natural es
"dame el mayor". En lugar de negar prioridades sobre el `MinHeap` genérico, la
cola implementa sus propios `_flotar`/`_hundir` de máximos porque de todas
formas necesita engancharse en cada intercambio para mantener el índice de
posiciones - algo que el `MinHeap` genérico, pensado como frontera efímera
de Dijkstra/A*, no necesita.

## Resultados reales

Experimento 2 (tiempos totales en ms; "por elem" en µs):

| n | inserción | por elem | 200 updates | extracción | por elem |
|---|-----------|----------|-------------|------------|----------|
| 500 | 4.31 | 8.62 | 1.83 | 18.04 | 36.08 |
| 2 000 | 20.60 | 10.30 | 2.87 | 76.18 | 38.09 |
| 10 000 | 118.96 | 11.90 | 3.99 | 624.22 | 62.42 |
| 50 000 | 773.10 | 15.46 | 5.43 | 4 240.89 | 84.82 |

* El costo por elemento crece muy despacio al multiplicar n por 100
  (8.6 → 15.5 µs al insertar), el comportamiento esperado de O(log n):
  log₂(500) ≈ 9 frente a log₂(50 000) ≈ 15.6.
* Las 200 actualizaciones tardan pocos ms incluso con 50 000 elementos:
  la localización O(1) vía tabla hash evita el barrido lineal.
* La extracción es más cara que la inserción porque `_hundir` compara con dos
  hijos en cada nivel y cada intercambio actualiza dos entradas del índice de
  posiciones; sigue siendo logarítmica.

En el escenario integrado, la cola con 520 incidentes entrega como más urgente
a `I-0102` (prioridad 364.0) y el `top_k(10)` coincide exactamente con el
ordenamiento completo por prioridad efectiva de la Parte 4: dos caminos
distintos que validan el mismo resultado.
