package com.lesson;

import org.junit.jupiter.params.ParameterizedTest;
import org.junit.jupiter.params.provider.MethodSource;

import java.util.Map;
import java.util.stream.Stream;

import static org.junit.jupiter.api.Assertions.*;

class FrequencyCounterTest {

    static Stream<FrequencyCounter> implementations() {
        return Stream.of(new LinearCount(), new HashCount());
    }

    // --- Casos normales ---

    @ParameterizedTest
    @MethodSource("implementations")
    void casoNormal(FrequencyCounter counter) {
        int[] data = {1, 2, 3, 1, 2, 1};
        Map<Integer, Integer> result = counter.count(data);

        assertEquals(3, result.get(1));
        assertEquals(2, result.get(2));
        assertEquals(1, result.get(3));
        assertEquals(3, result.size());
    }

    @ParameterizedTest
    @MethodSource("implementations")
    void negativos(FrequencyCounter counter) {
        int[] data = {-1, -1, 2, -1};
        Map<Integer, Integer> result = counter.count(data);

        assertEquals(3, result.get(-1));
        assertEquals(1, result.get(2));
        assertEquals(2, result.size());
    }

    // --- Casos borde ---

    @ParameterizedTest
    @MethodSource("implementations")
    void entradaVacia(FrequencyCounter counter) {
        Map<Integer, Integer> result = counter.count(new int[]{});
        assertTrue(result.isEmpty());
    }

    @ParameterizedTest
    @MethodSource("implementations")
    void unSoloElemento(FrequencyCounter counter) {
        Map<Integer, Integer> result = counter.count(new int[]{7});

        assertEquals(1, result.size());
        assertEquals(1, result.get(7));
    }

    @ParameterizedTest
    @MethodSource("implementations")
    void todosIguales(FrequencyCounter counter) {
        int[] data = {4, 4, 4, 4};
        Map<Integer, Integer> result = counter.count(data);

        assertEquals(1, result.size());
        assertEquals(4, result.get(4));
    }

    @ParameterizedTest
    @MethodSource("implementations")
    void todosUnicos(FrequencyCounter counter) {
        int[] data = {10, 20, 30, 40};
        Map<Integer, Integer> result = counter.count(data);

        assertEquals(4, result.size());
        for (int element : data) {
            assertEquals(1, result.get(element));
        }
    }
}
