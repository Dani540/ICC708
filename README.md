# Lesson 1.3 — Benchmarking de Algoritmos en Java

Proyecto Maven para comparar el rendimiento de dos implementaciones alternativas
de un mismo problema, midiendo tiempos de ejecución con distintos tamaños de entrada.

---

## Estructura del proyecto

```text
lesson1_3/
├── src/
│   ├── main/java/com/lesson/
│   │   ├── FrequencyCounter.java       ← Interfaz común
│   │   ├── LinearCount.java            ← Implementación O(n²)
│   │   ├── HashCount.java              ← Implementación O(n)
│   │   ├── Main.java                   ← Verificación manual en consola
│   │   └── benchmarks/
│   │       └── BenchmarkRunner.java    ← Medición de rendimiento
│   └── test/java/com/lesson/
│       └── FrequencyCounterTest.java   ← Tests unitarios (JUnit 5)
├── docs/
│   └── informe.md              ← Informe de resultados con tabla
├── scripts/
│   ├── run_benchmark.bat       ← Atajo Windows
│   └── run_benchmark.sh        ← Atajo Linux/macOS
├── pom.xml
└── README.md
```

---

## Requisitos

- Java 21+
- Maven 3.8+

Verificar instalación:

```bash
java -version
mvn -version
```

---

## Ejecutar tests

```bash
mvn test
```

Los resultados aparecen en la consola y en `target/surefire-reports/`.

---

## Ejecutar benchmark

### Opción A — con Maven (recomendado)

```bash
mvn compile exec:java
```

### Opción B — compilar y ejecutar el JAR

```bash
mvn package
java -jar target/lesson1_3-1.0-SNAPSHOT.jar
```

### Opción C — script de conveniencia

```bash
# Windows
scripts/run_benchmark.bat

# Linux / macOS
bash scripts/run_benchmark.sh
```

Los resultados se imprimirán en consola como tabla.

---

## Problema analizado

**Conteo de frecuencias:** dado un arreglo de `n` enteros, construir un mapa
`elemento → número de ocurrencias`.

Se comparan dos implementaciones:

1. **LinearCount** — búsqueda lineal por cada elemento único. O(n²).
2. **HashCount** — una sola pasada con `HashMap`. O(n) promedio.

---

## Resultados rápidos

| n      | LinearCount (ms) | HashCount (ms) |
|--------|------------------|----------------|
| 100    | 0,088            | 0,056          |
| 1 000  | 0,489            | 0,190          |
| 10 000 | 14,306           | 0,250          |
| 50 000 | 341,374          | 1,979          |

Ver `docs/informe.md` para la tabla completa y el análisis.

---

## Notas metodológicas

- Se ejecutan **20 repeticiones** por tamaño de entrada.
- Se reporta la **mediana** para minimizar el efecto de outliers.
- La generación de datos **no se incluye** en la medición.
- Se realizan **5 iteraciones de warm-up** antes de medir (calentamiento del JIT).

---

## Glosario

**Benchmark**
Experimento controlado que mide el rendimiento de un programa bajo condiciones definidas. El objetivo es obtener tiempos comparables y reproducibles, no simplemente "ver si corre".

**Mediana**
Valor central de un conjunto de datos ordenados. Si se tienen 20 tiempos medidos, la mediana es el promedio de los dos valores en las posiciones 10 y 11 una vez ordenados de menor a mayor. Es preferible al promedio cuando hay valores extremos (outliers) que distorsionarían el resultado.

**Outlier**
Valor atípico que se aleja significativamente del resto. En benchmarking, una pausa del recolector de basura (GC) durante una medición puede producir un tiempo 10× mayor al habitual. La mediana descarta ese efecto; el promedio no.

**Warm-up (calentamiento)**
Ejecuciones previas a la medición que no se contabilizan. La JVM de Java incluye un compilador JIT que optimiza el código en tiempo de ejecución: las primeras llamadas a un método son más lentas porque aún no han sido compiladas a código nativo. El warm-up garantiza que las mediciones reflejen el rendimiento estable, no el arranque.

**JIT (Just-In-Time compiler)**
Componente de la JVM que convierte el bytecode de Java a instrucciones nativas del procesador durante la ejecución, en lugar de hacerlo todo antes de correr el programa. Produce código altamente optimizado, pero requiere un período de calentamiento inicial.

**Complejidad temporal O(n)**
Notación que describe cómo crece el tiempo de ejecución en función del tamaño de entrada `n`. O(n) significa crecimiento lineal (duplicar `n` duplica el tiempo); O(n²) significa crecimiento cuadrático (duplicar `n` cuadruplica el tiempo).

**HashMap**
Estructura de datos que almacena pares clave-valor y permite buscar, insertar y actualizar en tiempo O(1) promedio mediante una función hash. En Java es parte de la biblioteca estándar (`java.util.HashMap`).
