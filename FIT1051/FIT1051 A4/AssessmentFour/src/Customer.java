import java.util.ArrayList;

public class Customer implements DisplayInfo
    // Name: Daniel Nguyen
    // Student Number: 32471033
    // Version: 1.0
    //
    //Creates Customer Class, and implements displayInfo interface method
{
    private Integer customerNumber;
    private String customerName;
    private ArrayList<Order> customerOrderList;

    public Customer(Integer customerNumber, String customerName)
    //non-default constructor
    {
        this.customerNumber = customerNumber;
        this.customerName = customerName;
        this.customerOrderList = new ArrayList<Order>();
    }

    public void addOrder(Order newOrder)
    //add order to orderList
    {
        this.customerOrderList.add(newOrder);
    }

    public String displayInfo()
    //returns string of customer info
    {
        final StringBuilder sb = new StringBuilder();
        sb.append("Customer Number: ").append(getCustomerNumber()).append("\n");
        sb.append("Customer Name: ").append(getCustomerName()).append("\n");
        sb.append("Number of Orders: ").append(getCustomerOrderList().size()).append("\n");
        return sb.toString();
    }

    public String getCustomerName()
    //customer name getter
    {
        return customerName;
    }

    public Integer getCustomerNumber()
    //customer number getter
    {
        return customerNumber;
    }

    public ArrayList<Order> getCustomerOrderList()
    //customer orderList getter
    {
        return customerOrderList;
    }
}
