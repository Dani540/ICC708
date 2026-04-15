# 🌳 Implementación y Análisis de Heaps en Python

Este repositorio contiene una implementación orientada a objetos de la estructura de datos Heap (Min-Heap y Max-Heap) utilizando el módulo nativo `heapq` de Python. Además, incluye la resolución de problemas clásicos de algoritmia para demostrar la eficiencia de estas estructuras frente a enfoques tradicionales.

## A) Implementación

Se desarrollaron dos clases principales para encapsular y facilitar el uso de la librería estándar (y por el gusto del diseño OOP):

* **`CustomMinHeap`**: Clase base que maneja operaciones de Min-Heap, integrando utilidades como `push_pop`, `replace`, y la inicialización optimizada en tiempo lineal O(N) vía `heapify`.
* **`CustomMaxHeap`**: Hereda de la clase base y utiliza el patrón de inversión de signos (almacenar números negativos) para simular un Max-Heap de forma transparente para el usuario.

Se resolvieron los siguientes problemas de rendimiento:

1. **Top-K Elementos**: Extracción de los $K$ mayores/menores.
2. **K-Frecuencias**: Uso de diccionarios y Min-Heap de tamaño fijo.
3. **Merge de K Listas Ordenadas**: Uso de tuplas `(valor, id_lista, id_elemento)` para mantener un consumo de memoria mínimo (O(K)).
4. **Sistema de Recomendación**: Filtrado eficiente del Top-K de productos basándose en puntajes.

---

## B) Comparación: Heaps vs `sorted()`

Al resolver problemas del tipo "Top K", existe la tentación de ordenar toda la estructura de datos y luego hacer un *slicing* (ej. `sorted(arr)[:k]`).

**Ordenamiento Tradicional (`sorted()` en Python):**

* Utiliza Timsort.
* Complejidad de Tiempo: **O(N log N)** en todos los casos.
* Ordena el 100% de los elementos, incluso si solo necesitamos los 3 primeros.

**Enfoque con Heaps (Min-Heap de tamaño K):**

* Mantiene un árbol de tamaño máximo K.
* Complejidad de Tiempo: **O(N log K)**.
* Si K es significativamente menor que N (ej. buscar el Top 10 en 1 millón de registros), la diferencia de rendimiento es abismal, ya que el costo de reordenamiento del árbol es minúsculo en comparación a ordenar toda la lista.

---

## C) Medición de Tiempos de Ejecución

Para validar la teoría, se realizó un *benchmark* buscando los 10 elementos más grandes en una lista de 1,000,000 de enteros aleatorios.

* **Método `sorted()[-k:]`**: ~0.71420 segundos.
* **Método Heap (`heapq.nlargest` / Tamaño fijo K)**: ~0.03120 segundos.

**Resultado:** El enfoque utilizando Heaps demostró ser consistentemente más rápido (22.89 veces más rápido en mi PC) cuando $K \ll N$, ahorrando ciclos de CPU al evitar comparaciones innecesarias.

---

## D) Conclusión

* El uso de `sorted()` es ideal cuando se necesita disponer de **todos** los datos en orden estricto.
* El uso de **Heaps** es la estructura óptima para problemas de prioridades dinámicas, colas de eventos o búsquedas de Top-K, ya que minimiza drásticamente tanto el uso de memoria (RAM) como el tiempo computacional, siendo la opción preferida para entornos de producción con grandes volúmenes de datos.
