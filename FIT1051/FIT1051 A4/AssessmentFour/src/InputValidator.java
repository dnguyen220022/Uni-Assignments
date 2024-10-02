import java.time.LocalDate;
import java.time.format.DateTimeFormatter;
import java.util.ArrayList;

public class InputValidator
    // Name: Daniel Nguyen
    // Student Number: 32471033
    // Version: 1.0
    //
    //Input validator class, which stores a string, and can perform multiple input validations
    //on said string. This is used to check user input in our store management system
    //contains methods to check whether an input is valid for various functions, as well as a getter
    //method for the input, to allow the string to be piped back when required.
{
    private String input;

    public InputValidator(String input)
    //non-default constructor
    {
        this.input = input;
    }

    public Boolean checkCustomerExists(Integer custCount)
    //check whether input refers to a valid customer number
    {
        try
        {
            Integer customerNumber = Integer.parseInt(getInput());

            if(customerNumber < 1 || customerNumber > custCount)
            {
                System.out.println("You have entered an invalid customer number, please try again.");
                return Boolean.FALSE;
            }
            else
            {
                return Boolean.TRUE;
            }
        }
        catch (Exception e)
        {
            System.out.println("You have entered an invalid customer number, please try again.");
            return Boolean.FALSE;
        }
    }

    public Boolean checkDate()
    //check if date given by input is valid
    {
        DateTimeFormatter dateFormat = DateTimeFormatter.ofPattern("dd/MM/yyyy");
        try
        {
            LocalDate.parse(getInput(), dateFormat);
            return Boolean.TRUE;
        }
        catch (Exception e)
        {
            System.out.println("You have entered an invalid date, please try again.");
            return Boolean.FALSE;
        }
    }

    public Boolean checkItemExists(Integer itemCount)
    //check if input refers to valid item number
    {
        try
        {
            Integer itemNumber = Integer.parseInt(getInput());

            if(itemNumber < 1 || itemNumber > itemCount)
            {
                System.out.println("You have entered an invalid item number, please try again.");
                return Boolean.FALSE;
            }
            else
            {
                return Boolean.TRUE;
            }
        }
        catch (Exception e)
        {
            System.out.println("You have entered an invalid item number, please try again.");
            return Boolean.FALSE;
        }
    }

    public Boolean checkMenuCommand(Store myStore)
    //check if input refers to a valid menu command
    //also checks if command can be completed (e.g. cannot create an order when no items in system)
    {
        try
        {
            int input = Integer.parseInt(getInput());
            if(input < 1 || input > 9)
            {
                System.out.println("You have entered an invalid command, please try again.\n");
                return Boolean.FALSE;
            }
            else if(input == 7 && !myStore.checkItemsInStock())
            {
                System.out.println("There are currently no items in stock.");
                return Boolean.FALSE;
            }
            else if (input == 7 && myStore.getCustomerList().isEmpty())
            {
                System.out.println("No customers have been added to the system.");
                return Boolean.FALSE;
            }
            else if(input == 6 && myStore.getItemList().isEmpty())
            {
                System.out.println("No items have been added to the system yet.");
                return Boolean.FALSE;
            }
            else
            {
                return Boolean.TRUE;
            }
        }
        catch (Exception e)
        {
            System.out.println("You have entered an invalid command, please try again.");
            return Boolean.FALSE;
        }
    }

    public Boolean checkNonNegativeInt()
    //check if input is a non negative integer
    {
        try
        {
            int input = Integer.parseInt(getInput());
            if(input < 0)
            {
                System.out.println("Number cannot be negative, please try again.");
                return Boolean.FALSE;
            }
            else
            {
                return Boolean.TRUE;
            }
        }
        catch (Exception e)
        {
            System.out.println("You have not entered a number, please try again.");
            return Boolean.FALSE;
        }
    }

    public Boolean checkShirtSize()
    //check if input refers to a valid ShirtSize in ShirtSize enum
    {
        try
        {
            ShirtSize shirtSize = ShirtSize.valueOf(getInput());
            return Boolean.TRUE;
        }
        catch (Exception e)
        {
            System.out.println("You have not entered a valid shirt size, please try again.");
            return Boolean.FALSE;
        }
    }

    public Boolean checkValidItemOrder(ArrayList<Item> itemList)
    //check if input refers to an item that exists and is in stock
    {
        try
        {
            Integer itemNumber = Integer.parseInt(getInput());

            if(itemNumber < 1 || itemNumber > itemList.size())
            {
                System.out.println("You have entered an invalid item number, please try again.");
                return Boolean.FALSE;
            }
            else
            {
                for(Item item : itemList)
                {
                    if(item.getItemNumber().equals(itemNumber) && item.getItemStock() > 0)
                    {
                        return Boolean.TRUE;
                    }
                }
                System.out.println("This item is out of stock, please try again.");
                return Boolean.FALSE;
            }
        }
        catch (Exception e)
        {
            System.out.println("You have entered an invalid item number, please try again.");
            return Boolean.FALSE;
        }
    }

    public Boolean checkValidPrice()
    //check if input refers to a valid price (non negative integer OR double)
    {
        try
        {
            Double input = Double.parseDouble(getInput());
            if(input < 0)
            {
                System.out.println("Price cannot be negative, please try again.");
                return Boolean.FALSE;
            }
            else
            {
                return Boolean.TRUE;
            }
        }
        catch (Exception e)
        {
            System.out.println("You have not entered a number, please try again.");
            return Boolean.FALSE;
        }
    }

    public String getInput()
    //input getter method
    {
        return this.input;
    }

}
