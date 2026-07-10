import math
from collections import deque
from dataclasses import dataclass

from estructuras.heap import MinHeap
from modelos.red_vial import VELOCIDAD_MAXIMA_KMH, RoadNetwork


@dataclass
class ResultadoBusqueda:
    """Resultado de una busqueda de ruta sobre la red vial"""

    ruta: list[str]
    costo: float
    nodos_visitados: list[str]

    @property
    def encontrada(self) -> bool:
        return bool(self.ruta)

    @property
    def tramos(self) -> int:
        return max(len(self.ruta) - 1, 0)


def bfs(red: RoadNetwork, origen: str, destino: str) -> ResultadoBusqueda:
    """Busqueda en anchura: ruta con menos tramos, ignora los pesos O(V + E)"""
    padres = {origen: None}
    cola = deque([origen])
    visitados = []
    while cola:
        actual = cola.popleft()
        visitados.append(actual)
        if actual == destino:
            ruta = _reconstruir_ruta(padres, destino)
            return ResultadoBusqueda(ruta, _costo_de_ruta(red, ruta), visitados)
        for vecino, _ in red.vecinos(actual):
            if vecino not in padres:
                padres[vecino] = actual
                cola.append(vecino)
    return ResultadoBusqueda([], math.inf, visitados)


def dijkstra(red: RoadNetwork, origen: str, destino: str) -> ResultadoBusqueda:
    """Busqueda de costo uniforme (UCS): ruta de costo minimo O((V + E) log V)"""
    return _busqueda_de_costo_minimo(red, origen, destino, _sin_heuristica)


def a_estrella(red: RoadNetwork, origen: str, destino: str) -> ResultadoBusqueda:
    """A*: Dijkstra guiado por una heuristica euclidiana admisible"""

    def heuristica(nodo: str) -> float:
        distancia = red.distancia_euclidiana(nodo, destino)
        if distancia is None:
            return 0.0
        return distancia / VELOCIDAD_MAXIMA_KMH * 60.0

    return _busqueda_de_costo_minimo(red, origen, destino, heuristica)


def _sin_heuristica(nodo: str) -> float:
    return 0.0


def _busqueda_de_costo_minimo(red: RoadNetwork, origen: str, destino: str,
                              heuristica) -> ResultadoBusqueda:
    """Motor comun de UCS y A*: expande siempre el nodo de menor costo + heuristica"""
    frontera = MinHeap()
    frontera.insertar(heuristica(origen), (0.0, origen))
    padres: dict[str, str | None] = {origen: None}
    costos = {origen: 0.0}
    expandidos: set[str] = set()
    visitados = []
    while not frontera.esta_vacio():
        _, (costo, actual) = frontera.extraer_minimo()
        if actual in expandidos:
            continue
        expandidos.add(actual)
        visitados.append(actual)
        if actual == destino:
            return ResultadoBusqueda(_reconstruir_ruta(padres, destino), costo, visitados)
        for vecino, peso in red.vecinos(actual):
            nuevo_costo = costo + peso
            if vecino not in costos or nuevo_costo < costos[vecino]:
                costos[vecino] = nuevo_costo
                padres[vecino] = actual
                frontera.insertar(nuevo_costo + heuristica(vecino), (nuevo_costo, vecino))
    return ResultadoBusqueda([], math.inf, visitados)


def _reconstruir_ruta(padres: dict, destino: str) -> list[str]:
    ruta = []
    actual = destino
    while actual is not None:
        ruta.append(actual)
        actual = padres[actual]
    ruta.reverse()
    return ruta


def _costo_de_ruta(red: RoadNetwork, ruta: list[str]) -> float:
    total = 0.0
    for origen, destino in zip(ruta, ruta[1:]):
        peso = red.peso(origen, destino)
        if peso is None:
            return math.inf
        total += peso
    return total
