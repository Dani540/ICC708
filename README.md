# Laboratorio 5.1 — Hashing en Estructuras de Datos

**Curso:** Programación Avanzada ICC708  
**Tema:** Comparación de funciones hash, colisiones y rendimiento empírico

---

## 1. Estructura implementada

Se implementó una tabla hash con **encadenamiento separado** (*separate chaining*) desde cero en Java, sin usar ninguna estructura de datos de la biblioteca estándar (`HashMap`, `LinkedList`, etc.).

La tabla está compuesta por tres capas:

- **`HashStrategy<T>`** — interfaz que define el contrato de cualquier función hash. Retorna un `int` con el hash crudo (sin módulo), lo que permite que distintas estrategias sean intercambiables sin modificar la tabla (Patrón de diseño "Strategy").
- **`Node<K, V>`** — nodo de lista enlazada que almacena la clave, el valor y una referencia `next` al siguiente nodo del mismo bucket. Es la unidad base del encadenamiento (inspirada en las listas enlazadas diseñadas en laboratorios anteriores).
- **`HashTable<V>`** — la tabla propiamente dicha. Internamente mantiene un arreglo `Node<String, V>[] buckets` de tamaño fijo. El índice de cada clave se calcula como `(hash_crudo & 0x7fffffff) % capacidad`( donde el AND con `0x7fffffff` elimina el bit de signo para evitar índices negativos producidos por desbordamiento de enteros, recomendación de la IA que valía la pena incluir).

### Operaciones implementadas

| Código (enunciado de lab) | Método | Comportamiento |
| --- | --- | --- |
| RF1 | `insert(key, value)` | Recorre el bucket en busca de la clave. Si existe, actualiza el valor. Si no, agrega un nuevo nodo al inicio de la lista. Registra colisión si el bucket ya contenía al menos un nodo distinto. |
| RF2 | `search(key)` | Recorre el bucket hasta encontrar la clave. Retorna el valor o `null` si no existe. |
| RF3 | `delete(key)` | Recorre el bucket con puntero doble (`prev` / `current`) para reconectar la cadena al eliminar. Retorna `true` si la clave existía. |
| RF4 | `hashSum(key)` | Índice por suma de caracteres módulo capacidad. |
| RF5 | `hashPolynomial(key)` | Índice por acumulación polinomial base 31 módulo capacidad. |
| RF6 | `getCollisions()` | Retorna el contador de colisiones acumulado desde la construcción. |
| RF7 | `getReport()` | Calcula y retorna tamaño, factor de carga, colisiones, buckets usados, bucket máximo. |

---

## 2. Funciones hash

### hashSum — suma de caracteres

```text
h_sum(key) = (Σ código_unicode(cᵢ)) mod m
```

Suma los valores enteros de cada carácter y aplica módulo por el tamaño de la tabla. **No considera el orden** de los caracteres: `"abc"` y `"bca"` producen el mismo hash. Además, con claves estructuralmente similares (mismo prefijo, sufijo numérico variable), los valores de hash caen en un rango muy estrecho.

### hashPolynomial — acumulación polinomial base 31

```text
h_poly(key) = (c₁·31ⁿ⁻¹ + c₂·31ⁿ⁻² + ... + cₙ) mod m
```

Equivalentemente, en cada paso: `hash = hash × 31 + cᵢ`

Cada carácter recibe un peso proporcional a su posición: el primer carácter queda multiplicado por la mayor potencia de 31, y el último no se multiplica. Esto hace que el orden importe: `"abc"` ≠ `"bca"`. La base 31 es un número primo pequeño que minimiza colisiones sistemáticas al repartir mejor los residuos módulo `m`.

No se usó `String.hashCode()` de Java; ambas funciones son implementaciones propias (aunque internamente la función `hashCode()` también usa éste valor).

---

## 3. Datos de prueba

Se usaron 1000 claves por dataset con tabla de tamaño **1009** (número primo) para los tres experimentos.

| Dataset | Descripción | Ejemplo de claves |
| --- | --- | --- |
| Aleatorio | 1000 strings de largo 8, caracteres a–z y 0–9, semilla fija 42 | `k7mxq3ab`, `zt19wcnr` |
| Secuencial | Prefijo fijo + índice incremental | `user0`, `user1`, …, `user999` |
| Agrupado | Prefijo común de chars repetidos + índice incremental | `aaa0`, `aaa1`, …, `aaa999` |

---

## 4. Resultados

| Dataset | Función | Colisiones | Factor de carga | Buckets usados | Bucket máx | Tiempo (ms) |
| --- | --- | --- | --- | --- | --- | --- |
| Aleatorio | `hashSum` | 693 | 0.9911 | 307 | 13 | 1.19 |
| Aleatorio | `hashPolynomial` | 370 | 0.9911 | 630 | 6 | 0.56 |
| Secuencial | `hashSum` | **945** | 0.9911 | **55** | **70** | 0.49 |
| Secuencial | `hashPolynomial` | 428 | 0.9911 | 572 | 4 | 0.17 |
| Agrupado | `hashSum` | **945** | 0.9911 | **55** | **70** | 0.48 |
| Agrupado | `hashPolynomial` | 419 | 0.9911 | 581 | 4 | 0.25 |

---

## 5. Tópico

`hashPolynomial` produjo consistentemente menos colisiones en los tres datasets. La diferencia más marcada se observó en los datos **secuenciales y agrupados**, donde `hashSum` alcanzó 945 colisiones (el 94.5% de las inserciones colisionaron) frente a 428–419 de `hashPolynomial` (42–43%).

**¿Por qué entonces hashSum falla con datos estructurados?**

Para `user0` … `user999`, el prefijo `"user"` contribuye siempre la misma suma (117 + 115 + 101 + 114 = 447). Lo único que varía son los sufijos numéricos, cuyos códigos Unicode van de 48 (`'0'`) a 57 (`'9'`). Eso produce hashes como 495, 496, …, 504 para `user0`–`user9`; luego 544–553 para `user10`–`user19`, etc. Los valores caen en un rango estrecho y concentrado, de modo que al aplicar módulo 1009 solo se activan 55 de los 1009 buckets disponibles. El bucket más cargado acumuló **70 nodos**, lo que convierte la búsqueda en ese bucket en una operación O(70) en vez de O(1), lo que significa una complijidad temporal O(N) en el peor de los casos.

El caso agrupado (`aaa0`…`aaa999`) produce exactamente el mismo patrón de colisiones porque la distribución de los sufijos numéricos es idéntica: solo cambia el valor de base de la suma (97×3 = 291 en vez de 447), pero la estructura del problema bajo módulo 1009 es la misma.

**¿Por qué hashPolynomial se comporta mejor?**

Cada carácter recibe un peso diferente según su posición. Para `"user0"`, el resultado es aproximadamente `u·31⁴ + s·31³ + e·31² + r·31 + 48`. Al cambiar `'0'` por `'1'` (pasar de `user0` a `user1`), la diferencia en el hash es exactamente 1 (49 − 48). Pero al pasar a `user10`, la cadena crece a 6 caracteres: todos los pesos anteriores se multiplican por un 31 adicional y se suma la contribución del `'1'` nuevo (49 × 31 = 1.519). El salto total supera los 100.000, frente al 1 del ejemplo anterior. Ese efecto multiplicativo dispersa las claves por un rango de valores mucho más amplio antes de aplicar el módulo, ocupando 572–630 buckets con un máximo de solo 4–6 nodos por bucket.

---

## 6. Conclusión técnica

El experimento demuestra que el diseño de la función hash tiene un impacto directo y medible sobre el rendimiento de la tabla. `hashPolynomial` superó a `hashSum` en los tres datasets, y la diferencia fue más pronunciada con datos estructurados: con claves secuenciales y agrupadas, `hashSum` concentró 1000 claves en apenas 55 de los 1009 buckets disponibles, generando un bucket máximo de 70 elementos. `hashPolynomial`, en cambio, distribuyó las mismas claves en más de 570 buckets con un máximo de 4 elementos. La causa raíz del problema de `hashSum` es su naturaleza conmutativa: al ignorar el orden de los caracteres, produce un rango estrecho de valores para claves con prefijo común, lo que genera agrupamiento sistemático. `hashPolynomial` evita esto al ponderar cada carácter según su posición mediante potencias de 31, efectivamente tratando la cadena como un número en base 31. El uso de un tamaño de tabla primo (1009) también contribuyó a una distribución más uniforme, ya que reduce la probabilidad de colisiones sistemáticas por factores comunes entre los hashes y la capacidad. Ambas funciones usaron encadenamiento separado, lo que evitó la pérdida de datos incluso con alto nivel de colisiones, pero la mala distribución de `hashSum` convierte búsquedas que deberían ser O(1) en O(70) para los buckets más cargados. Finalmente, operar con un factor de carga de 0.99 evidencia que en un sistema productivo sería necesario implementar rehashing dinámico antes de alcanzar esa saturación para mantener las garantías de rendimiento.
