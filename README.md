# Lesson 1.3 — Benchmarking de Algoritmos en Java

Proyecto Maven para comparar el rendimiento de dos implementaciones alternativas
de un mismo problema, midiendo tiempos de ejecución con distintos tamaños de entrada.

---

## Estructura del proyecto

```
lesson1_3/
├── src/
│   ├── main/java/com/lesson/   ← Implementaciones (lógica principal)
│   └── test/java/com/lesson/   ← Tests unitarios (JUnit 5)
├── benchmarks/
│   └── src/                    ← Clase BenchmarkRunner y utilidades
├── docs/
│   └── informe.md              ← Informe de resultados
├── pom.xml
└── README.md
```

---

## Requisitos

- Java 17+
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

Los resultados se imprimirán en consola en formato tabla CSV-compatible.

---

## Problema analizado

> **[A completar en la siguiente etapa]**

Se compararán dos implementaciones:
1. **Implementación A** — descripción
2. **Implementación B** — descripción

---

## Resultados rápidos

> Ver `docs/informe.md` para el análisis completo.

---

## Notas metodológicas

- Se ejecutan **N repeticiones** por tamaño de entrada (ver `BenchmarkRunner`).
- Se reporta la **mediana** para minimizar el efecto de outliers.
- La generación de datos de prueba **no se incluye** en la medición.
- El JVM se calienta con iteraciones previas (warm-up) antes de medir.
