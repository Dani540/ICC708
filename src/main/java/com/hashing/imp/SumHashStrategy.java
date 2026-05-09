package com.hashing.imp;

import com.hashing.out.HashStrategy;

// RF4 - hash por suma de codigos ASCII/Unicode de cada caracter
public class SumHashStrategy implements HashStrategy<String> {

    @Override
    public int hash(String key) {
        int sum = 0;
        for (char c : key.toCharArray()) {
            sum += c;
        }
        return sum;
    }
}
