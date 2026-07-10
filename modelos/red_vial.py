import csv
import math

VELOCIDAD_MAXIMA_KMH = 60.0


class RoadNetwork:
    """ADT que modela la red vial como un grafo ponderado no dirigido

    Usa listas de adyacencia: los nodos son intersecciones o localidades y
    el peso de cada arista es el tiempo de desplazamiento en minutos
    """

    def __init__(self) -> None:
        self._adyacencia: dict[str, list[tuple[str, float]]] = {}
        self._coordenadas: dict[str, tuple[float, float]] = {}
        self._numero_aristas = 0

    def agregar_nodo(self, nodo: str, x: float | None = None, y: float | None = None) -> None:
        """O(1)"""
        if nodo not in self._adyacencia:
            self._adyacencia[nodo] = []
        if x is not None and y is not None:
            self._coordenadas[nodo] = (float(x), float(y))

    def agregar_arista(self, origen: str, destino: str, peso: float,
                       bidireccional: bool = True) -> None:
        """O(1)"""
        self.agregar_nodo(origen)
        self.agregar_nodo(destino)
        self._adyacencia[origen].append((destino, float(peso)))
        if bidireccional:
            self._adyacencia[destino].append((origen, float(peso)))
        self._numero_aristas += 1

    def vecinos(self, nodo: str) -> list[tuple[str, float]]:
        """Pares (nodo_vecino, peso) O(1) para obtener la lista"""
        return self._adyacencia.get(nodo, [])

    def peso(self, origen: str, destino: str) -> float | None:
        """Peso de la arista directa origen-destino O(grado(origen))"""
        for vecino, peso in self.vecinos(origen):
            if vecino == destino:
                return peso
        return None

    def existe_nodo(self, nodo: str) -> bool:
        return nodo in self._adyacencia

    def nodos(self) -> list[str]:
        return list(self._adyacencia)

    def coordenadas(self, nodo: str) -> tuple[float, float] | None:
        return self._coordenadas.get(nodo)

    def distancia_euclidiana(self, origen: str, destino: str) -> float | None:
        """Distancia en linea recta en km entre dos nodos con coordenadas O(1)"""
        punto_origen = self._coordenadas.get(origen)
        punto_destino = self._coordenadas.get(destino)
        if punto_origen is None or punto_destino is None:
            return None
        return math.dist(punto_origen, punto_destino)

    @property
    def numero_nodos(self) -> int:
        return len(self._adyacencia)

    @property
    def numero_aristas(self) -> int:
        return self._numero_aristas

    @classmethod
    def cargar_desde_csv(cls, ruta_nodos: str, ruta_aristas: str) -> "RoadNetwork":
        """Construye la red desde nodos.csv (id,x,y) y aristas.csv (origen,destino,tiempo_minutos)"""
        red = cls()
        with open(ruta_nodos, newline="", encoding="utf-8") as archivo:
            for fila in csv.DictReader(archivo):
                red.agregar_nodo(fila["id"], float(fila["x"]), float(fila["y"]))
        with open(ruta_aristas, newline="", encoding="utf-8") as archivo:
            for fila in csv.DictReader(archivo):
                red.agregar_arista(fila["origen"], fila["destino"], float(fila["tiempo_minutos"]))
        return red
