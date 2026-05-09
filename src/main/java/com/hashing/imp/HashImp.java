package com.hashing.imp;

import com.hashing.out.HashStrategy;

public class HashImp<K, V> {

    private static final int DEFAULT_CAPACITY = 16;

    private Node<K, V>[] buckets;
    private int capacity;
    private int size;
    private HashStrategy<K> strategy;

    @SuppressWarnings("unchecked")
    public HashImp(int capacity, HashStrategy<K> strategy) {
        this.capacity = capacity;
        this.buckets = new Node[capacity];
        this.strategy = strategy;
        this.size = 0;
    }

    public HashImp() {
        this(DEFAULT_CAPACITY, new FlatHashStrategy<>());
    }

    // Convierte el hash raw en un índice válido para el array
    private int bucketIndex(K key) {
        return strategy.hash(key) % capacity;
    }

    // Inserta o actualiza. Retorna true si actualizó, false si insertó nuevo.
    public boolean put(K key, V value) {
        int index = bucketIndex(key);
        Node<K, V> current = buckets[index];

        while (current != null) {
            if (current.key.equals(key)) {
                current.value = value;
                return true;
            }
            current = current.next;
        }

        // No existe: agregar al inicio de la lista en este bucket
        Node<K, V> newNode = new Node<>(key, value);
        newNode.next = buckets[index];
        buckets[index] = newNode;
        size++;
        return false;
    }

    // Retorna el valor asociado a la key, o null si no existe.
    public V get(K key) {
        int index = bucketIndex(key);
        Node<K, V> current = buckets[index];

        while (current != null) {
            if (current.key.equals(key)) {
                return current.value;
            }
            current = current.next;
        }
        return null;
    }

    // Elimina la entrada con esa key. Retorna true si la encontró y eliminó.
    public boolean remove(K key) {
        int index = bucketIndex(key);
        Node<K, V> current = buckets[index];
        Node<K, V> prev = null;

        while (current != null) {
            if (current.key.equals(key)) {
                if (prev == null) {
                    buckets[index] = current.next;
                } else {
                    prev.next = current.next;
                }
                size--;
                return true;
            }
            prev = current;
            current = current.next;
        }
        return false;
    }

    public boolean contains(K key) {
        return get(key) != null;
    }

    public int size() {
        return size;
    }

    public boolean isEmpty() {
        return size == 0;
    }
}
