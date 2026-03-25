package com.lesson;

import java.util.HashMap;
import java.util.Map;

/**
 * Conteo de frecuencias por búsqueda lineal.
 *
 * Para cada elemento único, recorre el arreglo completo contando ocurrencias.
 * Complejidad temporal: O(n²)
 * Complejidad espacial: O(k), k = número de elementos únicos
 */
public class LinearCount implements FrequencyCounter {

    @Override
    public Map<Integer, Integer> count(int[] data) {
        Map<Integer, Integer> result = new HashMap<>();

        for (int i = 0; i < data.length; i++) {
            int element = data[i];

            // Saltar si este elemento ya fue contado
            if (result.containsKey(element)) {
                continue;
            }

            // Contar cuántas veces aparece element en todo el arreglo
            int occurrences = 0;
            for (int j = 0; j < data.length; j++) {
                if (data[j] == element) {
                    occurrences++;
                }
            }

            result.put(element, occurrences);
        }

        return result;
    }
}
