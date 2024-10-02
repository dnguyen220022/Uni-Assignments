import java.util.Random;

public class Game
    // Name: Daniel Nguyen
    // Student Number: 32471033
    // Version: 1.0
    //
    //Creates Game Class, with getter/setter methods for each team in the game, and
    //contains playGame method, which runs the game simulation
{
    private final Team team1;
    private final Team team2;

    public Game()
    //default constructor (game with 2 default teams)
    {
        this.team1 = new Team();
        this.team2 = new Team();
    }

    public Game(Team team1, Team team2)
    //non-default constructor
    {
        this.team1 = team1;
        this.team2 = team2;
    }

    public Team getTeam1()
    //getter method for team1
    {
        return this.team1;
    }

    public Team getTeam2()
    //getter method for team2
    {
        return this.team2;
    }

    public Team playGame()
    //runs game simulation between team1 and team2
    {
        Random randomiser = new Random();

        Team winner;
        Integer team1Goals = 0;
        Integer team2Goals = 0;
        Integer team1ChanceToScore = 20 - team1.getRank();
        Integer team2ChanceToScore = 20 - team2.getRank();

        System.out.println(team1.getName() + " VS " + team2.getName() + "\n");

        //runs 18 5min simulations (18 * 5 == 90 minutes)
        for (int i = 0; i < 18; i++)
        {
            //check if team 1 scored
            int generateGoal = randomiser.nextInt(100);
            if (generateGoal < team1ChanceToScore)
            {
                team1Goals += 1;
                int goalScoredTime = i * 5 + randomiser.nextInt(5);
                System.out.println(team1.getName() + " - " + goalScoredTime + "\'");
            }

            //check if team 2 scored
            generateGoal = randomiser.nextInt(100);
            if (generateGoal < team2ChanceToScore)
            {
                team2Goals += 1;
                int goalScoredTime = i * 5 + randomiser.nextInt(5);
                System.out.println(team2.getName() + " - " + goalScoredTime + "\'");
            }
        }

        //set goals for and goals against for each team
        team1.setGoalsFor(team1.getGoalsFor() + team1Goals);
        team1.setGoalsAgainst(team1.getGoalsAgainst() + team2Goals);

        team2.setGoalsFor(team2.getGoalsFor() + team2Goals);
        team2.setGoalsAgainst(team2.getGoalsAgainst() + team1Goals);

        //print final score
        System.out.println(team1.getName() + " " + team1Goals +
                " - " + team2Goals + " " + team2.getName());

        //handle match end conditions
        if (team1Goals.equals(team2Goals))
        {
            //penalty shootout handling
            System.out.println("The scores are tied at full time! A penalty shootout will take place");

            int team1Penalty = randomiser.nextInt();
            int team2Penalty = randomiser.nextInt();

            if (team1Penalty > team2Penalty)
            {
                winner = team1;
            }

            else
            {
                winner = team2;
            }
        }

        //assign winner if no penalty shootout
        else if (team1Goals > team2Goals)
        {
            //team 1 wins
            winner = team1;
        }

        else
        {
            //team 2 wins
            winner = team2;
        }

        //print winner and return winning team
        System.out.println(winner.getName() + " wins!");
        return winner;

    }
}