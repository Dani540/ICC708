package com.hashing;

import com.hashing.imp.HashTable;
import com.hashing.imp.SumHashStrategy;
import com.hashing.imp.PolynomialHashStrategy;

import java.util.Random;

public class Main {

    static final int TABLE_SIZE   = 1009;
    static final int DATASET_SIZE = 1000;
    static final int KEY_LENGTH   = 8;

    public static void main(String[] args) {
        String[] random     = generateRandom(DATASET_SIZE, KEY_LENGTH);
        String[] sequential = generateSequential(DATASET_SIZE);
        String[] grouped    = generateGrouped(DATASET_SIZE);

        System.out.println("============================================================");
        System.out.println("  Comparacion de funciones hash - Laboratorio 5.1");
        System.out.println("  Tamanio de tabla: " + TABLE_SIZE + "  |  Elementos: " + DATASET_SIZE);
        System.out.println("============================================================");
        System.out.println();

        runComparison("Aleatorio (strings random, largo 8)", random);
        runComparison("Secuencial (user0 .. user999)       ", sequential);
        runComparison("Agrupado   (aaa0  ..  aaa999)       ", grouped);
    }

    static void runComparison(String label, String[] keys) {
        System.out.println("Dataset: " + label.trim());

        HashTable<Integer> sumTable  = new HashTable<>(TABLE_SIZE, new SumHashStrategy());
        HashTable<Integer> polyTable = new HashTable<>(TABLE_SIZE, new PolynomialHashStrategy());

        long start = System.nanoTime();
        for (int i = 0; i < keys.length; i++) sumTable.insert(keys[i], i);
        long sumNs = System.nanoTime() - start;

        start = System.nanoTime();
        for (int i = 0; i < keys.length; i++) polyTable.insert(keys[i], i);
        long polyNs = System.nanoTime() - start;

        HashTable.Report sumR  = sumTable.getReport();
        HashTable.Report polyR = polyTable.getReport();

        // Encabezado de tabla
        String fmt = "  %-16s | %11s | %13s | %15s | %12s | %12s";
        System.out.println(String.format(fmt,
            "Funcion", "Colisiones", "Factor carga", "Buckets usados", "Bucket max", "Tiempo (ms)"));
        System.out.println("  " + "-".repeat(88));
        printRow("hashSum",        sumR,  sumNs);
        printRow("hashPolynomial", polyR, polyNs);
        System.out.println();
    }

    static void printRow(String name, HashTable.Report r, long nanos) {
        System.out.printf("  %-16s | %11d | %13.4f | %15d | %12d | %12.3f%n",
            name, r.collisions, r.loadFactor, r.usedBuckets, r.maxBucketSize, nanos / 1_000_000.0);
    }

    // Genera n strings aleatorios de longitud len usando semilla fija (reproducible)
    static String[] generateRandom(int n, int len) {
        Random rng = new Random(42);
        String chars = "abcdefghijklmnopqrstuvwxyz0123456789";
        String[] keys = new String[n];
        for (int i = 0; i < n; i++) {
            StringBuilder sb = new StringBuilder(len);
            for (int j = 0; j < len; j++) sb.append(chars.charAt(rng.nextInt(chars.length())));
            keys[i] = sb.toString();
        }
        return keys;
    }

    // user0, user1, ..., user999
    static String[] generateSequential(int n) {
        String[] keys = new String[n];
        for (int i = 0; i < n; i++) keys[i] = "user" + i;
        return keys;
    }

    // aaa0, aaa1, ..., aaa999
    static String[] generateGrouped(int n) {
        String[] keys = new String[n];
        for (int i = 0; i < n; i++) keys[i] = "aaa" + i;
        return keys;
    }
}
