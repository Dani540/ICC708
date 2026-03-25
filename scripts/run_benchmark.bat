@echo off
echo === Compilando proyecto ===
call mvn compile -q
if errorlevel 1 (
    echo ERROR: Falló la compilación
    exit /b 1
)

echo === Ejecutando Benchmark ===
call mvn exec:java -q
