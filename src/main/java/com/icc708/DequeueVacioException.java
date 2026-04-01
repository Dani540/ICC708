package com.icc708;

public class DequeueVacioException extends RuntimeException {

    public DequeueVacioException(String operacion) {
        super("No se puede ejecutar '" + operacion + "': el deque está vacío.");
    }
}
