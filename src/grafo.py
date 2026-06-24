import csv
import math
from typing import Dict, List, Optional, Tuple

from .problema import Problema


class ProblemaGrafo(Problema):
    def __init__(
        self,
        adyacencia: Dict[str, List[Tuple[str, float]]],
        inicio: str,
        objetivo: str,
        coordenadas: Optional[Dict[str, Tuple[float, float]]] = None,
    ):
        self.adyacencia = adyacencia
        self.inicio = inicio
        self.objetivo = objetivo
        # coordenadas (x, y) opcionales que sirven para dibujar el grafo y para implementar la heurística en A*
        self.coordenadas = coordenadas or {}

    def estado_inicial(self) -> str:
        return self.inicio

    def es_objetivo(self, estado: str) -> bool:
        return estado == self.objetivo

    def vecinos(self, estado: str) -> List[Tuple[str, float]]:
        # Ordenar por nombre del vecino, para que el recorrido sea reproducible
        return sorted(self.adyacencia.get(estado, []), key=lambda par: par[0])

    def heuristica(self, estado: str) -> float:
        #Distancia euclidiana hasta el objetivo usando las coordenadas.
        #A* se comporta como UCS si no hay coords (y devuelve 0).
        if estado in self.coordenadas and self.objetivo in self.coordenadas:
            x1, y1 = self.coordenadas[estado]
            x2, y2 = self.coordenadas[self.objetivo]
            return math.hypot(x1 - x2, y1 - y2)
        return 0.0

    def nodos(self) -> List[str]:
        return sorted(self.adyacencia.keys())



def _filas_utiles(ruta: str) -> List[List[str]]:
    with open(ruta, newline="", encoding="utf-8") as f:
        filas = []
        for fila in csv.reader(f):
            if not fila:
                continue
            if fila[0].strip().startswith("#"):
                continue
            filas.append(fila)
    return filas


def cargar_lista_adyacencia(ruta: str, dirigido: bool = False) -> Dict[str, List[Tuple[str, float]]]:
    """
    CSV es [origen,destino,costo]
    Si falta el costo, fallback a 1
    """
    adyacencia: Dict[str, List[Tuple[str, float]]] = {}
    for fila in _filas_utiles(ruta):
        origen = fila[0].strip()
        destino = fila[1].strip()
        costo = float(fila[2]) if len(fila) > 2 and fila[2].strip() else 1.0
        adyacencia.setdefault(origen, []).append((destino, costo))
        adyacencia.setdefault(destino, [])           # asegura que el destino exista como nodo
        if not dirigido:
            adyacencia[destino].append((origen, costo))
    return adyacencia


def cargar_matriz_adyacencia(ruta: str) -> Dict[str, List[Tuple[str, float]]]:
    """
    CSV con formato de tabla NxN. La primera fila y la primera columna son los nombres de los nodos. Cada celda es el costo de la arista.
    Ejemplo de tabla:
        ,A,B,C
        A,0,2,4
        B,2,0,1
        C,4,1,0
    """
    filas = _filas_utiles(ruta)
    encabezado = [c.strip() for c in filas[0][1:]]
    adyacencia: Dict[str, List[Tuple[str, float]]] = {n: [] for n in encabezado}
    for fila in filas[1:]:
        nodo = fila[0].strip()
        for j, val in enumerate(fila[1:]):
            val = val.strip()
            if val and val not in ("0", "inf"):
                adyacencia[nodo].append((encabezado[j], float(val)))
    return adyacencia


def cargar_coordenadas(ruta: str) -> Dict[str, Tuple[float, float]]:
    #CSV con formato:  nodo,x,y  (coords opcionales para habilitar la heurística de A*)
    coords: Dict[str, Tuple[float, float]] = {}
    for fila in _filas_utiles(ruta):
        nodo = fila[0].strip()
        coords[nodo] = (float(fila[1]), float(fila[2]))
    return coords
