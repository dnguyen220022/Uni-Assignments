import java.time.LocalDate;
import java.util.ArrayList;

public class Order implements DisplayInfo
    // Name: Daniel Nguyen
    // Student Number: 32471033
    // Version: 1.0
    //
    //Implements Order Class, with getter/setter methods.
    //Uses LocalDate to store date.
    //also implements DisplayInfo interface.
{
    private Integer orderNumber;
    private ArrayList<Item> itemList;
    private LocalDate orderDate;
    private Double orderTotal;

    public Order(Integer orderNumber, ArrayList<Item> itemList, LocalDate orderDate)
    //non-default constructor
    {
        this.orderNumber = orderNumber;
        this.itemList = itemList;
        this.orderDate = orderDate;
        this.orderTotal = 0.0;

        for(Item item: this.itemList)
        {
            this.orderTotal += item.getItemPrice();
        }
    }

    public String displayInfo()
    //returns string of relevant order information
    {
        StringBuffer sb = new StringBuffer();
        sb.append("Order Number: ").append(getOrderNumber()).append("\n");
        sb.append("Date of Purchase: ").append(getOrderDate()).append("\n");
        sb.append("Items (Item Number): ");
        String prefix = "";
        for(Item item : getItemList())
        {
            sb.append(prefix);
            sb.append(item.getItemNumber());
            prefix = ", ";
        }
        sb.append("\n");
        sb.append("Order Total: $").append(getOrderTotal()).append("\n");
        return sb.toString();
    }

    public ArrayList<Item> getItemList()
    //order itemList getter
    {
        return itemList;
    }

    public LocalDate getOrderDate()
    //order date getter
    {
        return orderDate;
    }

    public Integer getOrderNumber()
    //order number getter
    {
        return orderNumber;
    }

    public Double getOrderTotal()
    //order total cost getter
    {
        return orderTotal;
    }
}