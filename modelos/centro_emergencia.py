from dataclasses import dataclass


@dataclass(frozen=True)
class EmergencyCenter:
    """ADT que representa un centro de operaciones de emergencia"""

    id: str
    nombre: str
    ubicacion: str
