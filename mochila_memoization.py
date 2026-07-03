# -*- coding: utf-8 -*-
"""Mochila 0/1 con memoización top-down.

Versión opcional para comparar con el enfoque bottom-up.
"""

import sys
from typing import List, Optional

from mochila_dp import Objeto

sys.setrecursionlimit(10000)


class MochilaMemoization:
    """Resuelve knapsack con top-down y memoización."""

    def __init__(self, objetos: List[Objeto], capacidad: int):
        self.objetos = objetos
        self.capacidad = capacidad
        self.n = len(objetos)

        self.memo: List[List[Optional[int]]] = [
            [None] * (capacidad + 1) for _ in range(self.n + 1)
        ]
        self.subproblemas_calculados = 0

    def resolver(self, i: int, w: int) -> int:
        """Devuelve el valor máximo para los primeros i objetos y capacidad w."""
        if i == 0:
            return 0

        if self.memo[i][w] is not None:
            return self.memo[i][w]

        self.subproblemas_calculados += 1
        peso_i = self.objetos[i - 1].peso
        valor_i = self.objetos[i - 1].valor

        mejor = self.resolver(i - 1, w)
        if peso_i <= w:
            incluyendo = self.resolver(i - 1, w - peso_i) + valor_i
            if incluyendo > mejor:
                mejor = incluyendo

        self.memo[i][w] = mejor
        return mejor

    def reconstruir(self) -> List[Objeto]:
        """Recupera los objetos usados en la solución óptima."""
        seleccionados: List[Objeto] = []
        w = self.capacidad
        for i in range(self.n, 0, -1):
            valor_con_i = self.resolver(i, w)
            valor_sin_i = self.resolver(i - 1, w)
            if valor_con_i != valor_sin_i:
                seleccionados.append(self.objetos[i - 1])
                w -= self.objetos[i - 1].peso
        seleccionados.reverse()
        return seleccionados


def resolver_mochila_topdown(objetos: List[Objeto], capacidad: int):
    """Devuelve valor, selección, peso y subproblemas calculados."""
    solver = MochilaMemoization(objetos, capacidad)
    valor_optimo = solver.resolver(len(objetos), capacidad)
    seleccionados = solver.reconstruir()
    peso_total = sum(o.peso for o in seleccionados)
    return valor_optimo, seleccionados, peso_total, solver.subproblemas_calculados


if __name__ == "__main__":
    objetos = [
        Objeto("Agua",          2,  6),
        Objeto("Medicamentos",  3,  8),
        Objeto("Alimentos",     4,  7),
        Objeto("Radio",         5, 10),
        Objeto("Generador",     9, 15),
        Objeto("Herramientas",  7, 12),
    ]
    capacidad = 20

    print("=" * 70)
    print(" MOCHILA 0/1 - VERSION TOP-DOWN (MEMOIZATION)  [Desafio opcional]")
    print("=" * 70)

    valor, seleccionados, peso, subproblemas = resolver_mochila_topdown(objetos, capacidad)

    print(f"Valor maximo alcanzable = {valor}")
    print("\nObjetos seleccionados:")
    for o in seleccionados:
        print(f"   - {o.nombre:<14} (peso {o.peso}, valor {o.valor})")
    print(f"\nPeso total : {peso}  (capacidad {capacidad})")
    print(f"Valor total: {valor}")

    total_celdas = (len(objetos) + 1) * (capacidad + 1)
    print(f"\nSubproblemas calculados por memoization: {subproblemas}")
    print(f"Celdas totales que llenaria bottom-up   : {total_celdas}")
    print("=> Top-Down puede calcular menos celdas al resolver solo los subproblemas necesarios.")
