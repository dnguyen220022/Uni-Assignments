import java.time.LocalDate;
import java.time.format.DateTimeFormatter;

public class Main
//Initialises a blank store object, and starts the menu for that store.
{
    public static void main(String[] args)
    {
        Store myStore = new Store();
        StoreMenu myStoreMenu = new StoreMenu(myStore);

        myStoreMenu.startMenuLoop();
    }
}

