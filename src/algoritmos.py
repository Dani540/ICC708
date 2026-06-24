"""
Los 4 algoritmos de búsqueda escritos una sola vez para cualquier problema.

Todos siguen lo de búsqueda en grafo:
    frontera: estados descubiertos pero todavía no explorados
    explorados: estados ya explorados, para no repetir trabajo ni ciclar
    padre: de quién venimos (para reconstruir el camino al final jeje)

Lo que cambia entre algoritmos es la estructura de la frontera:
    BFS: Cola (FIFO) -> explora por NIVELES
    DFS: Pila (LIFO) -> explora en PROFUNDIDAD
    UCS: Cola de prioridad por g(n), es decir, el costo acumulado
    A*: Cola de prioridad por f(n)=g(n)+h(n) (costo acumulado + heurística)

g(n) es el costo real acumulado desde el inicio hasta n.
h(n) es la estimación del costo que falta de n al objetivo (la heurística, la linea euclidiana).
"""

import heapq
import itertools
from collections import deque
from typing import Any, Callable, Dict, List

from .problema import Problema, Resultado


# Utilidad común para reconstruir el camino siguiendo los punteros "padre",
# va del objetivo hacia atrás (hasta el inicio) y luego invierte.
def _reconstruir_camino(padre: Dict[Any, Any], objetivo: Any) -> List[Any]:
    camino = [objetivo]
    while padre[camino[-1]] is not None:
        camino.append(padre[camino[-1]])
    camino.reverse()
    return camino

def bfs(problema: Problema) -> Resultado:
    """
    BFS - Breadth-First Search o busqueda en anchura:

    Usa una cola, por lo que explora todos los de distancia 1, luego todos los de distancia 2, etc.
    Al final encuentra el camino con menos aristas; óptimo solo si todos los costos son iguales pero 
    no encuentra necesariamente el camino de menor costo.
    """
    inicio = problema.estado_inicial()
    frontera = deque([(inicio, None, 0.0)])   # (estado, padre, g)
    descubierto = {inicio}                    # marcar al encolar para evitar duplicados
    padre: Dict[Any, Any] = {}
    orden_visita: List[Any] = []

    while frontera:
        estado, p, g = frontera.popleft()     # FIFO: sale el más antiguo
        padre[estado] = p
        orden_visita.append(estado)

        if problema.es_objetivo(estado):
            return Resultado(orden_visita, _reconstruir_camino(padre, estado), g, True)

        for vecino, costo in problema.vecinos(estado):
            if vecino not in descubierto:
                descubierto.add(vecino)
                frontera.append((vecino, estado, g + costo))

    return Resultado(orden_visita, [], float("inf"), False)

def dfs(problema: Problema) -> Resultado:
    """
    DFS - Depth-First Search (búsqueda en profundidad):

    Usa una pila, así que se hunde por una rama hasta el fondo antes de retroceder.
    Es más rápido y usa poca memoria, pero el camino que encuentra no parece ser ni
    el más corto ni el más barato jaja
    """
    inicio = problema.estado_inicial()
    frontera = [(inicio, None, 0.0)]           # pila: (estado, padre, g)
    explorados = set()                         # marcar al expandir (al sacar)
    padre: Dict[Any, Any] = {}
    orden_visita: List[Any] = []

    while frontera:
        estado, p, g = frontera.pop()          # LIFO: sale el más reciente
        if estado in explorados:               # pudo haber entrado varias veces asi que lo saltamos
            continue
        explorados.add(estado)
        padre[estado] = p
        orden_visita.append(estado)

        if problema.es_objetivo(estado):
            return Resultado(orden_visita, _reconstruir_camino(padre, estado), g, True)

        # Apilamos en orden inverso porque la pila los invierte,
        # para que los vecinos se exploren en el orden natural en que vienen en la lista
        for vecino, costo in reversed(problema.vecinos(estado)):
            if vecino not in explorados:
                frontera.append((vecino, estado, g + costo))

    return Resultado(orden_visita, [], float("inf"), False)


# Plantilla común para UCS y A* (ambos usan una cola)
def _busqueda_con_prioridad(
    problema: Problema,
    prioridad: Callable[[float, float], float],
) -> Resultado:
    """
    prioridad(g, h) decide qué nodo sale primero del heap:
    si UCS: prioridad = g, solo costo acumulado
    si A*: prioridad = g + h, costo acumulado + heurística

    Detallitos:
    - Usar un contador para empates de prioridad, así gana el que entró primero
    - La variable mejor_g guarda el menor costo conocido para llegar a cada estado; Solo
      se reinserta un vecino si encontramos un camino más barato hacia éste (la gracia de usar Dijkstra/A*)
    """
    inicio = problema.estado_inicial()
    contador = itertools.count() # desempate FIFO estable
    g0 = 0.0
    h0 = problema.heuristica(inicio)

    # cada entrada del heap: (prioridad, orden_de_inserción, estado, padre, g)
    frontera = [(prioridad(g0, h0), next(contador), inicio, None, g0)]
    mejor_g: Dict[Any, float] = {inicio: 0.0}
    explorados = set()
    padre: Dict[Any, Any] = {}
    orden_visita: List[Any] = []

    while frontera:
        _, _, estado, p, g = heapq.heappop(frontera) # sale el de menor prioridad
        if estado in explorados: # entrada obsoleta: ignorar
            continue
        explorados.add(estado)
        padre[estado] = p
        orden_visita.append(estado)

        if problema.es_objetivo(estado):
            return Resultado(orden_visita, _reconstruir_camino(padre, estado), g, True)

        for vecino, costo in problema.vecinos(estado):
            if vecino in explorados:
                continue
            nuevo_g = g + costo
            # Primera vez que se visita o si llego por un camino más barato
            if vecino not in mejor_g or nuevo_g < mejor_g[vecino]:
                mejor_g[vecino] = nuevo_g
                h = problema.heuristica(vecino)
                heapq.heappush(
                    frontera,
                    (prioridad(nuevo_g, h), next(contador), vecino, estado, nuevo_g),
                )

    return Resultado(orden_visita, [], float("inf"), False)

def ucs(problema: Problema) -> Resultado:
    """
    UCS  -  Uniform Cost Search (búsqueda de costo uniforme = Dijkstra)
    
    Expande siempre el nodo de menor costo acumulado g(n)
    Así garantiza el camino de menor costo total, el camino óptimo"""
    return _busqueda_con_prioridad(problema, prioridad=lambda g, h: g)

def a_estrella(problema: Problema) -> Resultado:
    """
    A* - A estrella

    Expande el nodo de menor f(n) = g(n) + h(n).
    Lo mismo que UCS pero guiado por la heurística añadida hacia el objetivo, 
    encuentra el camino óptimo visitando menos nodos
    """
    return _busqueda_con_prioridad(problema, prioridad=lambda g, h: g + h)

# Registro de algoritmos (para los menús y la comparación automática)
ALGORITMOS: Dict[str, Callable[[Problema], Resultado]] = {
    "BFS": bfs,
    "DFS": dfs,
    "UCS": ucs,
    "A*": a_estrella,
}

def comparar_algoritmos(problema: Problema) -> Dict[str, Resultado]:
    """Corre los 4 algoritmos sobre el mismo problema y devuelve sus resultados."""
    return {nombre: fn(problema) for nombre, fn in ALGORITMOS.items()}
