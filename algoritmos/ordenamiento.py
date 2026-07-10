def _identidad(elemento):
    return elemento


def merge_sort(elementos: list, clave=None) -> list:
    """Ordenamiento estable por mezcla O(n log n) en todos los casos, O(n) espacio"""
    if clave is None:
        clave = _identidad
    if len(elementos) <= 1:
        return list(elementos)
    mitad = len(elementos) // 2
    izquierda = merge_sort(elementos[:mitad], clave)
    derecha = merge_sort(elementos[mitad:], clave)
    return _mezclar(izquierda, derecha, clave)


def _mezclar(izquierda: list, derecha: list, clave) -> list:
    resultado = []
    i = j = 0
    while i < len(izquierda) and j < len(derecha):
        if clave(izquierda[i]) <= clave(derecha[j]):
            resultado.append(izquierda[i])
            i += 1
        else:
            resultado.append(derecha[j])
            j += 1
    resultado.extend(izquierda[i:])
    resultado.extend(derecha[j:])
    return resultado


def quick_sort(elementos: list, clave=None) -> list:
    """Ordenamiento rapido con particion de tres vias y pivote central

    O(n log n) promedio, O(n^2) en el peor caso; la particion de tres vias
    lo hace robusto frente a listas ya ordenadas o con muchos duplicados
    """
    if clave is None:
        clave = _identidad
    if len(elementos) <= 1:
        return list(elementos)
    pivote = clave(elementos[len(elementos) // 2])
    menores = [elemento for elemento in elementos if clave(elemento) < pivote]
    iguales = [elemento for elemento in elementos if clave(elemento) == pivote]
    mayores = [elemento for elemento in elementos if clave(elemento) > pivote]
    return quick_sort(menores, clave) + iguales + quick_sort(mayores, clave)
