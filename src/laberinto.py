"""
Escenario 2: búsqueda en un LABERINTO representado como matriz.

    0 = celda libre
    1 = barrera   

Un "estado" es una posición (fila, columna). Desde una celda libre se puede
mover en 4 direcciones (arriba, abajo, izquierda, derecha), cada movimiento
cuesta 1. La heurística natural es la DISTANCIA MANHATTAN al objetivo.
"""

import csv
from typing import List, Tuple

from .problema import Problema

Pos = Tuple[int, int]


class ProblemaLaberinto(Problema):
    # Orden de movimientos: Arriba, Abajo, Izquierda, Derecha.
    MOVIMIENTOS = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    def __init__(self, grid: List[List[int]], inicio: Pos, objetivo: Pos):
        self.grid = grid
        self.filas = len(grid)
        self.cols = len(grid[0]) if grid else 0
        self.inicio = inicio
        self.objetivo = objetivo
        self._validar()

    def _validar(self) -> None:
        for nombre, (f, c) in (("inicio", self.inicio), ("objetivo", self.objetivo)):
            if not (0 <= f < self.filas and 0 <= c < self.cols):
                raise ValueError(f"La posición {nombre} {(f, c)} está fuera del laberinto.")
            if self.grid[f][c] != 0:
                raise ValueError(f"La posición {nombre} {(f, c)} cae sobre una barrera (1).")

    def _libre(self, f: int, c: int) -> bool:
        return 0 <= f < self.filas and 0 <= c < self.cols and self.grid[f][c] == 0

    # --- Interfaz Problema -------------------------------------------------
    def estado_inicial(self) -> Pos:
        return self.inicio

    def es_objetivo(self, estado: Pos) -> bool:
        return estado == self.objetivo

    def vecinos(self, estado: Pos) -> List[Tuple[Pos, float]]:
        f, c = estado
        resultado = []
        for df, dc in self.MOVIMIENTOS:
            nf, nc = f + df, c + dc
            if self._libre(nf, nc):
                resultado.append(((nf, nc), 1.0))   # cada paso cuesta 1
        return resultado

    def heuristica(self, estado: Pos) -> float:
        """Distancia Manhattan: |df| + |dc|. Admisible porque solo nos movemos
        en horizontal/vertical con costo 1 (nunca sobreestima el costo real)."""
        f, c = estado
        fo, co = self.objetivo
        return abs(f - fo) + abs(c - co)


def cargar_laberinto(ruta: str) -> List[List[int]]:
    """Lee un CSV de 0 y 1 (ignora filas vacías y comentarios con '#')."""
    grid: List[List[int]] = []
    with open(ruta, newline="", encoding="utf-8") as f:
        for fila in csv.reader(f):
            if not fila or fila[0].strip().startswith("#"):
                continue
            grid.append([int(x) for x in fila if x.strip() != ""])
    return grid
