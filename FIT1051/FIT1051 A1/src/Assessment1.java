import java.util.Scanner;

public class Assessment1
    // Name: Daniel Nguyen
    // Student Number: 32471033
    // Version: 1.0
{
    public static void main(String[] args)
    {

        Assessment1 a1 = new Assessment1();

        // Instruction: To run your respective task, uncomment below individually
//        a1.task1();
//        a1.task2();
//        a1.task3();
//        a1.task4();
    }

    public double areaOfCircle(double r)
            // return area of a circle for input r == radius
    {
        double area = Math.PI * r * r;
        return area;
    }

    public void task1()
    {
        double r = 5.0;
        double area = areaOfCircle(r);
        System.out.println(area);
    }

    public void task2()
    {
        Monster monster1 = new Monster("Mattasaur", 8, 3, 60);
        monster1.setHealth(45);
        int monster1Health = monster1.getHealth();
        System.out.println(monster1Health);
    }

    public Boolean numberValidator(int numToCheck, int max, int min)
            // determine whether numToCheck is between values min and max
    {
        Boolean numberIsValid = numToCheck >= min && numToCheck <= max;
        return numberIsValid;
    }

    public void task3()
    {
        Scanner scannerObject = new Scanner(System.in);

        System.out.println("Please enter an integer:");

        String userInput = scannerObject.nextLine();

        scannerObject.close();

        int userInputToInt = Integer.parseInt(userInput);

        if (numberValidator(userInputToInt, 100, 0) == Boolean.TRUE)
        {
            System.out.println("The number is valid.");
        }
        else
        {
            System.out.println("The number is not valid.");
        }
    }

    public Boolean dateValidator(int day, int month, int year)
            // determine if date given exists
    {
        if (year < 0 || month <= 0 || month > 12 || day <= 0 || day > 31)
        {
            return Boolean.FALSE;
        }

        if (month == 4 || month == 6 || month == 9 || month == 11)
        {
            if (day > 30)
            {
                return Boolean.FALSE;
            }
        }

        if (month == 2)
        {
            if (year % 4 == 0)
            {
                if (day > 29)
                {
                    return Boolean.FALSE;
                }
            }
            else
            {
                if (day > 28)
                {
                    return Boolean.FALSE;
                }
            }
        }
        return Boolean.TRUE;
    }

    public void task4()
    {
        Scanner scannerObject = new Scanner(System.in);

        System.out.println("Please enter a day, month and year:");

        String userDay = scannerObject.next();
        String userMonth = scannerObject.next();
        String userYear = scannerObject.next();

        int dayInt = Integer.parseInt(userDay);
        int monthInt = Integer.parseInt(userMonth);
        int yearInt = Integer.parseInt(userYear);

        if (dateValidator(dayInt, monthInt, yearInt))
        {
            System.out.println("Your date is valid");
        }
        else
        {
            System.out.println("your date is invalid");
        }

    }
}