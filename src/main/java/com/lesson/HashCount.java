package com.lesson;

import java.util.HashMap;
import java.util.Map;

/**
 * Conteo de frecuencias con HashMap.
 *
 * Una sola pasada sobre el arreglo; cada elemento incrementa
 * directamente su contador en el mapa.
 * Complejidad temporal: O(n) promedio
 * Complejidad espacial: O(k), k = número de elementos únicos
 */
public class HashCount implements FrequencyCounter {

    @Override
    public Map<Integer, Integer> count(int[] data) {
        Map<Integer, Integer> result = new HashMap<>();

        for (int element : data) {
            result.merge(element, 1, Integer::sum);
        }

        return result;
    }
}
