"""
Definición de una interface común para que usen todos los algoritmos de búsqueda.

La idea central del laboratorio de éstos algoritmos de búsqueda es que operen de forma agnóstica al problema 
Para hacer ésta abstracción, los algoritmos solo necesitan saber:
Cuál es el estado inicial?: estado_inicial()
Este estado es el objetivo?: es_objetivo(estado)
A qué estados puedo moverme y a qué costo desde este estado?: vecinos(estado)
Qué tan lejos creo que estoy del objetivo? (Solo para A*): heuristica(estado)

De ésta forma, cualquier clase que implemente estas funciones (respondería las preguntas) 
puede ser resuelta por los 4 algoritmos de búsqueda. Asi evitamos escribir BFS dos veces por ejemplo (uno para grafo y otro para laberinto)
Ademas siempre es buena práctica abstraer (era mi ejercicio favorito cuando empecé la carrera)
"""

from dataclasses import dataclass, field
from typing import Any, List, Tuple


class Problema:
    """Interface de clases que usaremos con los algoritmos"""

    def estado_inicial(self) -> Any:
        """Devuelve el estado desde donde empieza la búsqueda"""
        raise NotImplementedError

    def es_objetivo(self, estado: Any) -> bool:
        """Devuelve True si estado es la meta"""
        raise NotImplementedError

    def vecinos(self, estado: Any) -> List[Tuple[Any, float]]:
        """
        Devuelve una lista de pares (estado_vecino, costo_del_paso),
        el costo_del_paso es el costo de moverse desde estado al vecino
        """
        raise NotImplementedError

    def heuristica(self, estado: Any) -> float:
        """
        Estimación optimista del costo que falta desde estado hasta el objetivo
        Por defecto devuelve 0 porque solo la usa A*.
        """
        return 0.0


@dataclass
class Resultado:
    """
    Empaqueta todo lo que un algoritmo produce, para poder reportarlo y
    visualizarlo de forma uniforme (para las evidencias que requiere el lab)
    """
    orden_visita: List[Any] = field(default_factory=list)  # estados en el orden en que se EXPANDIERON
    camino: List[Any] = field(default_factory=list)        # ruta final inicio -> objetivo (arreglo vacío [] si no hay)
    costo: float = float("inf")                            # costo total acumulado del camino
    exito: bool = False                                    # Booleano de si se encontró el objetivo

    @property
    def num_visitados(self) -> int:
        """Cantidad de nodos expandidos (esfuerzo del algoritmo)"""
        return len(self.orden_visita)

    @property
    def longitud_camino(self) -> int:
        """Cantidad de nodos en el camino (longitud en aristas = esto - 1)"""
        return len(self.camino)
