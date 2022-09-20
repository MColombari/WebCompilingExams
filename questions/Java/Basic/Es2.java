/* -- "Difficult", weight: '1'
/* 'Realizza una classe Esercizio a cui si passi nel costruttore due numeri interi, ' */
/* 'tale classe deve avere una funzione run che ritorni il prodotto dei due numeri' */


public class Es2{
    public static void main(String[] args) {
        Esercizio e1 = new Esercizio(1,2);
        Esercizio e2 = new Esercizio(2,-2);
        if (e1.run() == 2){
            if (e2.run() == -4){
                System.out.println("..\nTest eseguiti con successo.");
            }
            else{
                System.out.println(".F\nUn test fallito.");
            }
        }
        else {
            System.out.println("FF\nTest falliti.");
        }
    }
}