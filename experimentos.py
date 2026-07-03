# -*- coding: utf-8 -*-
"""Experimentos para analizar tiempo y memoria de los enfoques knapsack."""

import random
import time
import tracemalloc
from typing import List

from mochila_dp import Objeto, construir_tabla_dp, reconstruir_solucion
from mochila_memoization import resolver_mochila_topdown


random.seed(42)


def generar_objetos(n: int, peso_max: int = 50, valor_max: int = 100) -> List[Objeto]:
    """Genera n objetos con peso y valor aleatorios."""
    objetos = []
    for k in range(n):
        peso = random.randint(1, peso_max)
        valor = random.randint(1, valor_max)
        objetos.append(Objeto(f"Obj{k}", peso, valor))
    return objetos


def medir_bottomup(objetos: List[Objeto], capacidad: int, repeticiones: int = 3):
    """Mide el mejor tiempo de ejecución para el algoritmo bottom-up."""
    mejor_tiempo = float("inf")
    valor_optimo = 0
    for _ in range(repeticiones):
        inicio = time.perf_counter()
        dp = construir_tabla_dp(objetos, capacidad)
        fin = time.perf_counter()

        valor_optimo = dp[len(objetos)][capacidad]
        mejor_tiempo = min(mejor_tiempo, fin - inicio)
    return mejor_tiempo, valor_optimo


def experimento_variando_n(tamanos: List[int], capacidad: int = 1000):
    """Varia N con capacidad fija para medir tiempo."""
    print("=" * 88)
    print(" EXPERIMENTO 1 (PARTE D) - Variando el numero de objetos (capacidad W fija)")
    print("=" * 88)
    print(f"Capacidad fija W = {capacidad}\n")

    print(f"{'N objetos':>10} | {'Capacidad':>9} | {'Tiempo (s)':>12} | "
          f"{'Tamano tabla':>14} | {'Valor optimo':>12}")
    print("-" * 88)

    resultados = []
    for n in tamanos:
        objetos = generar_objetos(n)
        tiempo, valor = medir_bottomup(objetos, capacidad)
        tamano_tabla = (n + 1) * (capacidad + 1)

        print(f"{n:>10} | {capacidad:>9} | {tiempo:>12.6f} | "
              f"{tamano_tabla:>14,} | {valor:>12}")

        resultados.append({
            "n": n,
            "capacidad": capacidad,
            "tiempo": tiempo,
            "tamano_tabla": tamano_tabla,
            "valor": valor,
        })
    print()
    return resultados


def experimento_variando_w(capacidades: List[int], n: int = 100):
    """Varia W con N fijo para medir tiempo."""
    print("=" * 88)
    print(" EXPERIMENTO 2 (PARTE E) - Variando la capacidad (numero de objetos N fijo)")
    print("=" * 88)
    print(f"Numero de objetos fijo N = {n}\n")

    print(f"{'N objetos':>10} | {'Capacidad':>9} | {'Tiempo (s)':>12} | "
          f"{'Tamano tabla':>14} | {'Valor optimo':>12}")
    print("-" * 88)

    objetos = generar_objetos(n)

    resultados = []
    for capacidad in capacidades:
        tiempo, valor = medir_bottomup(objetos, capacidad)
        tamano_tabla = (n + 1) * (capacidad + 1)

        print(f"{n:>10} | {capacidad:>9} | {tiempo:>12.6f} | "
              f"{tamano_tabla:>14,} | {valor:>12}")

        resultados.append({
            "n": n,
            "capacidad": capacidad,
            "tiempo": tiempo,
            "tamano_tabla": tamano_tabla,
            "valor": valor,
        })
    print()
    return resultados


def experimento_comparar_enfoques(tamanos: List[int], capacidad: int = 1000):
    """Compara tiempo y memoria de bottom-up y top-down."""
    print("=" * 100)
    print(" EXPERIMENTO 3 (DESAFIO OPCIONAL) - Bottom-Up vs Top-Down (memoization)")
    print("=" * 100)
    print(f"Capacidad fija W = {capacidad}\n")

    print(f"{'N':>6} | {'Tiempo BU (s)':>14} | {'Tiempo TD (s)':>14} | "
          f"{'Memoria BU (KB)':>16} | {'Memoria TD (KB)':>16} | {'Mismo optimo':>12}")
    print("-" * 100)

    resultados = []
    for n in tamanos:
        objetos = generar_objetos(n)

        inicio = time.perf_counter()
        dp = construir_tabla_dp(objetos, capacidad)
        t_bu = time.perf_counter() - inicio
        valor_bu = dp[n][capacidad]

        tracemalloc.start()
        dp = construir_tabla_dp(objetos, capacidad)
        _, pico_bu = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        del dp

        inicio = time.perf_counter()
        valor_td, _, _, _ = resolver_mochila_topdown(objetos, capacidad)
        t_td = time.perf_counter() - inicio

        tracemalloc.start()
        resolver_mochila_topdown(objetos, capacidad)
        _, pico_td = tracemalloc.get_traced_memory()
        tracemalloc.stop()

        mismo = "SI" if valor_bu == valor_td else "NO (!)"

        print(f"{n:>6} | {t_bu:>14.6f} | {t_td:>14.6f} | "
              f"{pico_bu/1024:>16.1f} | {pico_td/1024:>16.1f} | {mismo:>12}")

        resultados.append({
            "n": n,
            "tiempo_bu": t_bu,
            "tiempo_td": t_td,
            "memoria_bu": pico_bu,
            "memoria_td": pico_td,
        })
    print()
    return resultados


def generar_graficos(res_n, res_w, res_cmp):
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
    except ImportError:
        print("[Aviso] matplotlib no esta instalado; se omiten los graficos.")
        print("        Instalalo con:  pip install matplotlib")
        return

    ns = [r["n"] for r in res_n]
    tiempos_n = [r["tiempo"] for r in res_n]
    plt.figure()
    plt.plot(ns, tiempos_n, "o-", color="tab:blue")
    plt.title("Tiempo de ejecucion vs Numero de objetos (W fijo)")
    plt.xlabel("Numero de objetos (N)")
    plt.ylabel("Tiempo (segundos)")
    plt.grid(True)
    plt.savefig("tiempo_vs_n.png", dpi=120, bbox_inches="tight")
    plt.close()

    ws = [r["capacidad"] for r in res_w]
    tiempos_w = [r["tiempo"] for r in res_w]
    plt.figure()
    plt.plot(ws, tiempos_w, "s-", color="tab:green")
    plt.title("Tiempo de ejecucion vs Capacidad (N fijo)")
    plt.xlabel("Capacidad de la mochila (W)")
    plt.ylabel("Tiempo (segundos)")
    plt.grid(True)
    plt.savefig("tiempo_vs_w.png", dpi=120, bbox_inches="tight")
    plt.close()

    ns_c = [r["n"] for r in res_cmp]
    t_bu = [r["tiempo_bu"] for r in res_cmp]
    t_td = [r["tiempo_td"] for r in res_cmp]
    plt.figure()
    plt.plot(ns_c, t_bu, "o-", label="Bottom-Up (tabla)")
    plt.plot(ns_c, t_td, "^-", label="Top-Down (memoization)")
    plt.title("Bottom-Up vs Top-Down")
    plt.xlabel("Numero de objetos (N)")
    plt.ylabel("Tiempo (segundos)")
    plt.legend()
    plt.grid(True)
    plt.savefig("bottomup_vs_topdown.png", dpi=120, bbox_inches="tight")
    plt.close()

    print("[OK] Graficos generados: tiempo_vs_n.png, tiempo_vs_w.png, bottomup_vs_topdown.png\n")


if __name__ == "__main__":
    tamanos = [10, 20, 50, 100, 200]
    res_n = experimento_variando_n(tamanos, capacidad=1000)

    capacidades = [250, 500, 1000, 2000, 4000, 8000]
    res_w = experimento_variando_w(capacidades, n=100)

    res_cmp = experimento_comparar_enfoques(tamanos, capacidad=1000)
    generar_graficos(res_n, res_w, res_cmp)

    print("Experimentos finalizados. Revisa la tabla y los graficos PNG generados.")
