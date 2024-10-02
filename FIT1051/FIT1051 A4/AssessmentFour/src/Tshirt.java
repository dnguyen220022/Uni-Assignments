public class Tshirt extends Item
    // Name: Daniel Nguyen
    // Student Number: 32471033
    // Version: 1.0
    //
    //Creates Tshirt class, inheriting from Item abstract Class.
    //contains additional variables and getter methods for shirt size
{
    public ShirtSize shirtSize;

    public Tshirt(Integer itemNumber, String artistName, Double itemPrice, Integer itemStock, ShirtSize shirtSize)
    //Non default constructor
    {
        super("Tshirt", itemNumber, artistName, itemPrice, itemStock);
        this.shirtSize = shirtSize;
    }

    public String displayInfo()
    //returns string of relevant info about Tshirt
    {
        StringBuffer sb = new StringBuffer();
        sb.append("Item Number: ").append(getItemNumber()).append("\n");
        sb.append("Item Type: ").append(getItemType()).append("\n");
        sb.append("Size: ").append(getShirtSize()).append("\n");
        sb.append("Artist: ").append(getArtistName()).append("\n");
        sb.append("Price: $").append(getItemPrice()).append("\n");
        sb.append("Stock: ").append(getItemStock()).append("\n");
        return sb.toString();
    }

    public ShirtSize getShirtSize()
    //shirt size getter
    {
        return shirtSize;
    }
}