package com.hashing.imp;

import com.hashing.out.HashStrategy;

public class HashTable<V> {

    private static final int BASE = 31;

    private Node<String, V>[] buckets;
    private int capacity;
    private int size;
    private int collisions;           // RF6 - contador de colisiones
    private HashStrategy<String> strategy;

    @SuppressWarnings("unchecked")
    public HashTable(int capacity, HashStrategy<String> strategy) {
        this.capacity = capacity;
        this.buckets = new Node[capacity];
        this.strategy = strategy;
    }

    // RF4 - indice por suma de caracteres
    public int hashSum(String key) {
        int sum = 0;
        for (char c : key.toCharArray()) sum += c;
        return sum % capacity;
    }

    // RF5 - indice por acumulacion polinomial base 31
    public int hashPolynomial(String key) {
        int hash = 0;
        for (char c : key.toCharArray()) hash = hash * BASE + c;
        return (hash & 0x7fffffff) % capacity;
    }

    // Convierte el hash raw de la estrategia en indice de bucket
    private int bucketIndex(String key) {
        int raw = strategy.hash(key);
        return (raw & 0x7fffffff) % capacity;
    }

    // RF1 - inserta o actualiza; retorna true si fue actualizacion
    public boolean insert(String key, V value) {
        int index = bucketIndex(key);
        Node<String, V> current = buckets[index];

        while (current != null) {
            if (current.key.equals(key)) {
                current.value = value;
                return true;
            }
            current = current.next;
        }

        // RF6 - hay colision si el bucket ya tiene al menos un nodo distinto
        if (buckets[index] != null) {
            collisions++;
        }

        Node<String, V> newNode = new Node<>(key, value);
        newNode.next = buckets[index];
        buckets[index] = newNode;
        size++;
        return false;
    }

    // RF2 - busca una clave; retorna null si no existe
    public V search(String key) {
        int index = bucketIndex(key);
        Node<String, V> current = buckets[index];
        while (current != null) {
            if (current.key.equals(key)) return current.value;
            current = current.next;
        }
        return null;
    }

    // RF3 - elimina una clave; retorna true si existia
    public boolean delete(String key) {
        int index = bucketIndex(key);
        Node<String, V> current = buckets[index];
        Node<String, V> prev = null;

        while (current != null) {
            if (current.key.equals(key)) {
                if (prev == null) buckets[index] = current.next;
                else prev.next = current.next;
                size--;
                return true;
            }
            prev = current;
            current = current.next;
        }
        return false;
    }

    public int getCollisions() { return collisions; }
    public int size()          { return size; }
    public boolean isEmpty()   { return size == 0; }

    // RF7 - calcula y retorna todas las metricas
    public Report getReport() {
        int usedBuckets = 0;
        int maxBucketSize = 0;

        for (Node<String, V> head : buckets) {
            if (head != null) {
                usedBuckets++;
                int count = 0;
                for (Node<String, V> n = head; n != null; n = n.next) count++;
                if (count > maxBucketSize) maxBucketSize = count;
            }
        }
        return new Report(size, capacity, collisions, usedBuckets, maxBucketSize);
    }

    public static class Report {
        public final int size;
        public final int capacity;
        public final int collisions;
        public final int usedBuckets;
        public final int maxBucketSize;
        public final double loadFactor;

        Report(int size, int capacity, int collisions, int usedBuckets, int maxBucketSize) {
            this.size = size;
            this.capacity = capacity;
            this.collisions = collisions;
            this.usedBuckets = usedBuckets;
            this.maxBucketSize = maxBucketSize;
            this.loadFactor = (double) size / capacity;
        }
    }
}
