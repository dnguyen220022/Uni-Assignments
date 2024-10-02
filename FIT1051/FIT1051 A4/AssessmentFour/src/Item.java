abstract class Item implements DisplayInfo
    // Name: Daniel Nguyen
    // Student Number: 32471033
    // Version: 1.0
    //
    //Creates Item abstract class, with methods that will be used
    //unchanged for both tshirts and records, as well as relevant
    //variables for both.
    //implements DisplayInfo interface as well.
{
    private Integer itemNumber;
    private String artistName;
    private Double itemPrice;
    private Integer itemStock;
    private String itemType;

    public Item(String itemType, Integer itemNumber, String artistName, Double itemPrice, Integer itemStock)
    //Non default constructor
    {
        this.itemNumber = itemNumber;
        this.artistName = artistName;
        this.itemPrice = itemPrice;
        this.itemStock = itemStock;
        this.itemType = itemType;
    }

    public String getArtistName()
    //artist name getter
    {
        return artistName;
    }

    public Integer getItemNumber()
    //item number getter
    {
        return itemNumber;
    }

    public Double getItemPrice()
    //item price getter
    {
        return itemPrice;
    }

    public Integer getItemStock()
    //item stock getter
    {
        return itemStock;
    }

    public String getItemType()
    //item type getter
    {
        return itemType;
    }

    public void setItemStock(Integer itemStock)
    //item stock setter
    {
        this.itemStock = itemStock;
    }
}