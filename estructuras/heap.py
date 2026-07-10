class MinHeap:
    """Monticulo binario de minimos sobre un arreglo dinamico

    Cada elemento se guarda como la tupla (prioridad, elemento) y las
    comparaciones se hacen unicamente sobre la prioridad
    """

    def __init__(self) -> None:
        self._datos: list[tuple[float, object]] = []

    def __len__(self) -> int:
        return len(self._datos)

    def esta_vacio(self) -> bool:
        return not self._datos

    def insertar(self, prioridad: float, elemento) -> None:
        """O(log n)"""
        self._datos.append((prioridad, elemento))
        self._flotar(len(self._datos) - 1)

    def extraer_minimo(self) -> tuple[float, object]:
        """Extrae la tupla (prioridad, elemento) con prioridad minima O(log n)"""
        if not self._datos:
            raise IndexError("el monticulo esta vacio")
        self._datos[0], self._datos[-1] = self._datos[-1], self._datos[0]
        prioridad, elemento = self._datos.pop()
        if self._datos:
            self._hundir(0)
        return prioridad, elemento

    def minimo(self) -> tuple[float, object]:
        """O(1)"""
        if not self._datos:
            raise IndexError("el monticulo esta vacio")
        return self._datos[0]

    def _flotar(self, indice: int) -> None:
        while indice > 0:
            padre = (indice - 1) // 2
            if self._datos[indice][0] >= self._datos[padre][0]:
                break
            self._datos[indice], self._datos[padre] = self._datos[padre], self._datos[indice]
            indice = padre

    def _hundir(self, indice: int) -> None:
        total = len(self._datos)
        while True:
            menor = indice
            for hijo in (2 * indice + 1, 2 * indice + 2):
                if hijo < total and self._datos[hijo][0] < self._datos[menor][0]:
                    menor = hijo
            if menor == indice:
                break
            self._datos[indice], self._datos[menor] = self._datos[menor], self._datos[indice]
            indice = menor
