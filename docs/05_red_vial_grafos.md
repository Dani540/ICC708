# Parte 5: Grafos: la red vial (`modelos/red_vial.py`, `generar_datos.py`)

## Modelo

La red vial es un **grafo no dirigido, conexo y ponderado**:

* **Nodos**: 4 centros de emergencia (`C-NORTE`, `C-SUR`, `C-ORIENTE`,
  `C-PONIENTE`) y 51 zonas (`Z-01` … `Z-51`). Total: **55 nodos** (mínimo
  exigido: 50). Cada nodo tiene coordenadas `(x, y)` en un plano de
  100 × 100 km.
* **Aristas**: **115 caminos** (mínimo exigido: 100), bidireccionales.
* **Peso**: tiempo de desplazamiento en **minutos**, calculado como
  `distancia_euclidiana / velocidad_de_la_via × 60` con velocidades entre
  30 y 55 km/h por arista.

```
Ejemplo (datos/aristas.csv):
origen,destino,tiempo_minutos
C-NORTE,Z-24,11.5
C-SUR,Z-38,20.9
Z-18,Z-29,21.6
```

La representación interna es una lista de adyacencia (ver
[01_diseno_adt.md](01_diseno_adt.md)); el grafo se carga desde CSV con
`RoadNetwork.cargar_desde_csv`, cumpliendo la opción "CSV" del enunciado.

## Formatos de archivo

| Archivo | Columnas | Contenido |
|---------|----------|-----------|
| `datos/nodos.csv` | `id,x,y` | 55 nodos con coordenadas en km |
| `datos/aristas.csv` | `origen,destino,tiempo_minutos` | 115 aristas no dirigidas |
| `datos/centros.csv` | `id,nombre,ubicacion` | Los 4 centros de emergencia |
| `datos/incidentes.csv` | `id,ubicacion,prioridad,tipo,timestamp,estado` | 520 incidentes |

## Generación del dataset (`generar_datos.py`)

Todo se genera con `random.Random(20260704)`: **misma semilla, mismo dataset**,
lo que hace reproducibles las evidencias y los experimentos.

### Topología de la red

1. **Colocación**: los 4 centros se fijan en los cuatro puntos cardinales del
   mapa y las 51 zonas se dispersan con coordenadas uniformes.
2. **Vecinos cercanos**: cada nodo se conecta con sus 3 vecinos más próximos
   (distancia euclidiana). Esto produce una malla local realista: los caminos
   conectan lugares próximos entre sí.
3. **Conectividad garantizada**: con un *union-find* se detectan las
   componentes conexas y se agrega la arista más corta entre componentes
   hasta que quede una sola. Sin este paso, BFS/Dijkstra podrían no encontrar
   ruta hacia algunas zonas.
4. **Atajos**: se agregan aristas aleatorias (entre nodos a menos de 50 km)
   hasta llegar a 115, creando rutas alternativas que hacen interesante la
   comparación entre algoritmos.

### Pesos y velocidades

Cada arista recibe una velocidad aleatoria entre 30 y 55 km/h, simulando vías
de distinta calidad. El peso es el tiempo de recorrido en minutos. La
velocidad máxima real (55) se mantiene **por debajo** de la constante
`VELOCIDAD_MAXIMA_KMH = 60` que usa la heurística de A*: así la heurística
nunca sobreestima el tiempo real ni siquiera con el redondeo a un decimal, y
se garantiza su admisibilidad (ver
[06_algoritmos_busqueda.md](06_algoritmos_busqueda.md)).

### Incidentes

* 520 incidentes (mínimo exigido: 500) con id `I-0001` … `I-0520`.
* Cada zona recibe un peso de aparición aleatorio (0.5–4.0), de modo que unas
  zonas concentran más incidentes que otras y el reporte "zonas más
  afectadas" muestra diferencias reales (Z-03 acumula 22, otras solo 2–3).
* La prioridad base 1–5 sigue la distribución `[10, 20, 30, 25, 15] %`,
  con predominio de severidades medias, como en un triaje real.
* Los timestamps se reparten en las 72 horas previas a la fecha de referencia
  (2026-07-04 12:00), lo que produce un rango amplio de factores de espera.
* Todos parten en estado `pendiente`; el estado evoluciona durante el
  escenario integrado.

## Estadísticas del grafo generado

| Métrica | Valor |
|---------|-------|
| Nodos | 55 (4 centros + 51 zonas) |
| Aristas | 115 |
| Grado promedio | 2 × 115 / 55 ≈ 4.2 |
| Densidad | 115 / (55 × 54 / 2) ≈ 7.7 % |
| Conexo | Sí (garantizado por construcción) |

Con una densidad del 8 %, la lista de adyacencia usa ~230 pares frente a las
3 025 celdas de una matriz de adyacencia - la representación elegida es la
adecuada para un grafo disperso.
