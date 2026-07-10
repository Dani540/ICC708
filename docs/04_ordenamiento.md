# Parte 4: Ordenamiento (`algoritmos/ordenamiento.py`, `reportes.py`)

Se implementaron **MergeSort** y **QuickSort**. Ambos reciben un parámetro
`clave` (como el `key` de `sorted`) y devuelven una lista nueva sin modificar
la original, lo que permite ordenar incidentes por timestamp, por prioridad o
zonas por frecuencia con la misma función.

## MergeSort

Estrategia *divide y vencerás*:

1. Dividir la lista por la mitad.
2. Ordenar recursivamente cada mitad.
3. **Mezclar** las dos mitades ya ordenadas recorriéndolas en paralelo y
   tomando siempre el menor frente (`_mezclar`, O(n)).

La recurrencia es `T(n) = 2T(n/2) + O(n)`, es decir **O(n log n) garantizado**
en el mejor, promedio y peor caso, con O(n) de memoria auxiliar.

Es **estable**: cuando hay empate (`<=` en la mezcla) gana el elemento de la
mitad izquierda, así que los elementos con claves iguales conservan su orden
relativo original. Por eso es el algoritmo usado en los reportes por
timestamp y por frecuencia de zona, donde los empates son frecuentes.

## QuickSort

Se implementó con **partición de tres vías y pivote central**:

1. Elegir como pivote la clave del elemento central.
2. Partir la lista en `menores`, `iguales` y `mayores` que el pivote.
3. Ordenar recursivamente `menores` y `mayores` y concatenar.

Complejidad: **O(n log n) promedio, O(n²) en el peor caso** (particiones
sistemáticamente desbalanceadas). Las dos decisiones de diseño atacan
justamente los peores casos clásicos:

* **Pivote central**: una lista ya ordenada o invertida (casos habituales en
  reportes) parte siempre por la mitad, en lugar de degenerar como lo haría
  el pivote en el primer o último elemento.
* **Tres vías**: todos los duplicados del pivote quedan resueltos en la
  partición, así que listas con muchas claves repetidas (por ejemplo,
  prioridades 1–5) no degradan el rendimiento.

Esta variante usa O(n) memoria extra por las tres sublistas; se prefirió la
claridad frente a la versión *in place*, y el experimento confirma que sigue
siendo competitiva.

## Comparación teórica

| | MergeSort | QuickSort (3 vías) |
|---|-----------|--------------------|
| Mejor caso | O(n log n) | O(n log n) |
| Promedio | O(n log n) | O(n log n) |
| Peor caso | **O(n log n)** | O(n²) (improbable con pivote central) |
| Memoria extra | O(n) | O(n) en esta variante |
| Estable | **Sí** | No en general |
| Fortaleza | Garantías y estabilidad | Rápido en la práctica, inmune a duplicados |

## Resultados experimentales

Experimento 3, tiempos en ms (`sorted()` de Python como referencia):

| n | caso | merge_sort | quick_sort | sorted() |
|---|------|-----------|------------|----------|
| 1 000 | aleatorio | 4.91 | 7.19 | 0.27 |
| 1 000 | ordenado | 6.00 | 6.00 | 0.02 |
| 1 000 | inverso | 6.72 | 4.85 | 0.02 |
| 5 000 | aleatorio | 22.95 | 16.06 | 0.53 |
| 5 000 | ordenado | 20.32 | 15.56 | 0.03 |
| 5 000 | inverso | 14.48 | 11.80 | 0.02 |
| 15 000 | aleatorio | 73.67 | 59.77 | 1.94 |
| 15 000 | ordenado | 45.30 | 38.67 | 0.22 |
| 15 000 | inverso | 65.70 | 38.97 | 0.25 |

Discusión:

* **Ambos escalan como n log n**: al multiplicar n por 15 (1 000 → 15 000) el
  tiempo se multiplica por ~13–15, no por 225 como haría un O(n²).
* **QuickSort gana a MergeSort en listas grandes** (~20 % menos tiempo con
  n = 15 000): sus particiones por comprensión de listas recorren la memoria
  secuencialmente, mientras la mezcla de MergeSort alterna entre dos listas.
* **Los casos ordenado e inverso no degradan a QuickSort**; incluso son más
  rápidos que el aleatorio, validando la elección de pivote central + tres
  vías. Con pivote en el primer elemento estos casos serían O(n²).
* `sorted()` es ~30 veces más rápido: es Timsort implementado en C. La
  comparación es útil como referencia de cuánto pesa el intérprete, no como
  competencia: el objetivo de la parte es implementar y analizar los
  algoritmos.

## Los tres reportes (`reportes.py`)

| Reporte | Orden | Algoritmo | Por qué |
|---------|-------|-----------|---------|
| `incidentes_mas_antiguos` | timestamp ascendente | MergeSort | Estable: empates de fecha conservan orden de llegada |
| `incidentes_mas_criticos` | prioridad efectiva descendente | QuickSort | Claves float casi únicas, el caso ideal de QuickSort |
| `zonas_mas_afectadas` | frecuencia descendente | MergeSort | Cuenta con la `TablaHash` propia y ordena los pares (zona, total) |

Salida real del escenario (top 5 de cada reporte):

```
Incidentes mas antiguos:            Zonas con mas incidentes:
  I-0065  2026-07-01 12:00  Z-09      Z-03   22 incidentes
  I-0089  2026-07-01 12:03  Z-21      Z-23   20 incidentes
  I-0324  2026-07-01 12:05  Z-37      Z-39   19 incidentes
  I-0102  2026-07-01 12:11  Z-18      Z-18   18 incidentes
  I-0487  2026-07-01 12:11  Z-32      Z-08   17 incidentes
```
