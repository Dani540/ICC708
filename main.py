"""
Punto de entrada del laboratorio

Dos formas de ejecutarlo:

1) Menú interactivo (por defecto):
        
        python main.py
    
    Permite elegir escenario (grafo/laberinto), origen de datos (predefinido o
    CSV), algoritmo, nodo inicial y nodo objetivo (presione enter para default); 
    muestra orden de visita, camino, costo y abre la visualización gráfica (en caso de correr en "Todos (comparar)", las interfaces gráficas se van mostrando a medida que se van cerrando)

2) Modo demostración (genera todas las capturas de una vez):
         python main.py --demo
    Corre los 4 algoritmos en grafo y laberinto, imprime la tabla comparativa y guarda los PNG en la carpeta capturas/
"""

import os
import sys

try:
    sys.stdout.reconfigure(encoding="utf-8") # por si acaso, no vaya a ser que se rompa en consola por simbolos o tildes
except Exception:
    pass

from src.algoritmos import ALGORITMOS, comparar_algoritmos
from src.escenarios import grafo_predefinido, laberinto_predefinido
from src.grafo import (ProblemaGrafo, cargar_coordenadas, cargar_lista_adyacencia,
                       cargar_matriz_adyacencia)
from src.laberinto import ProblemaLaberinto, cargar_laberinto
from src import visualizacion as vis

DIR = os.path.dirname(os.path.abspath(__file__))
DIR_DATA = os.path.join(DIR, "data")
DIR_CAPTURAS = os.path.join(DIR, "capturas")


# ===========================================================================
# Reporte por consola
# ===========================================================================
def imprimir_resultado(nombre_alg, resultado):
    print(f"\n----- {nombre_alg} -----")
    print(f"  ¿Éxito?         : {'sí' if resultado.exito else 'no'}")
    print(f"  Nodos visitados : {resultado.num_visitados}")
    print(f"  Orden de visita : {' -> '.join(map(str, resultado.orden_visita))}")
    if resultado.exito:
        print(f"  Camino final    : {' -> '.join(map(str, resultado.camino))}")
        print(f"  Longitud camino : {resultado.longitud_camino} nodos "
              f"({resultado.longitud_camino - 1} pasos)")
        print(f"  Costo total     : {resultado.costo:g}")


def imprimir_tabla_comparativa(resultados, titulo):
    print(f"\n=== Comparación de algoritmos: {titulo} ===")
    print(f"{'Algoritmo':<10}{'Éxito':<8}{'Visitados':<12}{'Long.camino':<13}{'Costo':<8}")
    print("-" * 51)
    for nombre, r in resultados.items():
        costo = f"{r.costo:g}" if r.exito else "∞"
        print(f"{nombre:<10}{('sí' if r.exito else 'no'):<8}"
              f"{r.num_visitados:<12}{r.longitud_camino:<13}{costo:<8}")


# ===========================================================================
# Modo demostración
# ===========================================================================
def modo_demo():
    os.makedirs(DIR_CAPTURAS, exist_ok=True)
    print("### Modo Demo: corriendo BFS, DFS, UCS y A* en ambos escenarios ###")

    # ---- Grafo ----
    grafo = grafo_predefinido("A", "E")
    res_grafo = comparar_algoritmos(grafo)
    imprimir_tabla_comparativa(res_grafo, "GRAFO  A -> E")
    for nombre, r in res_grafo.items():
        ruta = os.path.join(DIR_CAPTURAS, f"grafo_{nombre.replace('*', '_estrella')}.png")
        vis.mostrar_grafo_grafico(grafo, r, f"Grafo · {nombre}", guardar_en=ruta)

    # ---- Laberinto ----
    lab = laberinto_predefinido((0, 0), (9, 14))
    res_lab = comparar_algoritmos(lab)
    imprimir_tabla_comparativa(res_lab, "LABERINTO  (0,0) -> (9,14)")
    for nombre, r in res_lab.items():
        ruta = os.path.join(DIR_CAPTURAS, f"laberinto_{nombre.replace('*', '_estrella')}.png")
        vis.mostrar_laberinto_grafico(lab, r, f"Laberinto · {nombre}", guardar_en=ruta)

    print(f"\nListo. Capturas en: {DIR_CAPTURAS}")


# ===========================================================================
# Menú interactivo
# ===========================================================================
def pedir(mensaje, opciones=None, por_defecto=None):
    while True:
        txt = input(mensaje).strip()
        if txt == "" and por_defecto is not None:
            return por_defecto
        if opciones is None or txt in opciones:
            return txt
        print(f"  Opción inválida. Use una de: {', '.join(opciones)}")


def elegir_grafo() -> ProblemaGrafo:
    print("\nOrigen del grafo:")
    print("  1) Predefinido en código")
    print("  2) CSV lista de adyacencia (data/grafo_lista.csv)")
    print("  3) CSV matriz de adyacencia (data/grafo_matriz.csv)")
    op = pedir("Elija [1/2/3] (1): ", {"1", "2", "3"}, "1")

    coords = {}
    ruta_coords = os.path.join(DIR_DATA, "grafo_coords.csv")
    if os.path.exists(ruta_coords):
        coords = cargar_coordenadas(ruta_coords)

    if op == "1":
        ady = grafo_predefinido().adyacencia
        coords = grafo_predefinido().coordenadas
    elif op == "2":
        ady = cargar_lista_adyacencia(os.path.join(DIR_DATA, "grafo_lista.csv"))
    else:
        ady = cargar_matriz_adyacencia(os.path.join(DIR_DATA, "grafo_matriz.csv"))

    nodos = sorted(ady.keys())
    print(f"Nodos disponibles: {', '.join(nodos)}")
    inicio = pedir(f"Nodo inicial ({nodos[0]}): ", set(nodos), nodos[0])
    objetivo = pedir(f"Nodo objetivo ({nodos[-1]}): ", set(nodos), nodos[-1])
    return ProblemaGrafo(ady, inicio, objetivo, coords)


def elegir_laberinto() -> ProblemaLaberinto:
    print("\nOrigen del laberinto:")
    print("  1) Predefinido en código")
    print("  2) CSV (data/laberinto.csv)")
    op = pedir("Elija [1/2] (1): ", {"1", "2"}, "1")
    if op == "1":
        grid = laberinto_predefinido().grid
    else:
        grid = cargar_laberinto(os.path.join(DIR_DATA, "laberinto.csv"))

    filas, cols = len(grid), len(grid[0])
    print(f"Laberinto de {filas} filas x {cols} columnas (índices desde 0).")
    print("Ingrese posiciones como 'fila,columna'.")
    def leer_pos(msg, defecto):
        # Loop hasta que la posición sea válida, así un formato malo no rompe nada
        while True:
            partes = pedir(msg, None, defecto).replace(" ", "").split(",")
            try:
                if len(partes) != 2:          # se necesita exactamente 'fila,columna'
                    raise ValueError
                f, c = int(partes[0]), int(partes[1])
            except ValueError:
                print("  Formato inválido. Use 'fila,columna' (ej: 3,5).")
                continue
            if not (0 <= f < filas and 0 <= c < cols):
                print(f"  Fuera de rango: fila 0..{filas-1}, columna 0..{cols-1}.")
                continue
            if grid[f][c] != 0:
                print("  Esa celda es una barrera. Elija una celda libre (0).")
                continue
            return (f, c)
    inicio = leer_pos("Posición inicial (0,0): ", "0,0")
    objetivo = leer_pos(f"Posición objetivo ({filas-1},{cols-1}): ", f"{filas-1},{cols-1}")
    return ProblemaLaberinto(grid, inicio, objetivo)


def menu_interactivo():
    os.makedirs(DIR_CAPTURAS, exist_ok=True)
    print("=" * 60)
    print(" Lab 5 · Búsqueda: BFS / DFS / UCS / A* ")
    print("=" * 60)

    tipo = pedir("\nEscenario:  1) Grafo   2) Laberinto   [1/2] (1): ",
                 {"1", "2"}, "1")
    es_grafo = (tipo == "1")
    problema = elegir_grafo() if es_grafo else elegir_laberinto()

    print("\nAlgoritmo:")
    print("  1) BFS   2) DFS   3) UCS   4) A*   5) Todos (para comparar)")
    op_alg = pedir("Elija [1-5] (5): ", {"1", "2", "3", "4", "5"}, "5")
    mapa = {"1": "BFS", "2": "DFS", "3": "UCS", "4": "A*"}

    if op_alg == "5":
        resultados = comparar_algoritmos(problema)
        imprimir_tabla_comparativa(
            resultados, "GRAFO" if es_grafo else "LABERINTO")
        for nombre, r in resultados.items():
            imprimir_resultado(nombre, r)
    else:
        nombre = mapa[op_alg]
        r = ALGORITMOS[nombre](problema)
        resultados = {nombre: r}
        imprimir_resultado(nombre, r)

    # Visualización
    quiere = pedir("\n¿Mostrar visualización gráfica? [s/n] (s): ",
                   {"s", "n"}, "s")
    for nombre, r in resultados.items():
        nom_archivo = ("grafo" if es_grafo else "laberinto") + "_" + nombre.replace("*", "_estrella")
        ruta = os.path.join(DIR_CAPTURAS, nom_archivo + ".png")
        if es_grafo:
            vis.mostrar_grafo_texto(problema, r)
            vis.mostrar_grafo_grafico(problema, r, f"Grafo · {nombre}",
                                      guardar_en=ruta, mostrar=(quiere == "s"))
        else:
            vis.mostrar_laberinto_texto(problema, r)
            vis.mostrar_laberinto_grafico(problema, r, f"Laberinto · {nombre}",
                                          guardar_en=ruta, mostrar=(quiere == "s"))


def main():
    if "--demo" in sys.argv:
        modo_demo()
    else:
        try:
            menu_interactivo()
        except (KeyboardInterrupt, EOFError):
            print("\nSaliendo.")


if __name__ == "__main__":
    main()
