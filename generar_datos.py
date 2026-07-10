import csv
import math
import random
from datetime import datetime, timedelta
from pathlib import Path

SEMILLA = 20260704
FECHA_REFERENCIA = datetime(2026, 7, 4, 12, 0)
DIRECTORIO_DATOS = Path(__file__).parent / "datos"

CANTIDAD_INCIDENTES = 520
CANTIDAD_ZONAS = 51
OBJETIVO_ARISTAS = 115
VECINOS_CERCANOS = 3
VELOCIDAD_MINIMA_KMH = 30.0
VELOCIDAD_CRUCERO_KMH = 55.0
HORAS_DE_HISTORIAL = 72

CENTROS = [
    ("C-NORTE", "Centro de Emergencia Norte", 50.0, 92.0),
    ("C-SUR", "Centro de Emergencia Sur", 50.0, 8.0),
    ("C-ORIENTE", "Centro de Emergencia Oriente", 92.0, 50.0),
    ("C-PONIENTE", "Centro de Emergencia Poniente", 8.0, 50.0),
]

TIPOS_INCIDENTE = [
    "incendio",
    "accidente_vehicular",
    "emergencia_medica",
    "inundacion",
    "derrumbe",
    "fuga_gas",
    "rescate",
]


def generar_nodos(rng: random.Random) -> list[tuple[str, float, float]]:
    nodos = [(identificador, x, y) for identificador, _, x, y in CENTROS]
    for numero in range(1, CANTIDAD_ZONAS + 1):
        nodos.append((
            f"Z-{numero:02d}",
            round(rng.uniform(2.0, 98.0), 2),
            round(rng.uniform(2.0, 98.0), 2),
        ))
    return nodos


def generar_aristas(nodos: list[tuple[str, float, float]],
                    rng: random.Random) -> list[tuple[str, str, float]]:
    """Conecta cada nodo con sus vecinos mas cercanos, garantiza conectividad
    y agrega atajos aleatorios hasta alcanzar el objetivo de aristas"""
    posiciones = {identificador: (x, y) for identificador, x, y in nodos}
    identificadores = list(posiciones)
    aristas: set[tuple[str, str]] = set()

    for identificador in identificadores:
        cercanos = sorted(
            (otro for otro in identificadores if otro != identificador),
            key=lambda otro: math.dist(posiciones[identificador], posiciones[otro]),
        )[:VECINOS_CERCANOS]
        for otro in cercanos:
            aristas.add(tuple(sorted((identificador, otro))))

    padre = {identificador: identificador for identificador in identificadores}

    def raiz(nodo: str) -> str:
        while padre[nodo] != nodo:
            padre[nodo] = padre[padre[nodo]]
            nodo = padre[nodo]
        return nodo

    for origen, destino in aristas:
        padre[raiz(origen)] = raiz(destino)

    while len({raiz(identificador) for identificador in identificadores}) > 1:
        origen, destino = min(
            (
                (primero, segundo)
                for primero in identificadores
                for segundo in identificadores
                if raiz(primero) != raiz(segundo)
            ),
            key=lambda par: math.dist(posiciones[par[0]], posiciones[par[1]]),
        )
        aristas.add(tuple(sorted((origen, destino))))
        padre[raiz(origen)] = raiz(destino)

    while len(aristas) < OBJETIVO_ARISTAS:
        origen, destino = rng.sample(identificadores, 2)
        par = tuple(sorted((origen, destino)))
        if par not in aristas and math.dist(posiciones[origen], posiciones[destino]) <= 50.0:
            aristas.add(par)

    resultado = []
    for origen, destino in sorted(aristas):
        distancia = math.dist(posiciones[origen], posiciones[destino])
        velocidad = rng.uniform(VELOCIDAD_MINIMA_KMH, VELOCIDAD_CRUCERO_KMH)
        tiempo_minutos = round(distancia / velocidad * 60.0, 1)
        resultado.append((origen, destino, tiempo_minutos))
    return resultado


def generar_incidentes(zonas: list[str], rng: random.Random) -> list[tuple]:
    pesos_de_zona = [rng.uniform(0.5, 4.0) for _ in zonas]
    filas = []
    for numero in range(1, CANTIDAD_INCIDENTES + 1):
        minutos_atras = rng.uniform(0.0, HORAS_DE_HISTORIAL * 60.0)
        marca = FECHA_REFERENCIA - timedelta(minutes=minutos_atras)
        filas.append((
            f"I-{numero:04d}",
            rng.choices(zonas, weights=pesos_de_zona)[0],
            rng.choices([1, 2, 3, 4, 5], weights=[10, 20, 30, 25, 15])[0],
            rng.choice(TIPOS_INCIDENTE),
            marca.isoformat(timespec="minutes"),
            "pendiente",
        ))
    return filas


def escribir_csv(ruta: Path, encabezados: list[str], filas: list[tuple]) -> None:
    with open(ruta, "w", newline="", encoding="utf-8") as archivo:
        escritor = csv.writer(archivo)
        escritor.writerow(encabezados)
        escritor.writerows(filas)


def main() -> None:
    rng = random.Random(SEMILLA)
    DIRECTORIO_DATOS.mkdir(exist_ok=True)

    nodos = generar_nodos(rng)
    aristas = generar_aristas(nodos, rng)
    zonas = [identificador for identificador, _, _ in nodos if identificador.startswith("Z-")]
    incidentes = generar_incidentes(zonas, rng)
    centros = [(identificador, nombre, identificador) for identificador, nombre, _, _ in CENTROS]

    escribir_csv(DIRECTORIO_DATOS / "nodos.csv", ["id", "x", "y"], nodos)
    escribir_csv(DIRECTORIO_DATOS / "aristas.csv", ["origen", "destino", "tiempo_minutos"], aristas)
    escribir_csv(DIRECTORIO_DATOS / "centros.csv", ["id", "nombre", "ubicacion"], centros)
    escribir_csv(
        DIRECTORIO_DATOS / "incidentes.csv",
        ["id", "ubicacion", "prioridad", "tipo", "timestamp", "estado"],
        incidentes,
    )

    print(f"Datos generados en {DIRECTORIO_DATOS}")
    print(f"  Nodos:      {len(nodos)} ({len(CENTROS)} centros + {len(zonas)} zonas)")
    print(f"  Aristas:    {len(aristas)}")
    print(f"  Incidentes: {len(incidentes)}")


if __name__ == "__main__":
    main()
