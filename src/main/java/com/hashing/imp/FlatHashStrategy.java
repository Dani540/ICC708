package com.hashing.imp;

import com.hashing.out.HashStrategy;

public class FlatHashStrategy<T> implements HashStrategy<T> {

    @Override
    public int hash(T type) {
        return Math.abs(type.hashCode());
    }

}