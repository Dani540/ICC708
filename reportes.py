from datetime import datetime

from algoritmos.ordenamiento import merge_sort, quick_sort
from estructuras.tabla_hash import TablaHash
from modelos.incidente import Incident


def incidentes_mas_antiguos(incidentes: list[Incident], cantidad: int = 10) -> list[Incident]:
    """Incidentes ordenados por tiempo de reporte con MergeSort O(n log n)"""
    ordenados = merge_sort(incidentes, clave=lambda incidente: incidente.timestamp)
    return ordenados[:cantidad]


def incidentes_mas_criticos(incidentes: list[Incident], ahora: datetime,
                            cantidad: int = 10) -> list[Incident]:
    """Incidentes ordenados por prioridad efectiva con QuickSort O(n log n)"""
    ordenados = quick_sort(incidentes, clave=lambda incidente: incidente.prioridad_efectiva(ahora))
    return ordenados[::-1][:cantidad]


def zonas_mas_afectadas(incidentes: list[Incident]) -> list[tuple[str, int]]:
    """Pares (zona, total) ordenados por frecuencia descendente O(n log n)"""
    conteo = TablaHash()
    for incidente in incidentes:
        total = conteo.buscar(incidente.ubicacion) or 0
        conteo.insertar(incidente.ubicacion, total + 1)
    pares = conteo.entradas()
    return merge_sort(pares, clave=lambda par: par[1])[::-1]
