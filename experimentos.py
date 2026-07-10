import csv
import random
import time
from datetime import datetime, timedelta
from pathlib import Path

from algoritmos.busqueda import a_estrella, bfs, dijkstra
from algoritmos.ordenamiento import merge_sort, quick_sort
from estructuras.cola_prioridad import PriorityQueue
from estructuras.tabla_hash import TablaHash
from modelos import Incident, RoadNetwork

DIRECTORIO_DATOS = Path(__file__).parent / "datos"
FECHA_BASE = datetime(2026, 7, 4, 12, 0)


def cronometrar(funcion) -> tuple[object, float]:
    """Ejecuta la funcion y devuelve (resultado, milisegundos)"""
    inicio = time.perf_counter()
    resultado = funcion()
    return resultado, (time.perf_counter() - inicio) * 1000.0


def titulo(texto: str) -> None:
    print(f"\n{'=' * 78}")
    print(texto)
    print("=" * 78)


def incidentes_sinteticos(cantidad: int, rng: random.Random) -> list[Incident]:
    return [
        Incident(
            id=f"I-{numero:05d}",
            ubicacion=f"Z-{rng.randint(1, 51):02d}",
            prioridad=rng.randint(1, 5),
            tipo="sintetico",
            timestamp=FECHA_BASE - timedelta(minutes=rng.uniform(0, 4320)),
        )
        for numero in range(cantidad)
    ]


def experimento_hashing() -> None:
    titulo("EXPERIMENTO 1 - Tabla hash: metricas y rendimiento (500 busquedas)")
    print(f"{'n':>7} {'capacidad':>10} {'carga':>7} {'colisiones':>11} {'buckets':>8} "
          f"{'max':>4} {'insercion':>11} {'hash':>9} {'lineal':>9}")
    for cantidad in [100, 500, 1000, 5000, 20000]:
        rng = random.Random(cantidad)
        claves = [f"I-{numero:05d}" for numero in range(cantidad)]
        pares = [(clave, numero) for numero, clave in enumerate(claves)]
        consultas = [rng.choice(claves) for _ in range(500)]

        tabla = TablaHash()

        def insertar_todo():
            for clave, valor in pares:
                tabla.insertar(clave, valor)

        def buscar_en_tabla():
            for clave in consultas:
                tabla.buscar(clave)

        def buscar_en_lista():
            for objetivo in consultas:
                for clave, _ in pares:
                    if clave == objetivo:
                        break

        _, tiempo_insercion = cronometrar(insertar_todo)
        _, tiempo_tabla = cronometrar(buscar_en_tabla)
        _, tiempo_lista = cronometrar(buscar_en_lista)
        est = tabla.estadisticas()
        print(f"{cantidad:>7} {est.capacidad:>10} {est.factor_carga:>7.3f} "
              f"{est.colisiones:>11} {est.buckets_usados:>8} {est.bucket_maximo:>4} "
              f"{tiempo_insercion:>9.2f}ms {tiempo_tabla:>7.2f}ms {tiempo_lista:>7.2f}ms")


def experimento_heap() -> None:
    titulo("EXPERIMENTO 2 - Cola de prioridad: insercion, actualizacion y extraccion")
    print(f"{'n':>7} {'insercion':>11} {'por elem':>10} {'200 updates':>12} "
          f"{'extraccion':>11} {'por elem':>10}")
    for cantidad in [500, 2000, 10000, 50000]:
        rng = random.Random(cantidad)
        incidentes = incidentes_sinteticos(cantidad, rng)
        prioridades = [rng.uniform(1.0, 400.0) for _ in range(cantidad)]
        cola = PriorityQueue()

        def insertar_todo():
            for incidente, prioridad in zip(incidentes, prioridades):
                cola.insertar(incidente, prioridad)

        muestras = rng.sample(range(cantidad), 200)

        def actualizar_muestras():
            for indice in muestras:
                cola.actualizar_prioridad(incidentes[indice].id, prioridades[indice] * 2.0)

        def extraer_todo():
            while not cola.esta_vacia():
                cola.extraer_mas_urgente()

        _, tiempo_insercion = cronometrar(insertar_todo)
        _, tiempo_actualizacion = cronometrar(actualizar_muestras)
        _, tiempo_extraccion = cronometrar(extraer_todo)
        print(f"{cantidad:>7} {tiempo_insercion:>9.2f}ms {tiempo_insercion / cantidad * 1000:>8.2f}us "
              f"{tiempo_actualizacion:>10.2f}ms {tiempo_extraccion:>9.2f}ms "
              f"{tiempo_extraccion / cantidad * 1000:>8.2f}us")


def experimento_ordenamiento() -> None:
    titulo("EXPERIMENTO 3 - Ordenamiento: MergeSort vs QuickSort vs sorted()")
    print(f"{'n':>7} {'caso':<10} {'merge_sort':>11} {'quick_sort':>11} {'sorted()':>11}")
    for cantidad in [1000, 5000, 15000]:
        rng = random.Random(cantidad)
        aleatorio = [rng.random() for _ in range(cantidad)]
        casos = [
            ("aleatorio", aleatorio),
            ("ordenado", sorted(aleatorio)),
            ("inverso", sorted(aleatorio, reverse=True)),
        ]
        for nombre, datos in casos:
            _, tiempo_merge = cronometrar(lambda: merge_sort(datos))
            _, tiempo_quick = cronometrar(lambda: quick_sort(datos))
            _, tiempo_python = cronometrar(lambda: sorted(datos))
            print(f"{cantidad:>7} {nombre:<10} {tiempo_merge:>9.2f}ms "
                  f"{tiempo_quick:>9.2f}ms {tiempo_python:>9.2f}ms")


def experimento_grafos() -> None:
    titulo("EXPERIMENTO 4 - Busqueda en grafos: BFS vs Dijkstra vs A*")
    red = RoadNetwork.cargar_desde_csv(
        DIRECTORIO_DATOS / "nodos.csv", DIRECTORIO_DATOS / "aristas.csv"
    )
    with open(DIRECTORIO_DATOS / "centros.csv", newline="", encoding="utf-8") as archivo:
        ubicaciones = [fila["ubicacion"] for fila in csv.DictReader(archivo)]

    rng = random.Random(42)
    zonas = [nodo for nodo in red.nodos() if nodo.startswith("Z-")]
    pares = [(centro, rng.choice(zonas)) for centro in ubicaciones for _ in range(2)]
    algoritmos = [("BFS", bfs), ("Dijkstra", dijkstra), ("A*", a_estrella)]

    print(f"{'origen':<11} {'destino':<8} {'algoritmo':<10} {'tramos':>7} "
          f"{'costo':>8} {'visitados':>10} {'tiempo':>9}")
    acumulados = {nombre: [0.0, 0, 0.0] for nombre, _ in algoritmos}
    for origen, destino in pares:
        for nombre, algoritmo in algoritmos:
            resultado, tiempo = cronometrar(lambda: algoritmo(red, origen, destino))
            acumulados[nombre][0] += resultado.costo
            acumulados[nombre][1] += len(resultado.nodos_visitados)
            acumulados[nombre][2] += tiempo
            print(f"{origen:<11} {destino:<8} {nombre:<10} {resultado.tramos:>7} "
                  f"{resultado.costo:>8.1f} {len(resultado.nodos_visitados):>10} "
                  f"{tiempo:>7.3f}ms")

    print(f"\n{'PROMEDIOS':<20} {'costo':>8} {'visitados':>10} {'tiempo':>9}")
    for nombre, (costo, visitados, tiempo) in acumulados.items():
        total = len(pares)
        print(f"{nombre:<20} {costo / total:>8.1f} {visitados / total:>10.1f} "
              f"{tiempo / total:>7.3f}ms")


def main() -> None:
    experimento_hashing()
    experimento_heap()
    experimento_ordenamiento()
    experimento_grafos()


if __name__ == "__main__":
    main()
