public class Team
    // Name: Daniel Nguyen
    // Student Number: 32471033
    // Version: 1.0
    //
    //Create team class, with getter/setter methods for statistics
    //contains toString method, which returns all statistics
{
    private final String name;
    private final Integer rank;
    private Integer goalsFor;
    private Integer goalsAgainst;

    public Team()
    //default constructor
    {
        this.name = "Default Team";
        this.rank = 0;
        this.goalsFor = 0;
        this.goalsAgainst = 0;
    }
    public Team(String name, Integer rank)
    //non-default constructor
    {
        this.name = name;
        this.rank = rank;
        this.goalsFor = 0;
        this.goalsAgainst = 0;
    }

    public String getName()
    //getter method for team name
    {
        return name;
    }

    public Integer getRank()
    //getter method for team rank
    {
        return rank;
    }

    public Integer getGoalsFor()
    //getter method for goalsFor
    {
        return goalsFor;
    }

    public Integer getGoalsAgainst()
    //getter method for goalsAgainst
    {
        return goalsAgainst;
    }

    public void setGoalsFor(Integer goalsFor)
    //setter method for goalsFor
    {
        this.goalsFor = goalsFor;
    }

    public void setGoalsAgainst(Integer goalsAgainst)
    //setter method for GoalsAgainst
    {
        this.goalsAgainst = goalsAgainst;
    }

    public String toString()
    //return string of team details
    {
        return "Team: " + name + "\n" + "Ranking: " + rank + "\n" +
                "Goals For: " + goalsFor + "\n" + "Goals Against: " + goalsAgainst;
    }
}