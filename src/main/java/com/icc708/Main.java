package com.icc708;

public class Main {

    public static void main(String[] args) {
        AttentionSystem sistema = new AttentionSystem();
        Client anaClient = new Client("Ana");
        Client mariaClient = new Client("Maria");
        Client carlosClient = new Client("Carlos");
        Client pedroClient = new Client("Pedro");

        sistema.processEvent(anaClient, EventType.NORMAL);
        sistema.processEvent(mariaClient, EventType.NORMAL);
        sistema.processEvent(carlosClient, EventType.PRIORITARIO);
        sistema.processEvent(pedroClient, EventType.NORMAL);

        System.out.println("---");
        sistema.processEvent(anaClient, EventType.ATENDER);
        sistema.processEvent(mariaClient, EventType.CANCELAR_ULTIMO);
        sistema.processEvent(carlosClient, EventType.ATENDER);
        sistema.processEvent(pedroClient, EventType.ATENDER);

        System.out.println("Clientes restantes: " + sistema.waitingClients());
    }
}
