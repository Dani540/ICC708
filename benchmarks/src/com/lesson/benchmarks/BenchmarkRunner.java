package com.lesson.benchmarks;

import com.lesson.FrequencyCounter;
import com.lesson.HashCount;
import com.lesson.LinearCount;

import java.util.Arrays;
import java.util.Random;

/**
 * Mide y compara el tiempo de ejecución de LinearCount y HashCount
 * sobre distintos tamaños de entrada.
 *
 * Protocolo:
 *  - 7 tamaños de entrada (ver SIZES).
 *  - 5 iteraciones de warm-up por implementación (no medidas) para que
 *    el JIT de Java compile los métodos antes de empezar a cronometrar.
 *  - 20 repeticiones medidas por implementación por tamaño.
 *  - Se reporta la MEDIANA de los tiempos (robusta frente a outliers
 *    causados por el GC o interrupciones del sistema operativo).
 *  - La generación de datos ocurre ANTES de la medición y no se contabiliza.
 *
 * Ejecutar con:
 *   mvn compile exec:java
 *
 * Nota: LinearCount es O(n²). Para n ≥ 30 000 cada repetición puede
 * tardar varios segundos; el progreso se imprime por tamaño para que
 * sea visible que el programa no se ha congelado.
 */
public class BenchmarkRunner {

    // Tamaños de entrada. El último valor (~50 000) hace que LinearCount
    // sea visiblemente lento, ilustrando la diferencia cuadrática vs lineal.
    private static final int[] SIZES = {100, 500, 1_000, 5_000, 10_000, 30_000, 50_000};

    // 20 repeticiones: suficiente para que la mediana sea estable,
    // sin disparar el tiempo total a niveles impracticables.
    private static final int REPETITIONS = 20;

    // Iteraciones de calentamiento: el JIT optimiza el bytecode tras
    // unas pocas ejecuciones; sin warm-up la primera medición puede
    // ser 5-10× más lenta que las siguientes.
    private static final int WARMUP = 5;

    public static void main(String[] args) {
        FrequencyCounter linear = new LinearCount();
        FrequencyCounter hash   = new HashCount();

        System.out.println("Benchmark — Conteo de Frecuencias");
        System.out.println("Repeticiones: " + REPETITIONS + " | Warm-up: " + WARMUP);
        System.out.println();
        System.out.printf("%-10s  %-20s  %-20s%n", "n", "LinearCount (ms)", "HashCount (ms)");
        System.out.println("-".repeat(54));

        for (int n : SIZES) {
            System.out.printf("Midiendo n = %-7d ...", n);
            System.out.flush(); // Mostrar progreso antes de que termine el cálculo

            // Generación de datos: fuera de la medición.
            // Rango [0, n/2) para forzar colisiones y que el conteo no sea trivial.
            // Semilla fija (42) para reproducibilidad entre ejecuciones.
            int[] data = generateData(n, 42);

            // Warm-up: ambas implementaciones se ejecutan sin medir
            for (int i = 0; i < WARMUP; i++) {
                linear.count(data);
                hash.count(data);
            }

            // Medición
            double medianLinearMs = nanosToMillis(measureMedian(linear, data));
            double medianHashMs   = nanosToMillis(measureMedian(hash,   data));

            System.out.printf("\r%-10d  %-20.3f  %-20.3f%n", n, medianLinearMs, medianHashMs);
        }
    }

    /**
     * Ejecuta {@code counter.count(data)} exactamente {@link #REPETITIONS} veces,
     * registra el tiempo de cada ejecución con System.nanoTime() y devuelve
     * la mediana de esos tiempos en nanosegundos.
     *
     * Se usa la mediana en lugar del promedio porque una pausa del GC o una
     * interrupción del SO puede inflar un único sample sin representar el
     * comportamiento típico del algoritmo.
     */
    private static long measureMedian(FrequencyCounter counter, int[] data) {
        long[] times = new long[REPETITIONS];

        for (int i = 0; i < REPETITIONS; i++) {
            long start = System.nanoTime();
            counter.count(data);
            times[i] = System.nanoTime() - start;
        }

        Arrays.sort(times);

        // Con número par de muestras, la mediana es el promedio de los dos centrales.
        int mid = REPETITIONS / 2;
        return (times[mid - 1] + times[mid]) / 2;
    }

    /**
     * Genera un arreglo de {@code n} enteros aleatorios en [0, n/2).
     *
     * @param n    tamaño del arreglo
     * @param seed semilla del generador (fija para reproducibilidad)
     */
    private static int[] generateData(int n, long seed) {
        Random rng = new Random(seed);
        int[] data = new int[n];
        int range = Math.max(1, n / 2);
        for (int i = 0; i < n; i++) {
            data[i] = rng.nextInt(range);
        }
        return data;
    }

    private static double nanosToMillis(long nanos) {
        return nanos / 1_000_000.0;
    }
}
