import java.time.LocalDate;
import java.time.format.DateTimeFormatter;
import java.util.ArrayList;
import java.util.Scanner;

public class StoreMenu
    // Name: Daniel Nguyen
    // Student Number: 32471033
    // Version: 1.0
    //
    //Creates class for user menu function, allowing multiple menus to be created for different stores independantly.
    //has all methods needed for menu function, including the menu loop.
{
    private Store myStore;
    private Boolean exitBool;

    public StoreMenu(Store store)
    //non-default constructor
    {
        this.myStore = store;
    }

    public void addCustomer()
    //allow user to add customer to the system
    {
        Scanner sc = new Scanner(System.in);
        System.out.println("Please enter the name of the customer.");
        String customerName = sc.nextLine();
        customerName = customerName.toUpperCase();

        myStore.addCustomer(customerName);

        System.out.println("A new customer with the name: " + customerName + ", has been added to the system.\n");
    }

    public void addOrder()
    //allow user to add order to system
    {
        InputValidator inputCheck;
        Boolean validInput;
        Integer customerNumber = -1;
        ArrayList<Item> itemList = new ArrayList<Item>();
        LocalDate orderDate = LocalDate.now();

        Scanner sc = new Scanner(System.in);

        //get customer number
        validInput = Boolean.FALSE;
        while(validInput.equals(Boolean.FALSE))
        {
            myStore.displayCustomers();
            System.out.println("Please enter the customer number of the order.");
            inputCheck = new InputValidator(sc.nextLine());

            if(inputCheck.checkCustomerExists(myStore.getItemList().size()) == Boolean.TRUE)
            {
                customerNumber = Integer.parseInt(inputCheck.getInput());
                validInput = Boolean.TRUE;
            }
        }

        //get items in order
        while(Boolean.TRUE)
        {
            myStore.displayStock();
            System.out.println("Please enter the item number of the next item in the order, " +
                    "or enter: exit to finish adding items");

            inputCheck = new InputValidator(sc.nextLine());

            if(inputCheck.getInput().toUpperCase().equals("EXIT"))
            {
                break;
            }
            else if (inputCheck.checkValidItemOrder(myStore.getItemList()) == Boolean.TRUE)
            {
                itemList.add(myStore.getItemList().get(Integer.parseInt(inputCheck.getInput()) - 1));
                myStore.decrementItemStock(Integer.parseInt(inputCheck.getInput()));
            }
        }

        //get order date
        DateTimeFormatter dateFormat = DateTimeFormatter.ofPattern("dd/MM/yyyy");
        validInput = Boolean.FALSE;
        while(validInput.equals(Boolean.FALSE))
        {
            System.out.println("Please enter the date of order in format: dd/MM/yyyy");
            inputCheck = new InputValidator(sc.nextLine());

            if(inputCheck.checkDate() == Boolean.TRUE)
            {
                orderDate = LocalDate.parse(inputCheck.getInput(), dateFormat);
                validInput = Boolean.TRUE;
            }
        }

        myStore.addOrder(itemList, orderDate, customerNumber);
    }

    public void addRecord()
    //allow user to add record to system
    {
        String artistName;
        String albumName;
        Double itemPrice = 0.0;
        Integer itemStock = 0;
        Boolean validInput;

        Scanner sc = new Scanner(System.in);
        InputValidator inputCheck;

        //get name
        System.out.println("Please enter the name of the artist");
        artistName = sc.nextLine().toUpperCase();

        //get album name
        System.out.println("Please enter the name of the album");
        albumName = sc.nextLine().toUpperCase();

        //get item price
        validInput = Boolean.FALSE;
        while(validInput.equals(Boolean.FALSE))
        {
            System.out.println("Please enter the price of the item (do not include $ sign).");
            inputCheck = new InputValidator(sc.nextLine());

            if(inputCheck.checkValidPrice() == Boolean.TRUE)
            {
                itemPrice = Double.parseDouble(inputCheck.getInput());
                validInput = Boolean.TRUE;
            }
        }

        //get item stock
        validInput = Boolean.FALSE;
        while(validInput.equals(Boolean.FALSE))
        {
            System.out.println("Please enter the current stock of the item.");
            inputCheck = new InputValidator(sc.nextLine());

            if(inputCheck.checkNonNegativeInt() == Boolean.TRUE)
            {
                itemStock = Integer.parseInt(inputCheck.getInput());
                validInput = Boolean.TRUE;
            }
        }

        //add record to system
        myStore.addRecord(artistName, itemPrice, itemStock, albumName);
    }

    public void addTshirt()
    //allow user to add Tshirt to system
    {
        InputValidator inputCheck;
        String artistName;
        ShirtSize shirtSize = ShirtSize.valueOf("S");
        Double itemPrice = -1.0;
        Integer itemStock = -1;
        Boolean validInput;

        Scanner sc = new Scanner(System.in);

        //get artist name
        System.out.println("Please enter the name of the artist");
        artistName = sc.nextLine().toUpperCase();

        //get shirt size
        validInput = Boolean.FALSE;
        while(validInput.equals(Boolean.FALSE))
        {
            System.out.println("Please enter the size of the shirt (S, M, L, XL)");
            inputCheck = new InputValidator(sc.nextLine().toUpperCase());

            if(inputCheck.checkShirtSize() == Boolean.TRUE)
            {
                shirtSize = ShirtSize.valueOf(inputCheck.getInput());
                validInput = Boolean.TRUE;
            }
        }

        //get price
        validInput = Boolean.FALSE;
        while(validInput.equals(Boolean.FALSE))
        {
            System.out.println("Please enter the price of the item (do not include $ sign).");
            inputCheck = new InputValidator(sc.nextLine());

            if(inputCheck.checkValidPrice() == Boolean.TRUE)
            {
                itemPrice = Double.parseDouble(inputCheck.getInput());
                validInput = Boolean.TRUE;
            }
        }

        //get stock
        validInput = Boolean.FALSE;
        while(validInput.equals(Boolean.FALSE))
        {
            System.out.println("Please enter the current stock of the item.");
            inputCheck = new InputValidator(sc.nextLine());

            if(inputCheck.checkNonNegativeInt() == Boolean.TRUE)
            {
                itemStock = Integer.parseInt(inputCheck.getInput());
                validInput = Boolean.TRUE;
            }
        }

        myStore.addTshirt(artistName, itemPrice, itemStock, shirtSize);
    }

    public void displayCustomers()
    //display customer information
    {
        myStore.displayCustomers();
    }

    public void displayMonthOrders()
    //display all order from current Local Time month
    {
        LocalDate currentDate = LocalDate.now();
        myStore.displayMonthOrders(currentDate.getMonth(), currentDate.getYear());
    }

    public void displayStock()
    //display information about all items in the system
    {
        myStore.displayStock();
    }

    public void exit()
    //exit program
    {
        this.exitBool = Boolean.TRUE;
    }

    public void startMenuLoop()
    //menu loop, that allows users to keep using system functionality until exiting the program with option 9
    {
        Scanner sc = new Scanner(System.in);

        this.exitBool = Boolean.FALSE;
        while(exitBool.equals(Boolean.FALSE))
        {
            System.out.println("1. Add a new customer.");
            System.out.println("2. Display a list of all customers.");
            System.out.println("3. Add a new record to the store inventory.");
            System.out.println("4. Add a new t-shirt to the store inventory.");
            System.out.println("5. Display a list of all items and their current stock levels.");
            System.out.println("6. Update the stock level of an item in the inventory");
            System.out.println("7. Enter and store the details of a new customer order.");
            System.out.println("8. Output a list of all orders placed in the current month.");
            System.out.println("9. Exit the program.\n");
            System.out.println("Please enter a number 1-9 for what you would like to do.");

            String userInput = sc.nextLine();
            InputValidator inputCheck = new InputValidator(userInput);

            if(inputCheck.checkMenuCommand(myStore) == Boolean.TRUE)
            {
                Integer userCommand = Integer.parseInt(userInput);

                switch(userCommand)
                {
                    case 1:
                        addCustomer();
                        break;

                    case 2:
                        displayCustomers();
                        break;

                    case 3:
                        addRecord();
                        break;

                    case 4:
                        addTshirt();
                        break;

                    case 5:
                        displayStock();
                        break;

                    case 6:
                        if(myStore.getItemList().isEmpty())
                        {
                            System.out.println("There are no items in the store.");
                        }
                        else
                        {
                            updateStock();
                        }
                        break;


                    case 7:
                        addOrder();
                        break;

                    case 8:
                        displayMonthOrders();
                        break;

                    case 9:
                        exit();
                        break;
                }
            }
        }
    }

    public void updateStock()
    //allows user to update stock for an item in system
    {
        InputValidator inputCheck;
        Boolean validInput;
        Integer itemStock = -1;
        Integer itemNumber = -1;

        Scanner sc = new Scanner(System.in);

        //get item to update stock
        validInput = Boolean.FALSE;
        while(validInput.equals(Boolean.FALSE))
        {
            myStore.displayStock();
            System.out.println("Please enter the item number of the item you would like to update stock for.");
            inputCheck = new InputValidator(sc.nextLine());

            if(inputCheck.checkItemExists(myStore.getItemList().size()) == Boolean.TRUE)
            {
                itemNumber = Integer.parseInt(inputCheck.getInput());
                validInput = Boolean.TRUE;
            }
        }

        //get new stock
        validInput = Boolean.FALSE;
        while(validInput.equals(Boolean.FALSE))
        {
            System.out.println("Please enter the new stock of the item.");
            inputCheck = new InputValidator(sc.nextLine());

            if(inputCheck.checkNonNegativeInt() == Boolean.TRUE)
            {
                itemStock = Integer.parseInt(inputCheck.getInput());
                validInput = Boolean.TRUE;
            }
        }

        //update stock
        myStore.updateStock(itemNumber, itemStock);
    }
}
