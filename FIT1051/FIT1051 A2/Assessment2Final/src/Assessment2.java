import java.util.Random;

public class Assessment2
    // Name: Daniel Nguyen
    // Student Number: 32471033
    // Version: 1.0
{
    public static void main(String[] args)
    {
        System.out.println("Task 3 output: ");
        task3();

        System.out.println();
        System.out.println("Task 6 output: ");
        task6();

    }

    public static void task3()
    {
        NameDatabase db = new NameDatabase();

        Random randomiser = new Random();

        for (int i = 0; i < 10; i++)
        {
            //generate random length and character
            int length = randomiser.nextInt(8) + 3;
            char character = (char)(randomiser.nextInt(26) + 'a');

            StringBuffer name = new StringBuffer();

            //generate the name from random character and random length
            for (int j = 0; j < length; j++)
            {
                name.append(character);
            }

            db.addName(name.toString());
        }

        System.out.println(db.toString());

    }

    public static void task6()
    {
        NameDatabase db = new NameDatabase();
        db.addName("Maria");
        db.addName("Nushi");
        db.addName("Mohammed");
        db.addName("Jose");
        db.addName("Wei");
        db.addName("Ahmed");
        db.addName("Yan");
        db.addName("Ali");
        db.addName("John");
        db.addName("David");
        db.addName("Li");
        db.addName("Abdul");
        db.addName("Anna");
        db.addName("Ying");
        db.addName("Michael");
        db.addName("Juan");
        db.addName("Mary");
        db.addName("Jean");
        db.addName("Robert");
        db.addName("Daniel");

        System.out.println(db.getMeanNameLength());

        int prevNamesLength = 0;
        int namesLength = db.getNames().size();

        //keep removing duplicate first letter names until all names have unique starting letter
        while(namesLength != prevNamesLength)
        {
            db.removeCommonStartNames();
            prevNamesLength = namesLength;
            namesLength = db.getNames().size();
        }

        System.out.println(db.toString());
    }


}
