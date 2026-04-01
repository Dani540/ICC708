package com.icc708;

public class Main {

    public static void main(String[] args) {
        AttentionSystem sistema = new AttentionSystem();

        Client ana = new Client("Ana");
        Client maria = new Client("Maria");
        Client carlos = new Client("Carlos");
        Client pedro = new Client("Pedro");
        Client lucia = new Client("Lucia");
        Client jorge = new Client("Jorge");
        Client camila = new Client("Camila");
        Client roberto = new Client("Roberto");
        Client valeria = new Client("Valeria");
        Client diego = new Client("Diego");

        System.out.println("=== Llegan clientes ===");
        sistema.processEvent(ana, EventType.NORMAL);
        sistema.processEvent(maria, EventType.NORMAL);
        sistema.processEvent(carlos, EventType.NORMAL);
        sistema.processEvent(pedro, EventType.NORMAL);
        sistema.processEvent(lucia, EventType.PRIORITARIO);
        sistema.processEvent(jorge, EventType.NORMAL);
        sistema.processEvent(camila, EventType.PRIORITARIO);
        sistema.processEvent(roberto, EventType.NORMAL);
        sistema.processEvent(valeria, EventType.PRIORITARIO);
        sistema.processEvent(diego, EventType.NORMAL);

        System.out.println("\n=== Cola: " + sistema.waitingClients() + " clientes en espera ===");
        sistema.showQueue();

        System.out.println("\n=== Se atienden los primeros 4 ===");
        sistema.processEvent(null, EventType.ATENDER);
        sistema.processEvent(null, EventType.ATENDER);
        sistema.processEvent(null, EventType.ATENDER);
        sistema.processEvent(null, EventType.ATENDER);

        System.out.println("\n=== Se cancela el último de la cola ===");
        sistema.processEvent(null, EventType.CANCELAR_ULTIMO);

        System.out.println("\n=== Se atiende el resto ===");
        while (sistema.waitingClients() > 0) {
            sistema.processEvent(null, EventType.ATENDER);
        }

        System.out.println("\n=== Intento atender con cola vacía ===");
        sistema.processEvent(null, EventType.ATENDER);

        System.out.println("\nClientes restantes: " + sistema.waitingClients());
    }
}
