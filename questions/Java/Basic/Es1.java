/*Easy-'Realizza una classe Esercizio a cui si passi nel costruttore due numeri interi, tale classe deve avere una funzione
run che ritorni la somma dei due numeri'*/


public class Es1{
    public static void main(String[] args) {
	    Sum es = new Sum(1,2);
        if (es.run() == 3){
            System.out.println("Test eseguiti con successo.");
        }
        else {
            System.out.println("Test falliti.");
        }
    }
}