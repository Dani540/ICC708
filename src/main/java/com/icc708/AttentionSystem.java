package com.icc708;

public class AttentionSystem {

    private final Dequeue<Client> doblecola = new Dequeue<>();

    public void processEvent(Client subject, EventType evento) {
        switch (evento) {
            case NORMAL          -> addNormal(subject);
            case PRIORITARIO     -> addPriority(subject);
            case ATENDER         -> serve();
            case CANCELAR_ULTIMO -> cancelLast();
        }
    }

    public void addNormal(Client cliente) {
        doblecola.addLast(cliente);
        System.out.println("NORMAL agregado al final: " + cliente);
    }

    public void addPriority(Client cliente) {
        doblecola.addFirst(cliente);
        System.out.println("PRIORITARIO agregado al inicio: " + cliente);
    }

    public Client serve() {
        try {
            Client cliente = doblecola.removeFirst();
            System.out.println("Atendiendo: " + cliente);
            return cliente;
        } catch (DequeueVacioException e) {
            System.out.println("No se puede atender: " + e.getMessage());
            return null;
        }
    }

    public Client cancelLast() {
        try {
            Client cliente = doblecola.removeLast();
            System.out.println("Cancelado último: " + cliente);
            return cliente;
        } catch (DequeueVacioException e) {
            System.out.println("No se puede cancelar: " + e.getMessage());
            return null;
        }
    }

    public void showQueue() {
        System.out.println("Orden en cola: " + doblecola);
    }

    public int waitingClients() {
        return doblecola.size();
    }
}
