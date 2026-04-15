import timeit
import random
import heapq

# Generamos un millón de números aleatorios
N = 1_000_000
K = 10
datos = [random.randint(1, 10_000_000) for _ in range(N)]

def test_sorted():
    # Ordena TODO el millón de números y saca los últimos 10
    return sorted(datos)[-K:]

def test_heap():
    # Solo mantiene un heap de tamaño 10 usando la librería nativa
    return heapq.nlargest(K, datos)

# Ejecutamos cada test 10 veces para sacar un promedio
tiempo_sorted = timeit.timeit(test_sorted, number=10) / 10
tiempo_heap = timeit.timeit(test_heap, number=10) / 10

print(f"Buscando el Top {K} en {N} registros:")
print(f"Tiempo con sorted(): {tiempo_sorted:.5f} segundos")
print(f"Tiempo con Heaps:    {tiempo_heap:.5f} segundos")
print(f"¡El Heap fue {tiempo_sorted / tiempo_heap:.2f} veces más rápido!")