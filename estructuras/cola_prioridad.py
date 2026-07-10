from .heap import MinHeap
from .tabla_hash import TablaHash


class PriorityQueue:
    """Cola de prioridad maxima para incidentes, basada en un heap binario

    Cada entrada del arreglo es el par [prioridad, incidente] Una TablaHash
    propia mapea id de incidente -> indice en el arreglo, lo que permite
    actualizar prioridades en O(log n)
    """

    def __init__(self) -> None:
        self._datos: list[list] = []
        self._posiciones = TablaHash()

    def __len__(self) -> int:
        return len(self._datos)

    def esta_vacia(self) -> bool:
        return not self._datos

    def insertar(self, incidente, prioridad: float) -> None:
        """O(log n)"""
        self._datos.append([prioridad, incidente])
        self._posiciones.insertar(incidente.id, len(self._datos) - 1)
        self._flotar(len(self._datos) - 1)

    def extraer_mas_urgente(self) -> tuple[float, object]:
        """Extrae el par (prioridad, incidente) mas urgente O(log n)"""
        if not self._datos:
            raise IndexError("la cola de prioridad esta vacia")
        self._intercambiar(0, len(self._datos) - 1)
        prioridad, incidente = self._datos.pop()
        self._posiciones.eliminar(incidente.id)
        if self._datos:
            self._hundir(0)
        return prioridad, incidente

    def actualizar_prioridad(self, id_incidente: str, nueva_prioridad: float) -> bool:
        """Cambia la prioridad de un incidente y reordena el heap O(log n)"""
        indice = self._posiciones.buscar(id_incidente)
        if indice is None:
            return False
        prioridad_anterior = self._datos[indice][0]
        self._datos[indice][0] = nueva_prioridad
        if nueva_prioridad > prioridad_anterior:
            self._flotar(indice)
        else:
            self._hundir(indice)
        return True

    def top_k(self, cantidad: int) -> list[tuple[float, object]]:
        """Los k incidentes mas urgentes sin alterar la cola O(n log n)"""
        auxiliar = MinHeap()
        for prioridad, incidente in self._datos:
            auxiliar.insertar(-prioridad, incidente)
        resultado = []
        while len(resultado) < cantidad and not auxiliar.esta_vacio():
            prioridad_negada, incidente = auxiliar.extraer_minimo()
            resultado.append((-prioridad_negada, incidente))
        return resultado

    def _intercambiar(self, i: int, j: int) -> None:
        self._datos[i], self._datos[j] = self._datos[j], self._datos[i]
        self._posiciones.insertar(self._datos[i][1].id, i)
        self._posiciones.insertar(self._datos[j][1].id, j)

    def _flotar(self, indice: int) -> None:
        while indice > 0:
            padre = (indice - 1) // 2
            if self._datos[indice][0] <= self._datos[padre][0]:
                break
            self._intercambiar(indice, padre)
            indice = padre

    def _hundir(self, indice: int) -> None:
        total = len(self._datos)
        while True:
            mayor = indice
            for hijo in (2 * indice + 1, 2 * indice + 2):
                if hijo < total and self._datos[hijo][0] > self._datos[mayor][0]:
                    mayor = hijo
            if mayor == indice:
                break
            self._intercambiar(indice, mayor)
            indice = mayor
