public class Record extends Item
    // Name: Daniel Nguyen
    // Student Number: 32471033
    // Version: 1.0
    //
    //Creates Record class, inheriting from Item abstract Class.
    //contains additional variables and getter/setter methods for album name
{
    public String albumName;

    public Record(Integer itemNumber, String artistName, Double itemPrice, Integer itemStock, String albumName)
    //Non default constructor
    {
        super("Record", itemNumber, artistName, itemPrice, itemStock);
        this.albumName = albumName;
    }

    public String displayInfo()
    //returns string of relevant record information
    {
        StringBuffer sb = new StringBuffer();
        sb.append("Item Number: ").append(getItemNumber()).append("\n");
        sb.append("Item Type: ").append(getItemType()).append("\n");
        sb.append("Album Name: ").append(getAlbumName()).append("\n");
        sb.append("Artist: ").append(getArtistName()).append("\n");
        sb.append("Price: $").append(getItemPrice()).append("\n");
        sb.append("Stock: ").append(getItemStock()).append("\n");
        return sb.toString();
    }

    public String getAlbumName()
    //album name getter
    {
        return albumName;
    }
}