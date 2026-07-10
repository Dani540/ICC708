from dataclasses import dataclass
from datetime import datetime
from enum import Enum


class EstadoIncidente(Enum):
    PENDIENTE = "pendiente"
    ASIGNADO = "asignado"
    ATENDIDO = "atendido"
    CANCELADO = "cancelado"


@dataclass
class Incident:
    """ADT que representa un incidente reportado durante una emergencia"""

    id: str
    ubicacion: str
    prioridad: int
    tipo: str
    timestamp: datetime
    estado: EstadoIncidente = EstadoIncidente.PENDIENTE

    def prioridad_efectiva(self, ahora: datetime) -> float:
        """Urgencia dinamica: prioridad base x (1 + horas de espera) O(1)"""
        horas_espera = max((ahora - self.timestamp).total_seconds() / 3600.0, 0.0)
        return self.prioridad * (1.0 + horas_espera)

    def horas_de_espera(self, ahora: datetime) -> float:
        return max((ahora - self.timestamp).total_seconds() / 3600.0, 0.0)

    @classmethod
    def desde_fila_csv(cls, fila: dict) -> "Incident":
        return cls(
            id=fila["id"],
            ubicacion=fila["ubicacion"],
            prioridad=int(fila["prioridad"]),
            tipo=fila["tipo"],
            timestamp=datetime.fromisoformat(fila["timestamp"]),
            estado=EstadoIncidente(fila["estado"]),
        )
