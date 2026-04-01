package com.icc708;


public class Dequeue<T> {

    private class Node {
        T data;
        Node prev;
        Node next;

        Node(T data) {
            this.data = data;
        }
    }

    private Node head;
    private Node tail;
    private int size;

    public void addFirst(T data) {
        Node node = new Node(data);
        if (isEmpty()) {
            head = tail = node;
        } else {
            node.next = head;
            head.prev = node;
            head = node;
        }
        size++;
    }

    public void addLast(T data) {
        Node node = new Node(data);
        if (isEmpty()) {
            head = tail = node;
        } else {
            node.prev = tail;
            tail.next = node;
            tail = node;
        }
        size++;
    }

    public T removeFirst() {
        if (isEmpty()) throw new DequeueVacioException("removeFirst");
        T data = head.data;
        if (head == tail) {
            head = tail = null;
        } else {
            head = head.next;
            head.prev = null;
        }
        size--;
        return data;
    }

    public T removeLast() {
        if (isEmpty()) throw new DequeueVacioException("removeLast");
        T data = tail.data;
        if (head == tail) {
            head = tail = null;
        } else {
            tail = tail.prev;
            tail.next = null;
        }
        size--;
        return data;
    }

    public T peekFirst() {
        if (isEmpty()) throw new DequeueVacioException("peekFirst");
        return head.data;
    }

    public T peekLast() {
        if (isEmpty()) throw new DequeueVacioException("peekLast");
        return tail.data;
    }

    public boolean isEmpty() {
        return size == 0;
    }

    public int size() {
        return size;
    }
}
