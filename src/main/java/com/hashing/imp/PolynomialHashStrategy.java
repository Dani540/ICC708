package com.hashing.imp;

import com.hashing.out.HashStrategy;

// RF5 - hash polinomial con base 31: ((c1*31 + c2)*31 + c3)... + cn
public class PolynomialHashStrategy implements HashStrategy<String> {

    private static final int BASE = 31;

    @Override
    public int hash(String key) {
        int hash = 0;
        for (char c : key.toCharArray()) {
            hash = hash * BASE + c;
        }
        return hash;
    }
}
