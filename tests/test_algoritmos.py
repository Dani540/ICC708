"""
Pruebas automáticas de los 4 algoritmos :D

Se ejecutan con:
    python -m pytest tests/        (si tiene pytest)
    python tests/test_algoritmos.py   (si no tiene pytest, corre las aserciones a mano)

Verifican las propiedades teoricaws de cada algoritmo:
- UCS y A* siempre devuelven el costo óptimo
- BFS devuelve el camino con menos aristas (pero no necesariamente el más barato)
- Todos encuentran un camino cuando existe y ninguno cuando no existe (no vaya a ser que alguno encuentre un camino si se supone que el camino no existe jaja)
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.algoritmos import bfs, dfs, ucs, a_estrella, comparar_algoritmos
from src.escenarios import grafo_predefinido, laberinto_predefinido
from src.grafo import ProblemaGrafo
from src.laberinto import ProblemaLaberinto


def _camino_valido(problema, camino, inicio, objetivo):
    """Comprueba que el camino sea conexo y empiece/termine donde debe"""
    if not camino:
        return False
    if camino[0] != inicio or camino[-1] != objetivo:
        return False
    for a, b in zip(camino, camino[1:]):
        vecinos = [v for v, _ in problema.vecinos(a)]
        if b not in vecinos:
            return False
    return True


def test_grafo_optimalidad():
    g = grafo_predefinido("A", "E")
    r = comparar_algoritmos(g)
    # UCS y A* deben dar el costo óptimo (10 en este grafo)
    assert r["UCS"].costo == 10
    assert r["A*"].costo == 10
    # A* nunca debe ser peor que UCS en costo
    assert r["A*"].costo == r["UCS"].costo
    # BFS minimiza aristas: 3 saltos (4 nodos), aunque cueste más (12)
    assert r["BFS"].longitud_camino == 4
    assert r["BFS"].costo >= r["UCS"].costo
    # Todos encuentran un camino válido
    for nombre, res in r.items():
        assert res.exito
        assert _camino_valido(g, res.camino, "A", "E"), nombre


def test_laberinto_optimalidad():
    lab = laberinto_predefinido((0, 0), (9, 14))
    r = comparar_algoritmos(lab)
    # Con costos uniformes, BFS, UCS y A* dan el mismo costo óptimo
    assert r["BFS"].costo == r["UCS"].costo == r["A*"].costo
    # A* explora <= que UCS, ya que la heurística lo guía
    assert r["A*"].num_visitados <= r["UCS"].num_visitados
    for nombre, res in r.items():
        assert res.exito
        assert _camino_valido(lab, res.camino, (0, 0), (9, 14)), nombre


def test_sin_solucion():
    # Objetivo encerrado por barreras: nadie debe encontrar camino
    grid = [
        [0, 1, 0],
        [1, 1, 0],
        [0, 0, 0],
    ]
    lab = ProblemaLaberinto(grid, (0, 0), (0, 2))
    for fn in (bfs, dfs, ucs, a_estrella):
        res = fn(lab)
        assert not res.exito
        assert res.camino == []


def test_inicio_igual_objetivo():
    g = grafo_predefinido("A", "A")
    for fn in (bfs, dfs, ucs, a_estrella):
        res = fn(g)
        assert res.exito
        assert res.camino == ["A"]
        assert res.costo == 0


def test_grafo_desde_csv_coincide():
    """El grafo leído desde CSV debe dar el mismo resultado que el hardcodeado (sino el lector estaría funcionando mal)"""
    from src.grafo import cargar_lista_adyacencia, cargar_coordenadas
    base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    ady = cargar_lista_adyacencia(os.path.join(base, "data", "grafo_lista.csv"))
    coords = cargar_coordenadas(os.path.join(base, "data", "grafo_coords.csv"))
    g = ProblemaGrafo(ady, "A", "E", coords)
    assert ucs(g).costo == 10
    assert a_estrella(g).costo == 10


if __name__ == "__main__":
    pruebas = [v for k, v in sorted(globals().items()) if k.startswith("test_")]
    fallidas = 0
    for prueba in pruebas:
        try:
            prueba()
            print(f"[OK]   {prueba.__name__}")
        except AssertionError as e:
            fallidas += 1
            print(f"[FALLA] {prueba.__name__}: {e}")
    print(f"\n{len(pruebas) - fallidas}/{len(pruebas)} pruebas pasaron.")
    sys.exit(1 if fallidas else 0)
