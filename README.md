# Dequeue — Sistema de Atención Ciudadana

## ¿Qué implementamos?

Un sistema de atención ciudadana que maneja una cola con dos extremos (Deque: *Double-Ended Queue*).

A diferencia de una cola normal, este sistema permite agregar y retirar elementos tanto por el frente como por el final. Esto hace posible distinguir entre clientes normales, que esperan su turno al final de la fila, y clientes prioritarios, que se ubican directamente al inicio.

La estructura se construye con **nodos**: cada cliente en la cola es un nodo que conoce quién tiene adelante y quién tiene atrás. Manipulando esos vínculos entre nodos es como se logra insertar o retirar en cualquier extremo de forma eficiente, sin mover al resto de la fila.

### Eventos que maneja el sistema

| Evento | Efecto |
|---|---|
| `NORMAL` | El cliente se agrega al final de la cola |
| `PRIORITARIO` | El cliente se agrega al inicio de la cola |
| `ATENDER` | Se atiende al primer cliente de la cola |
| `CANCELAR_ULTIMO` | Se retira al último cliente de la cola |

## Cómo correr el programa

**Requisitos:** Java 17+ y Maven 3.6+

```bash
# Compilar
mvn compile

# Ejecutar
mvn exec:java "-Dexec.mainClass=com.icc708.Main"
```
