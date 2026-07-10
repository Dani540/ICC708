import csv
from pathlib import Path

import reportes
from algoritmos.busqueda import a_estrella, bfs, dijkstra
from estructuras.cola_prioridad import PriorityQueue
from estructuras.tabla_hash import TablaHash
from modelos import EmergencyCenter, EstadoIncidente, Incident, RoadNetwork

DIRECTORIO_DATOS = Path(__file__).parent / "datos"


def cargar_incidentes(ruta: Path) -> list[Incident]:
    with open(ruta, newline="", encoding="utf-8") as archivo:
        return [Incident.desde_fila_csv(fila) for fila in csv.DictReader(archivo)]


def cargar_centros(ruta: Path) -> list[EmergencyCenter]:
    with open(ruta, newline="", encoding="utf-8") as archivo:
        return [
            EmergencyCenter(fila["id"], fila["nombre"], fila["ubicacion"])
            for fila in csv.DictReader(archivo)
        ]


def titulo(texto: str) -> None:
    print(f"\n{'=' * 72}")
    print(texto)
    print("=" * 72)


def formato_tiempo(minutos: float) -> str:
    horas, resto = divmod(round(minutos), 60)
    return f"{horas}h {resto:02d}m"


def formato_ruta(ruta: list[str]) -> str:
    return " -> ".join(ruta)


def main() -> None:
    titulo("PASO 1 - Carga de datos")
    incidentes = cargar_incidentes(DIRECTORIO_DATOS / "incidentes.csv")
    centros = cargar_centros(DIRECTORIO_DATOS / "centros.csv")
    red = RoadNetwork.cargar_desde_csv(
        DIRECTORIO_DATOS / "nodos.csv", DIRECTORIO_DATOS / "aristas.csv"
    )
    ahora = max(incidente.timestamp for incidente in incidentes)
    print(f"Incidentes leidos:    {len(incidentes)}")
    print(f"Centros de operacion: {len(centros)}")
    print(f"Red vial:             {red.numero_nodos} nodos, {red.numero_aristas} aristas")
    print(f"Hora de referencia:   {ahora}")

    titulo("PASO 2 - Insercion en tabla hash y cola de prioridad")
    tabla = TablaHash()
    cola = PriorityQueue()
    for incidente in incidentes:
        tabla.insertar(incidente.id, incidente)
        cola.insertar(incidente, incidente.prioridad_efectiva(ahora))

    estadisticas = tabla.estadisticas()
    print(f"Tabla hash:  {estadisticas.elementos} elementos en {estadisticas.capacidad} buckets")
    print(f"  Factor de carga:  {estadisticas.factor_carga:.3f}")
    print(f"  Colisiones:       {estadisticas.colisiones}")
    print(f"  Buckets usados:   {estadisticas.buckets_usados}")
    print(f"  Bucket maximo:    {estadisticas.bucket_maximo}")
    print(f"Cola de prioridad: {len(cola)} incidentes")

    print("\nTop 10 incidentes mas criticos:")
    print(f"  {'ID':<8} {'Zona':<6} {'Tipo':<20} {'Base':>4} {'Espera':>8} {'Prioridad':>10}")
    for prioridad, incidente in cola.top_k(10):
        espera = incidente.horas_de_espera(ahora)
        print(f"  {incidente.id:<8} {incidente.ubicacion:<6} {incidente.tipo:<20} "
              f"{incidente.prioridad:>4} {espera:>7.1f}h {prioridad:>10.1f}")

    reclasificado = incidentes[99]
    prioridad_nueva = reclasificado.prioridad_efectiva(ahora) * 2.0
    cola.actualizar_prioridad(reclasificado.id, prioridad_nueva)
    print(f"\nPrioridad actualizada (reclasificacion simulada): {reclasificado.id} "
          f"de {reclasificado.prioridad_efectiva(ahora):.1f} a {prioridad_nueva:.1f}")

    titulo("PASO 3 - Extraccion del incidente mas urgente")
    prioridad_urgente, urgente = cola.extraer_mas_urgente()
    print(f"Incidente: {urgente.id}")
    print(f"  Zona:              {urgente.ubicacion}")
    print(f"  Tipo:              {urgente.tipo}")
    print(f"  Prioridad base:    {urgente.prioridad}")
    print(f"  Reportado:         {urgente.timestamp} ({urgente.horas_de_espera(ahora):.1f}h de espera)")
    print(f"  Prioridad efectiva: {prioridad_urgente:.1f}")

    titulo("PASO 4 - Centro de emergencia mas cercano (Dijkstra)")
    print(f"  {'Centro':<12} {'Costo (min)':>12} {'Tramos':>7} {'Visitados':>10}")
    candidatos = []
    for centro in centros:
        resultado = dijkstra(red, centro.ubicacion, urgente.ubicacion)
        candidatos.append((resultado, centro))
        print(f"  {centro.id:<12} {resultado.costo:>12.1f} {resultado.tramos:>7} "
              f"{len(resultado.nodos_visitados):>10}")
    mejor_resultado, mejor_centro = min(candidatos, key=lambda par: par[0].costo)
    print(f"\nCentro elegido: {mejor_centro.nombre} ({mejor_centro.id})")

    titulo("PASO 5 - Comparacion de algoritmos de busqueda")
    algoritmos = [("BFS", bfs), ("Dijkstra/UCS", dijkstra), ("A*", a_estrella)]
    print(f"  {'Algoritmo':<14} {'Tramos':>7} {'Costo (min)':>12} {'Visitados':>10}")
    for nombre, algoritmo in algoritmos:
        resultado = algoritmo(red, mejor_centro.ubicacion, urgente.ubicacion)
        print(f"  {nombre:<14} {resultado.tramos:>7} {resultado.costo:>12.1f} "
              f"{len(resultado.nodos_visitados):>10}")
    print(f"\nRuta sugerida ({mejor_resultado.tramos} tramos):")
    print(f"  {formato_ruta(mejor_resultado.ruta)}")

    titulo("PASO 6 - Asignacion y mantenimiento de la tabla hash")
    urgente.estado = EstadoIncidente.ASIGNADO
    tabla.actualizar(urgente.id, urgente)
    verificado = tabla.buscar(urgente.id)
    print(f"Estado actualizado: {verificado.id} -> {verificado.estado.value}")

    cancelado = incidentes[7]
    tabla.eliminar(cancelado.id)
    print(f"Incidente eliminado de la tabla (cancelado): {cancelado.id}")
    print(f"Busqueda posterior devuelve: {tabla.buscar(cancelado.id)}")
    print(f"Elementos restantes en la tabla: {len(tabla)}")

    titulo("PASO 7 - Reportes ordenados")
    print("Incidentes mas antiguos (MergeSort por timestamp):")
    for incidente in reportes.incidentes_mas_antiguos(incidentes, 5):
        print(f"  {incidente.id}  {incidente.timestamp}  {incidente.ubicacion:<6} {incidente.tipo}")

    print("\nIncidentes mas criticos (QuickSort por prioridad efectiva):")
    for incidente in reportes.incidentes_mas_criticos(incidentes, ahora, 5):
        print(f"  {incidente.id}  prioridad {incidente.prioridad_efectiva(ahora):>6.1f}  "
              f"{incidente.ubicacion:<6} {incidente.tipo}")

    print("\nZonas con mas incidentes (MergeSort por frecuencia):")
    for zona, total in reportes.zonas_mas_afectadas(incidentes)[:5]:
        print(f"  {zona:<6} {total} incidentes")

    titulo("RESUMEN FINAL")
    print(f"Incidente asignado: {urgente.id} ({urgente.tipo} en {urgente.ubicacion})")
    print(f"Prioridad:          {prioridad_urgente:.1f}")
    print(f"Centro asignado:    {mejor_centro.nombre}")
    print(f"Ruta sugerida:      {formato_ruta(mejor_resultado.ruta)}")
    print(f"Costo total:        {mejor_resultado.costo:.1f} minutos")
    print(f"Tiempo estimado:    {formato_tiempo(mejor_resultado.costo)}")


if __name__ == "__main__":
    main()
