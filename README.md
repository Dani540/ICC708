# Sistema Inteligente de Gestión y Optimización de Rutas de Emergencia

Proyecto Integrador Final: Programación Avanzada (ICC708)

Prototipo que gestiona incidentes durante un desastre natural: los registra en
estructuras de datos propias, los prioriza dinámicamente, analiza las zonas
afectadas y calcula rutas óptimas desde los centros de emergencia usando
algoritmos de búsqueda sobre grafos.

## Ejecución

```bash
# 1. Generar el dataset (520 incidentes, 55 nodos, 115 aristas)
python generar_datos.py

# 2. Ejecutar el escenario integrado (Parte 7)
python main.py

# 3. Ejecutar el análisis experimental (benchmarks)
python experimentos.py
```

## Estructura del proyecto

```
proyecto_integrador_final/
├── main.py                  Escenario integrado (flujo completo de la Parte 7)
├── generar_datos.py         Generador reproducible del dataset (semilla fija)
├── experimentos.py          Análisis experimental de todas las estructuras
├── reportes.py              Reportes ordenados (Parte 4)
├── modelos/                 Parte 1: ADT
│   ├── incidente.py         Incident + EstadoIncidente
│   ├── centro_emergencia.py EmergencyCenter
│   └── red_vial.py          RoadNetwork (grafo ponderado)
├── estructuras/             Partes 2 y 3: estructuras propias
│   ├── tabla_hash.py        TablaHash (encadenamiento, sin dict) + métricas
│   ├── heap.py              MinHeap binario genérico
│   └── cola_prioridad.py    PriorityQueue máxima con actualización O(log n)
├── algoritmos/              Partes 4 y 6
│   ├── ordenamiento.py      MergeSort y QuickSort
│   └── busqueda.py          BFS, Dijkstra/UCS y A*
├── datos/                   Dataset generado (CSV)
│   ├── incidentes.csv       520 incidentes
│   ├── nodos.csv            55 nodos con coordenadas (para la heurística de A*)
│   ├── aristas.csv          115 aristas con tiempo de desplazamiento en minutos
│   └── centros.csv          4 centros de emergencia
└── docs/                    Documentación extensa de cada parte
```

## Cobertura de requerimientos

| Parte | Requerimiento | Implementación |
|-------|---------------|----------------|
| 1 | ADT Incident, EmergencyCenter, RoadNetwork | `modelos/`, ver [docs/01_diseno_adt.md](docs/01_diseno_adt.md) |
| 2 | Tabla hash propia (sin `dict`) con métricas | `estructuras/tabla_hash.py`, ver [docs/02_tabla_hash.md](docs/02_tabla_hash.md) |
| 3 | Priority Queue basada en heap | `estructuras/heap.py`, `estructuras/cola_prioridad.py`, ver [docs/03_heap_cola_prioridad.md](docs/03_heap_cola_prioridad.md) |
| 4 | MergeSort y QuickSort + reportes ordenados | `algoritmos/ordenamiento.py`, `reportes.py`, ver [docs/04_ordenamiento.md](docs/04_ordenamiento.md) |
| 5 | Red vial como grafo ponderado cargado desde CSV | `modelos/red_vial.py`, `generar_datos.py`, ver [docs/05_red_vial_grafos.md](docs/05_red_vial_grafos.md) |
| 6 | BFS y UCS/Dijkstra obligatorios, A* como bono | `algoritmos/busqueda.py`, ver [docs/06_algoritmos_busqueda.md](docs/06_algoritmos_busqueda.md) |
| 7 | Escenario integrado | `main.py`, ver [docs/07_escenario_integrado.md](docs/07_escenario_integrado.md) |
| - | Análisis experimental | `experimentos.py`, ver [docs/08_analisis_experimental.md](docs/08_analisis_experimental.md) |

## Resultados destacados (ejecución real)

* La tabla hash mantiene el factor de carga bajo 0.75 con redimensionamiento a
  capacidades primas; con 20 000 claves el bucket más largo tiene 3 entradas y
  buscar 500 claves tarda ~1 ms frente a ~220 ms de la búsqueda lineal.
* La cola de prioridad inserta y extrae en tiempo logarítmico medible:
  ~8.6 µs por inserción con 500 elementos y ~15.5 µs con 50 000.
* En la red vial, A* encuentra la misma ruta óptima que Dijkstra visitando en
  promedio la mitad de los nodos (17.9 contra 34.1); BFS es el más rápido pero
  entrega rutas hasta 12 % más costosas por ignorar los pesos.
* Escenario integrado: el incidente más urgente (`I-0102`, incendio con 71.8 h
  de espera, prioridad 364.0) se asigna al Centro Sur con la ruta
  `C-SUR -> Z-38 -> Z-29 -> Z-18` (67.9 minutos).

