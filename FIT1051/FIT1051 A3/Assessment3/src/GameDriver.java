import java.util.ArrayList;
import java.util.Arrays;
import java.util.Scanner;

public class GameDriver
    // Name: Daniel Nguyen
    // Student Number: 32471033
    // Version: 1.0
    //
    //Creates teams, and runs the tournament, while printing scores,
    //winners, and information about gold and silver medallists
{
    public static void main(String[] args)
    {
        //create teams
        Team Spain = new Team("Spain", 1);
        Team USA = new Team("USA", 2);
        Team France = new Team("France", 3);
        Team Japan = new Team("Japan", 4);
        Team Canada = new Team("Canada", 5);
        Team Brazil = new Team("Brazil", 6);
        Team Australia = new Team("Australia", 7);
        Team Colombia = new Team("Colombia", 8);

        //add teams to an arraylist
        ArrayList<Team> currentRound = new ArrayList<Team>(
                Arrays.asList(
                        Spain,
                        USA,
                        France,
                        Japan,
                        Canada,
                        Brazil,
                        Australia,
                        Colombia)
        );

        //init variables for running the game and constructing next round bracket
        ArrayList<Team> nextRound;
        Game currentGame;
        Scanner pressEnter = new Scanner(System.in);

        //keep running tournament until only final is left
        while (currentRound.size() > 2)
        {
            nextRound = new ArrayList<Team>();

            //run the current tournament round
            for (int i = 0; i < currentRound.size() / 2; i++)
            {
                //determine winner of the game
                currentGame = new Game(currentRound.get(i),
                        currentRound.get(currentRound.size() - 1 - i));

                //add the game winner to the next round
                nextRound.add(currentGame.playGame());

                //pause until user input before running next game
                System.out.println("Press enter to continue");
                pressEnter.nextLine();

            }
            //after all matches in a round are finished, set next round becomes current round
            currentRound = nextRound;
        }

        //play final match and get winner
        currentGame = new Game(currentRound.get(0), currentRound.get(1));
        Team winner = currentGame.playGame();

        //print gold medal winner message + stats
        System.out.println("\n" + winner.getName() +
                " has won the Olympic Gold Medal! Their statistics for the tournament are:" +
                "\n" + winner.toString() + "\n");

        //print silver medal winner message + stats
        if (winner.equals(currentGame.getTeam1()))
        {
            System.out.println(currentGame.getTeam2().getName() +
                    " has won the Olympic Silver Medal! Their statistics for the tournament are:" +
                    "\n" + currentGame.getTeam2().toString());
        }
        else
        {
            System.out.println(currentGame.getTeam1().getName() +
                    " has won the Olympic Silver Medal! Their statistics for the tournament are:" +
                    "\n" + currentGame.getTeam2().toString());
        }
    }
}