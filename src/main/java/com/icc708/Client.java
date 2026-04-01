package com.icc708;

public record Client(String name) {
    @Override
    public String toString() {
        return name;
    }
}
