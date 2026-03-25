#!/usr/bin/env bash
set -e

echo "=== Compilando proyecto ==="
mvn compile -q

echo "=== Ejecutando Benchmark ==="
mvn exec:java -q
