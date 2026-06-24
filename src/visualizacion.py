"""
Visualización del recorrido, tanto en text (siempre disponible) como
gráfica con matplotlib (cómo indica el lab)

Laberinto: imshow (mapa de calor) con barreras, visitados, camino, inicio, objetivo.
Grafo: networkx con nodos coloreados y aristas del camino resaltadas.
"""

from typing import Optional

from .grafo import ProblemaGrafo
from .laberinto import ProblemaLaberinto
from .problema import Resultado

# Lazy import de matplotlib para que, si no está instalado, el modo texto sigua funcionando
try:
    import matplotlib
    import matplotlib.pyplot as plt
    from matplotlib.colors import ListedColormap
    _HAY_MPL = True
except Exception:  
    _HAY_MPL = False

try:
    import networkx as nx
    _HAY_NX = True
except Exception: 
    _HAY_NX = False


def hay_matplotlib() -> bool:
    return _HAY_MPL


# ===========================================================================
# LABERINTO
# ===========================================================================
# Códigos de color para el laberinto:
#                  0 libre      1 barrera    2 visitado    3 camino     4 inicio     5 objetivo
_COLORES_LAB = ["#ffffff", "#2c3e50", "#5dade2", "#f5b041", "#27ae60", "#e74c3c"]


def _matriz_codigos(problema: ProblemaLaberinto, resultado: Resultado):
    """Construye una matriz de códigos de 0 al 5 para pintar el laberinto."""
    codigos = [[problema.grid[f][c] for c in range(problema.cols)]
               for f in range(problema.filas)]
    for (f, c) in resultado.orden_visita:           # 2 = visitado
        codigos[f][c] = 2
    for (f, c) in resultado.camino:                 # 3 = camino final
        codigos[f][c] = 3
    fi, ci = problema.inicio
    fo, co = problema.objetivo
    codigos[fi][ci] = 4                              # 4 = inicio
    codigos[fo][co] = 5                              # 5 = objetivo
    return codigos


def mostrar_laberinto_texto(problema: ProblemaLaberinto, resultado: Resultado) -> None:
    """Imprime el laberinto con simbolos:
    # barrera: . libre: o visitado: * camino: S inicio: G objetivo
    """
    simbolo = {0: " . ", 1: " # ", 2: " o ", 3: " * ", 4: " S ", 5: " G "}
    codigos = _matriz_codigos(problema, resultado)
    print("Leyenda:  # barrera   . libre   o visitado   * camino   S inicio   G objetivo")
    for fila in codigos:
        print("".join(simbolo[v] for v in fila))


def mostrar_laberinto_grafico(
    problema: ProblemaLaberinto,
    resultado: Resultado,
    titulo: str = "Laberinto",
    guardar_en: Optional[str] = None,
    mostrar: bool = False,
) -> None:
    if not _HAY_MPL:
        print("[matplotlib no disponible] Uso la visualización en texto:")
        mostrar_laberinto_texto(problema, resultado)
        return

    codigos = _matriz_codigos(problema, resultado)
    cmap = ListedColormap(_COLORES_LAB)

    fig, ax = plt.subplots(figsize=(problema.cols * 0.6, problema.filas * 0.6))
    ax.imshow(codigos, cmap=cmap, vmin=0, vmax=5)

    # Rejilla para distinguir celdas.
    ax.set_xticks([x - 0.5 for x in range(problema.cols + 1)], minor=True)
    ax.set_yticks([y - 0.5 for y in range(problema.filas + 1)], minor=True)
    ax.grid(which="minor", color="#bbbbbb", linewidth=0.5)
    ax.set_xticks(range(problema.cols))
    ax.set_yticks(range(problema.filas))
    ax.tick_params(length=0)

    # Etiquetas S y G encima de las celclas.
    fi, ci = problema.inicio
    fo, co = problema.objetivo
    ax.text(ci, fi, "S", ha="center", va="center", color="white", fontweight="bold")
    ax.text(co, fo, "G", ha="center", va="center", color="white", fontweight="bold")

    costo = "∞" if not resultado.exito else f"{resultado.costo:g}"
    ax.set_title(f"{titulo}\nvisitados={resultado.num_visitados}  "
                 f"costo={costo}  long. camino={resultado.longitud_camino}")
    fig.tight_layout()

    if guardar_en:
        fig.savefig(guardar_en, dpi=120, bbox_inches="tight")
        print(f"  figura guardada en: {guardar_en}")
    if mostrar:
        plt.show()
    plt.close(fig)


# ===========================================================================
# GRAFO
# ===========================================================================
def mostrar_grafo_texto(problema: ProblemaGrafo, resultado: Resultado) -> None:
    print("Orden de visita :", " -> ".join(map(str, resultado.orden_visita)))
    if resultado.exito:
        print("Camino final    :", " -> ".join(map(str, resultado.camino)))
        print(f"Costo total     : {resultado.costo:g}")
    else:
        print("No se encontró camino al objetivo.")


def mostrar_grafo_grafico(
    problema: ProblemaGrafo,
    resultado: Resultado,
    titulo: str = "Grafo",
    guardar_en: Optional[str] = None,
    mostrar: bool = False,
) -> None:
    if not (_HAY_MPL and _HAY_NX):
        print("[matplotlib/networkx no disponibles] Uso la visualización en texto:")
        mostrar_grafo_texto(problema, resultado)
        return

    G = nx.Graph()
    for nodo, vecinos in problema.adyacencia.items():
        for vecino, costo in vecinos:
            G.add_edge(nodo, vecino, weight=costo)

    # Posiciones: coordenadas reales si existen; si no, layout automático.
    if problema.coordenadas:
        pos = {n: problema.coordenadas[n] for n in G.nodes if n in problema.coordenadas}
    else:
        pos = nx.spring_layout(G, seed=42)

    camino = resultado.camino
    visitados = set(resultado.orden_visita)
    aristas_camino = set()
    for a, b in zip(camino, camino[1:]):
        aristas_camino.add(frozenset((a, b)))

    # Color de cada nodo según su rol.
    colores = []
    for n in G.nodes:
        if n == problema.inicio:
            colores.append("#27ae60")        # inicio = verde
        elif n == problema.objetivo:
            colores.append("#e74c3c")        # objetivo = rojo
        elif n in camino:
            colores.append("#f5b041")        # en el camino = naranja
        elif n in visitados:
            colores.append("#aed6f1")        # visitado = celeste
        else:
            colores.append("#ecf0f1")        # no tocado = gris claro

    colores_aristas, anchos = [], []
    for a, b in G.edges:
        if frozenset((a, b)) in aristas_camino:
            colores_aristas.append("#f5b041")
            anchos.append(3.5)
        else:
            colores_aristas.append("#95a5a6")
            anchos.append(1.0)

    fig, ax = plt.subplots(figsize=(8, 6))
    nx.draw_networkx_edges(G, pos, edge_color=colores_aristas, width=anchos, ax=ax)
    nx.draw_networkx_nodes(G, pos, node_color=colores, edgecolors="#34495e",
                           node_size=900, ax=ax)
    nx.draw_networkx_labels(G, pos, font_weight="bold", ax=ax)
    etiquetas = nx.get_edge_attributes(G, "weight")
    etiquetas = {k: f"{v:g}" for k, v in etiquetas.items()}
    nx.draw_networkx_edge_labels(G, pos, edge_labels=etiquetas, ax=ax)

    costo = "∞" if not resultado.exito else f"{resultado.costo:g}"
    ax.set_title(f"{titulo}\norden de visita: {' '.join(map(str, resultado.orden_visita))}\n"
                 f"camino: {' -> '.join(map(str, camino)) or '(sin camino)'}   "
                 f"costo={costo}  visitados={resultado.num_visitados}")
    ax.axis("off")
    fig.tight_layout()

    if guardar_en:
        fig.savefig(guardar_en, dpi=120, bbox_inches="tight")
        print(f"  figura guardada en: {guardar_en}")
    if mostrar:
        plt.show()
    plt.close(fig)
