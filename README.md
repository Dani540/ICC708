# Taller de Programación Dinámica - Problema de la Mochila 0/1

**Programación Avanzada · ICC708**

Solución completa del problema de la Mochila 0/1 (*0/1 Knapsack*) usando Programación
Dinámica, con implementación, reconstrucción de la solución, visualización de la tabla,
experimentos y análisis de complejidad.

---

## Estructura del proyecto

| Archivo | Contenido |
|---|---|
| `mochila_dp.py` | **Partes A, B y C.** Algoritmo DP *bottom-up*, reconstrucción de la solución óptima e impresión de la tabla dinámica. Es el archivo principal para estudiar. |
| `mochila_memoization.py` | **Desafío opcional.** Versión *top-down* (recursión + memoization). |
| `experimentos.py` | **Partes D y E.** Datasets aleatorios, mediciones (tiempo, tamaño de tabla, valor óptimo), comparación de enfoques y generación de gráficos. |
| `INFORME.md` | Informe técnico (introducción, diseño, resultados, análisis y conclusiones). |
| `tiempo_vs_n.png`, `tiempo_vs_w.png`, `bottomup_vs_topdown.png` | Gráficos generados por `experimentos.py`. |

---

## Requisitos

- **Python 3.9 o superior** (probado con Python 3.13).
- **matplotlib** (solo para generar los gráficos de la Parte D).

Instalar matplotlib (si no lo tienes):

```bash
pip install matplotlib
```

> Nota: `mochila_dp.py` y `mochila_memoization.py` **no** requieren matplotlib.
> Solo `experimentos.py` lo usa, y si no está instalado, igual corre los experimentos
> y solo omite los gráficos.

---

## Cómo ejecutar

Desde la carpeta del proyecto:

**1) Partes A, B y C - algoritmo, reconstrucción y tabla (dataset del taller):**

```bash
python mochila_dp.py
```

**2) Desafío opcional - versión top-down con memoization:**

```bash
python mochila_memoization.py
```

**3) Partes D y E - experimentos, mediciones y gráficos:**

```bash
python experimentos.py
```

---
