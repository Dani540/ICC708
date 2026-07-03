# -*- coding: utf-8 -*-
"""Mochila 0/1 con programación dinámica bottom-up.

Partes A, B y C: tabla DP, reconstrucción de la solución e impresión.
"""

from dataclasses import dataclass
from typing import List


@dataclass
class Objeto:
    nombre: str
    peso: int
    valor: int


def construir_tabla_dp(objetos: List[Objeto], capacidad: int) -> List[List[int]]:
    """Devuelve la tabla dp para el problema knapsack 0/1."""
    n = len(objetos)
    W = capacidad
    dp = [[0] * (W + 1) for _ in range(n + 1)]

    for i in range(1, n + 1):
        peso_i = objetos[i - 1].peso
        valor_i = objetos[i - 1].valor
        for w in range(0, W + 1):
            dp[i][w] = dp[i - 1][w]
            if peso_i <= w:
                valor_incluyendo = dp[i - 1][w - peso_i] + valor_i
                if valor_incluyendo > dp[i][w]:
                    dp[i][w] = valor_incluyendo

    return dp


def reconstruir_solucion(dp: List[List[int]], objetos: List[Objeto],
                         capacidad: int) -> List[Objeto]:
    """Devuelve la lista de objetos que forman la solución óptima."""
    seleccionados: List[Objeto] = []
    w = capacidad

    for i in range(len(objetos), 0, -1):
        if dp[i][w] != dp[i - 1][w]:
            objeto_usado = objetos[i - 1]
            seleccionados.append(objeto_usado)
            w -= objeto_usado.peso

    seleccionados.reverse()
    return seleccionados


def imprimir_tabla_dp(dp: List[List[int]], objetos: List[Objeto]) -> None:
    """Imprime la tabla DP con encabezado de capacidades."""
    n = len(objetos)
    W = len(dp[0]) - 1

    encabezado = "  Objeto \\ w  |" + "".join(f"{w:4d}" for w in range(W + 1))
    print(encabezado)
    print("-" * len(encabezado))

    for i in range(n + 1):
        etiqueta = "(0) sin obj." if i == 0 else f"({i}) {objetos[i - 1].nombre}"
        fila = f"{etiqueta[:12]:<12} |" + "".join(f"{dp[i][w]:4d}" for w in range(W + 1))
        print(fila)


def resolver_mochila(objetos: List[Objeto], capacidad: int):
    """Resuelve el problema completo y devuelve dp, valor y selección."""
    dp = construir_tabla_dp(objetos, capacidad)
    valor_optimo = dp[len(objetos)][capacidad]
    seleccionados = reconstruir_solucion(dp, objetos, capacidad)
    peso_total = sum(o.peso for o in seleccionados)
    return dp, valor_optimo, seleccionados, peso_total


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
    print(" PROBLEMA DE LA MOCHILA 0/1  -  DATASET INICIAL DEL TALLER")
    print("=" * 70)
    print(f"Capacidad maxima del vehiculo: {capacidad} unidades\n")

    # Datos de entrada
    print(f"{'Recurso':<14}{'Peso':>6}{'Valor':>7}")
    print("-" * 27)
    for o in objetos:
        print(f"{o.nombre:<14}{o.peso:>6}{o.valor:>7}")

    dp, valor_optimo, seleccionados, peso_total = resolver_mochila(objetos, capacidad)

    print("\n" + "=" * 70)
    print(" PARTE C - TABLA DINAMICA (DP)")
    print("=" * 70)
    imprimir_tabla_dp(dp, objetos)

    print("\n" + "=" * 70)
    print(" PARTE A - RESULTADO")
    print("=" * 70)
    print(f"Valor maximo alcanzable (dp[N][W]) = {valor_optimo}")

    print("\n" + "=" * 70)
    print(" PARTE B - RECONSTRUCCION DE LA SOLUCION OPTIMA")
    print("=" * 70)
    print("Objetos seleccionados:")
    for o in seleccionados:
        print(f"   - {o.nombre:<14} (peso {o.peso}, valor {o.valor})")
    print(f"\nPeso total : {peso_total}  (capacidad {capacidad})")
    print(f"Valor total: {valor_optimo}")

    print("\n(Nota: el ejemplo del enunciado no es el óptimo real para este dataset.)")
