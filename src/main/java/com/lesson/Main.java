package com.lesson;

import java.util.Arrays;
import java.util.Map;

/**
 * Punto de entrada para verificar manualmente el comportamiento
 * de ambas implementaciones de FrequencyCounter.
 *
 * No reemplaza los tests unitarios: su propósito es mostrar
 * la salida en consola de forma legible y confirmar que ambas
 * implementaciones producen el mismo resultado sobre un input concreto. 
**/

public class Main {

    public static void main(String[] args) {
        // Input con repeticiones variadas para que el conteo sea no trivial:
        // 1 aparece 3 veces, 2 dos veces, 3 cuatro veces.
        int[] data = {1, 2, 3, 1, 2, 1, 3, 3, 3};

        System.out.println("Input: " + Arrays.toString(data));
        System.out.println();

        // Ambas implementaciones se tratan a través de la interfaz común.
        // Esto demuestra que son intercambiables: el cliente no necesita
        // conocer los detalles internos de cada algoritmo.
        FrequencyCounter linear = new LinearCount();
        FrequencyCounter hash   = new HashCount();

        Map<Integer, Integer> resultLinear = linear.count(data);
        Map<Integer, Integer> resultHash   = hash.count(data);

        System.out.println("LinearCount → " + resultLinear);
        System.out.println("HashCount   → " + resultHash);

        System.out.println();
        // Verificación de correctitud: ambos mapas deben ser iguales
        // (mismas claves, mismos valores), independientemente del orden interno.
        System.out.println("Resultados iguales: " + resultLinear.equals(resultHash));
    }
}
