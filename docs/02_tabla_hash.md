# Parte 2: Tabla Hash propia (`estructuras/tabla_hash.py`)

`TablaHash` es un mapa clave→valor implementado desde cero, **sin usar el
`dict` de Python**, tal como exige el enunciado. Almacena los incidentes por
`id` y expone las métricas de colisiones y ocupación pedidas.

## Diseño

### Encadenamiento separado

La tabla es un arreglo de *buckets*; cada bucket es una lista de pares
`[clave, valor]`:

```
índice 0: []
índice 1: [["I-0102", <Incident>]]
índice 2: [["I-0044", <Incident>], ["I-0311", <Incident>]]   <- colisión
...
```

Cuando dos claves caen en el mismo índice (colisión), simplemente conviven en
la misma lista. Se eligió encadenamiento frente a direccionamiento abierto
porque:

* la eliminación es trivial (no necesita marcas *tombstone*),
* el rendimiento se degrada suavemente cuando sube el factor de carga,
* el código es más simple de razonar y de medir.

### Función de dispersión: djb2

```python
codigo = 5381
for caracter in clave:
    codigo = (codigo * 33 + codigo_del_caracter) & 0xFFFFFFFF
indice = codigo % capacidad
```

djb2 es una función clásica para cadenas: mezcla cada carácter multiplicando
por 33 y acumulando, truncado a 32 bits. Es barata (O(longitud de la clave)) y
distribuye bien claves con prefijos comunes como `I-0001 … I-0520`, que es
exactamente nuestro caso.

### Capacidades primas y redimensionamiento

* La capacidad inicial es 17 y siempre se usa un **número primo**: al reducir
  módulo un primo, los patrones regulares en los códigos hash (claves
  consecutivas, pasos fijos) se reparten mejor entre los buckets.
* Cuando el factor de carga supera **0.75**, la tabla crece al siguiente primo
  mayor que el doble de la capacidad y **redispersa** todas las entradas
  (`_redimensionar`, O(n)). Ese costo ocasional se amortiza: cada elemento se
  redispersa O(log n) veces en total, así que la inserción sigue siendo O(1)
  amortizado.

## Operaciones

| Operación | Precondición | Postcondición | Complejidad promedio | Peor caso |
|-----------|--------------|---------------|----------------------|-----------|
| `insertar(clave, valor)` | `clave` es `str` | La clave queda asociada al valor (reemplaza si existía); factor de carga ≤ 0.75 | O(1) amortizado | O(n) |
| `buscar(clave)` | - | Devuelve el valor o `None`; no modifica la tabla | O(1) | O(n) |
| `actualizar(clave, valor)` | - | Reemplaza el valor si la clave existe; devuelve `True`/`False` | O(1) | O(n) |
| `eliminar(clave)` | - | La clave ya no está; devuelve `True` si existía | O(1) | O(n) |
| `entradas()` / `valores()` | - | Lista de todos los pares/valores | O(n + capacidad) | - |
| `estadisticas()` | - | `EstadisticasTabla` con las métricas; no modifica la tabla | O(capacidad) | - |

El peor caso O(n) ocurriría si todas las claves cayeran en el mismo bucket;
con djb2 + capacidad prima + factor de carga acotado, en la práctica los
buckets tienen 1–4 entradas (ver métricas abajo).

## Métricas registradas

`estadisticas()` devuelve un dataclass `EstadisticasTabla` con:

| Métrica | Significado |
|---------|-------------|
| `elementos` | Número de pares almacenados (n) |
| `capacidad` | Número de buckets (m) |
| `factor_carga` | n / m |
| `colisiones` | Veces que una inserción nueva cayó en un bucket ya ocupado (acumulado; las reinserciones internas del redimensionamiento no cuentan) |
| `buckets_usados` | Buckets con al menos una entrada |
| `bucket_maximo` | Longitud de la cadena más larga |

## Resultados reales

Con los 520 incidentes del escenario integrado:

```
Tabla hash:  520 elementos en 1361 buckets
  Factor de carga:  0.382
  Colisiones:       307
  Buckets usados:   484
  Bucket maximo:    3
```

Y el experimento de escalabilidad (500 búsquedas por fila, tiempos en ms):

| n | capacidad | carga | colisiones | buckets usados | máx | inserción | búsqueda hash | búsqueda lineal |
|---|-----------|-------|------------|----------------|-----|-----------|---------------|-----------------|
| 100 | 163 | 0.613 | 47 | 60 | 2 | 0.40 | 0.76 | 0.86 |
| 500 | 673 | 0.743 | 295 | 314 | 3 | 2.08 | 0.72 | 3.73 |
| 1 000 | 1 361 | 0.735 | 750 | 522 | 4 | 3.72 | 1.17 | 9.42 |
| 5 000 | 10 949 | 0.457 | 1 742 | 4 802 | 2 | 40.31 | 1.63 | 41.79 |
| 20 000 | 43 853 | 0.456 | 4 968 | 18 504 | 3 | 106.11 | 1.05 | 219.74 |

Lectura de los resultados:

* **La búsqueda es O(1) en la práctica**: el tiempo de las 500 búsquedas se
  mantiene alrededor de 1 ms sin importar si la tabla tiene 100 o 20 000
  claves, mientras la búsqueda lineal crece linealmente hasta 220 ms (unas
  **200 veces más lenta** con 20 000 elementos).
* **La cadena más larga nunca pasa de 4** aun con 20 000 claves, evidencia de
  que djb2 + capacidad prima distribuyen uniformemente.
* Las colisiones acumuladas (~25 % de las inserciones) son las esperadas para
  un factor de carga en torno a 0.5–0.75; lo importante es que no se
  concentran en pocos buckets.
* El costo de inserción crece de forma prácticamente lineal con n (O(1)
  amortizado por elemento, incluyendo los redimensionamientos intermedios).

## Reutilización en el sistema

Además de almacenar los incidentes en `main.py`, la `TablaHash` se reutiliza
en dos lugares:

1. `PriorityQueue` la usa como índice `id → posición en el heap` para poder
   actualizar prioridades en O(log n).
2. `reportes.zonas_mas_afectadas` la usa para contar incidentes por zona.
