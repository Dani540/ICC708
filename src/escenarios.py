"""
Escenarios predefinidos hardcodeados para correr el programa sin depender de
archivos. Los mismos datos están también en data/*.csv para probar leyendolos

El grafo está hecho a propósito para que los 4 algoritmos den resultados
distintos y se note la diferencia entre ellos
"""
from typing import Dict, List, Tuple

from .grafo import ProblemaGrafo
from .laberinto import ProblemaLaberinto

# grafo no dirigido y con costos. Coordenadas para dibujarlo
# y para que A* tenga heurística de distancia en línea recta.
ARISTAS_GRAFO: List[Tuple[str, str, float]] = [
    ("A", "B", 2),
    ("A", "C", 4),
    ("B", "C", 1),
    ("B", "D", 7),
    ("C", "D", 8),
    ("C", "F", 5),
    ("D", "E", 3),
    ("D", "G", 2),
    ("F", "E", 2),
    ("E", "G", 6),
]

COORDS_GRAFO: Dict[str, Tuple[float, float]] = {
    "A": (0, 0),
    "B": (2, 1),
    "C": (1, 3),
    "D": (4, 2),
    "E": (5, 4),
    "F": (4, 5),
    "G": (6, 1),
}


def _construir_adyacencia(aristas, dirigido=False):
    adyacencia: Dict[str, List[Tuple[str, float]]] = {}
    for origen, destino, costo in aristas:
        adyacencia.setdefault(origen, []).append((destino, float(costo)))
        adyacencia.setdefault(destino, [])
        if not dirigido:
            adyacencia[destino].append((origen, float(costo)))
    return adyacencia


def grafo_predefinido(inicio: str = "A", objetivo: str = "E") -> ProblemaGrafo:
    adyacencia = _construir_adyacencia(ARISTAS_GRAFO)
    return ProblemaGrafo(adyacencia, inicio, objetivo, COORDS_GRAFO)


# laberinto con 0 = libre, 1 = barrera.
# 10 filas x 15 columnas. Inicio arriba-izquierda, objetivo abajo-derecha.
LABERINTO: List[List[int]] = [
    [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0],
    [1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 0, 1, 0, 1, 0],
    [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0],
    [0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0],
    [1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0],
    [0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0],
    [0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0],
    [0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 1, 1, 1, 0, 0, 0, 1, 1, 1, 0, 0, 0],
]


def laberinto_predefinido(inicio=(0, 0), objetivo=(9, 14)) -> ProblemaLaberinto:
    return ProblemaLaberinto(LABERINTO, inicio, objetivo)
