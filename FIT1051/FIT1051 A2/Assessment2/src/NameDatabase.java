import java.util.ArrayList;
import java.util.Iterator;

public class NameDatabase
    // Name: Daniel Nguyen
    // Student Number: 32471033
    // Version: 1.0
{
    private ArrayList<String> names;

    public NameDatabase()
        //default constructor
    {
        names = new ArrayList<String>();
    }

    public NameDatabase(ArrayList<String> names)
        //non-default constructor
    {
        this.names = names;
    }

    public ArrayList<String> getNames()
        //getter method
    {
        return names;
    }

    public void setNames(ArrayList<String> names)
        //setter method
    {
        this.names = names;
    }

    public void addName(String name)
        //add a new name to end of list
    {
        names.add(name);
    }

    public void removeName(int index)
        //remove a name at index position
    {
        names.remove(index);
    }

    public String toString()
        //return list of names seperate by newLine
    {
        StringBuffer output = new StringBuffer();
        for (String name : names)
        {
            output.append(name).append("\n");
        }
        return output.toString();
    }

    public double getMeanNameLength()
        //returns mean name length
    {
        double totalLength = 0;

        for (String name : names)
        {
            totalLength += name.length();
        }

        return totalLength / names.size();
    }

    public char getMostCommonStartingLetter()
        //returns the most common starting letter
    {
        int[] letterCount = new int[26];

        //iterate over name list and get the count of each starting letter
        for (String name : names)
        {
            char startLetter = name.toLowerCase().charAt(0);
            letterCount[startLetter - 'a']++;
        }

        int maxCount = 0;
        char mostCommonStartingChar = ' ';

        //iterate through count array to find most common starting letter
        for (int i = 0; i < 26; i++)
        {
            if (letterCount[i] > maxCount)
            {
                maxCount = letterCount[i];
            }
        }

        //get first occurence of most popular letter that is in names
        for (String name : names)

        {
            int firstLetterIndex = (int) name.toLowerCase().charAt(0) - 'a';

            if (letterCount[firstLetterIndex] == maxCount)
            {
                mostCommonStartingChar = (char) ('a' + firstLetterIndex);
                break;
            }
        }

        return mostCommonStartingChar;
    }

    public int removeCommonStartNames()
        //remove all names in the list that begin with most common starting letter except for the first
    {
        char mostCommonStartingLetter = getMostCommonStartingLetter();
        int namesScanned = 0;

        Iterator<String> iterator = names.iterator();

        //remove names starting with most common starting char except for the first
        while(iterator.hasNext())
        {
            String name = iterator.next();
            char startingLetter = name.toLowerCase().charAt(0);

            if (startingLetter == mostCommonStartingLetter)
            {
                if (namesScanned == 0)
                {
                    namesScanned += 1;
                }
                else
                {
                    iterator.remove();
                    System.out.println("Removing name " + name);
                    namesScanned += 1;
                }
            }
        }

        if (namesScanned != 1)
        {
            System.out.println("Removed " + (namesScanned - 1) + " names beginning with " + mostCommonStartingLetter);
        }

        return namesScanned;
    }
}
