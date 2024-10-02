import java.time.LocalDate;
import java.time.Month;
import java.util.ArrayList;

public class Store
    // Name: Daniel Nguyen
    // Student Number: 32471033
    // Version: 1.0
    //
    //Creates Store class, with methods needed to run store database
    //includes some methods created for modularisation, such as decrementStock, which is
    //used when creating an order to decrement the stock of items in the order.
    //Also includes several display methods.
{
    private ArrayList<Customer> customerList;
    private ArrayList<Item> itemList;
    private ArrayList<Order> orderList;

    public Store()
    //non-default constructor
    {
        this.customerList =  new ArrayList<Customer>();
        this.itemList = new ArrayList<Item>();
        this.orderList = new ArrayList<Order>();
    }

    public void addCustomer(String customerName)
    //add customer to customerList
    {
        Integer customerNumber = customerList.size() + 1;

        Customer newCustomer = new Customer(customerNumber, customerName);
        this.customerList.add(newCustomer);
    }

    public void addOrder(ArrayList<Item> itemList, LocalDate orderDate, Integer customerNumber)
    //create and add order to orderList
    {
        Integer orderNumber = orderList.size() + 1;

        Order newOrder = new Order(orderNumber, itemList, orderDate);
        orderList.add(newOrder);
        this.customerList.get(customerNumber - 1).addOrder(newOrder);
    }

    public void addRecord(String artistName, Double itemPrice, Integer itemStock, String albumName)
    //create and add record to itemList
    {
        Integer itemNumber = itemList.size() + 1;

        Record newRecord = new Record(itemNumber, artistName, itemPrice, itemStock, albumName);
        this.itemList.add(newRecord);
    }

    public void addTshirt(String artistName, Double itemPrice, Integer itemStock, ShirtSize shirtSize)
    //create and add tShirt to itemList
    {
        Integer itemNumber = itemList.size() + 1;

        Tshirt newTshirt = new Tshirt(itemNumber, artistName, itemPrice, itemStock, shirtSize);
        this.itemList.add(newTshirt);
    }

    public Boolean checkItemsInStock()
    //check if there are any items in stock
    {
        if(this.itemList.isEmpty())
        {
            return Boolean.FALSE;
        }

        for (Item item : this.itemList)
        {
            if(item.getItemStock() > 0)
            {
                return Boolean.TRUE;
            }
        }

        return Boolean.FALSE;
    }

    public void decrementItemStock(Integer itemNumber)
    //decrements the stock of an item by 1
    {
        for(Item item : this.itemList)
        {
            if(item.getItemNumber().equals(itemNumber))
            {
                Integer newItemStock = item.getItemStock() - 1;
                item.setItemStock(newItemStock);
            }
        }
    }

    public void displayCustomers()
    //prints customer information
    {
        for(Customer customer : this.customerList)
        {
            System.out.println(customer.displayInfo());
        }
    }

    public void displayMonthOrders(Month month, int year)
    //display all orders created in the current (based on user local time) month.
    {
        for(Order order : getOrderList())
        {
            if(month.equals(order.getOrderDate().getMonth())
                    && year == order.getOrderDate().getYear())
            {
                System.out.println(order.displayInfo());
            }
        }
    }

    public void displayStock()
    //display information on all items in system.
    {
        for(Item item : getItemList())
        {
            System.out.println(item.displayInfo());
        }
    }

    public ArrayList<Customer> getCustomerList()
    //customerList getter
    {
        return customerList;
    }

    public ArrayList<Item> getItemList()
    //itemList getter
    {
        return itemList;
    }

    public ArrayList<Order> getOrderList()
    //orderList getter
    {
        return orderList;
    }

    public void updateStock(Integer itemNumber, Integer stockNumber)
    //update the stock of an item already in the system
    {
        for(Item item : this.itemList)
        {
            if(item.getItemNumber().equals(itemNumber))
            {
                item.setItemStock(stockNumber);
            }
        }
    }

}