from dataclasses import dataclass


def _es_primo(numero: int) -> bool:
    if numero < 2:
        return False
    if numero % 2 == 0:
        return numero == 2
    divisor = 3
    while divisor * divisor <= numero:
        if numero % divisor == 0:
            return False
        divisor += 2
    return True


def _siguiente_primo(numero: int) -> int:
    while not _es_primo(numero):
        numero += 1
    return numero


@dataclass
class EstadisticasTabla:
    elementos: int
    capacidad: int
    factor_carga: float
    colisiones: int
    buckets_usados: int
    bucket_maximo: int


class TablaHash:
    """Tabla hash propia con encadenamiento separado (no usa dict)

    Los buckets se guardan en un arreglo y cada bucket es una lista de
    pares [clave, valor] La funcion de dispersion es djb2 y la tabla se
    redimensiona al siguiente primo cuando el factor de carga supera 0.75
    """

    FACTOR_CARGA_MAXIMO = 0.75

    def __init__(self, capacidad: int = 17) -> None:
        self._buckets: list[list[list]] = [[] for _ in range(_siguiente_primo(capacidad))]
        self._elementos = 0
        self._colisiones = 0

    def __len__(self) -> int:
        return self._elementos

    def __contains__(self, clave: str) -> bool:
        return self.buscar(clave) is not None

    @property
    def factor_carga(self) -> float:
        return self._elementos / len(self._buckets)

    def _indice(self, clave: str) -> int:
        """Funcion de dispersion djb2 reducida modulo capacidad O(len(clave))"""
        codigo = 5381
        for caracter in clave:
            codigo = (codigo * 33 + ord(caracter)) & 0xFFFFFFFF
        return codigo % len(self._buckets)

    def insertar(self, clave: str, valor) -> None:
        """Inserta o reemplaza el valor asociado a la clave O(1) promedio"""
        bucket = self._buckets[self._indice(clave)]
        for entrada in bucket:
            if entrada[0] == clave:
                entrada[1] = valor
                return
        if bucket:
            self._colisiones += 1
        bucket.append([clave, valor])
        self._elementos += 1
        if self.factor_carga > self.FACTOR_CARGA_MAXIMO:
            self._redimensionar()

    def buscar(self, clave: str):
        """Valor asociado a la clave o None si no existe O(1) promedio"""
        for entrada_clave, valor in self._buckets[self._indice(clave)]:
            if entrada_clave == clave:
                return valor
        return None

    def actualizar(self, clave: str, valor) -> bool:
        """Reemplaza el valor de una clave existente O(1) promedio"""
        for entrada in self._buckets[self._indice(clave)]:
            if entrada[0] == clave:
                entrada[1] = valor
                return True
        return False

    def eliminar(self, clave: str) -> bool:
        """Elimina la entrada asociada a la clave O(1) promedio"""
        bucket = self._buckets[self._indice(clave)]
        for posicion, entrada in enumerate(bucket):
            if entrada[0] == clave:
                bucket.pop(posicion)
                self._elementos -= 1
                return True
        return False

    def entradas(self) -> list[tuple[str, object]]:
        """Todos los pares (clave, valor) O(n + capacidad)"""
        return [(clave, valor) for bucket in self._buckets for clave, valor in bucket]

    def valores(self) -> list:
        return [valor for _, valor in self.entradas()]

    def estadisticas(self) -> EstadisticasTabla:
        """Metricas de ocupacion de la tabla O(capacidad)"""
        tamanios = [len(bucket) for bucket in self._buckets if bucket]
        return EstadisticasTabla(
            elementos=self._elementos,
            capacidad=len(self._buckets),
            factor_carga=self.factor_carga,
            colisiones=self._colisiones,
            buckets_usados=len(tamanios),
            bucket_maximo=max(tamanios, default=0),
        )

    def _redimensionar(self) -> None:
        """Duplica la capacidad al siguiente primo y redispersa todo O(n)"""
        entradas = self.entradas()
        self._buckets = [[] for _ in range(_siguiente_primo(len(self._buckets) * 2))]
        for clave, valor in entradas:
            self._buckets[self._indice(clave)].append([clave, valor])
