import time

"""
torres_hanoi.py
Implementación de las Torres de Hanói utilizando una estructura de datos de Pila (Stack).
"""

class Pila:
    """Clase que representa una estructura de datos de tipo pila (LIFO)."""
    
    def __init__(self, nombre):
        self.items = []
        self.nombre = nombre

    def is_empty(self):
        return len(self.items) == 0

    def push(self, item):
        self.items.append(item)

    def pop(self):
        if not self.is_empty():
            return self.items.pop()
        raise IndexError("No se puede desapilar de una pila vacía")

    def peek(self):
        if not self.is_empty():
            return self.items[-1]
        return None

    def __str__(self):
        return f"{self.nombre}: {self.items}"


def move_disk(source, destination):
    """
    Saca un disco de la pila de origen y lo coloca en la pila de destino,
    imprimiendo la acción en consola.
    """
    disk = source.pop()
    destination.push(disk)
    print(f"Moviendo disco {disk} de '{source.nombre}' a '{destination.nombre}'")


def solve_hanoi(n, source, auxiliary, destination):
    """
    Función recursiva para resolver el problema interactuando con las pilas.
    
    :param n: Número de discos a mover.
    :param source: Pila desde donde se mueven los discos.
    :param auxiliary: Pila utilizada como apoyo temporal.
    :param destination: Pila hacia donde deben llegar los discos.
    """
    # Caso base: Si solo hay un disco, se mueve directamente al destino
    if n == 1:
        move_disk(source, destination)
        return
    
    # Paso 1: Mover n-1 discos del Origen al Auxiliar, usando el Destino como apoyo
    solve_hanoi(n - 1, source, destination, auxiliary)
    
    # Paso 2: Mover el disco más grande restante del Origen al Destino
    move_disk(source, destination)
    
    # Paso 3: Mover los n-1 discos del Auxiliar al Destino, usando el Origen como apoyo
    solve_hanoi(n - 1, auxiliary, source, destination)


def main():
    # Configuración inicial
    num_discos = 3
    
    # Instanciamos las tres pilas
    torre_origen = Pila("Origen")
    torre_auxiliar = Pila("Auxiliar")
    torre_destino = Pila("Destino")
    
    # Apilamos los discos en la torre de origen (el más grande en el fondo)
    # Ejemplo con 3 discos: [3, 2, 1]
    for i in range(num_discos, 0, -1):
        torre_origen.push(i)
        
    print("=== ESTADO INICIAL ===")
    print(torre_origen)
    print(torre_auxiliar)
    print(torre_destino)
    print("\nIniciando movimientos...\n")
    
    # Capturamos el tiempo exacto antes de empezar
    inicio_tiempo = time.perf_counter()
    
    # Ejecutamos el algoritmo
    solve_hanoi(num_discos, torre_origen, torre_auxiliar, torre_destino)
    
    # Capturamos el tiempo exacto al terminar y calculamos la diferencia
    fin_tiempo = time.perf_counter()
    tiempo_transcurrido = fin_tiempo - inicio_tiempo
    
    print("\n=== ESTADO FINAL ===")
    print(torre_origen)
    print(torre_auxiliar)
    print(torre_destino)
    
    # Imprimimos el tiempo total con 6 decimales para mayor claridad
    print(f"\n⏱️ Tiempo de ejecución: {tiempo_transcurrido:.6f} segundos")


if __name__ == "__main__":
    main()