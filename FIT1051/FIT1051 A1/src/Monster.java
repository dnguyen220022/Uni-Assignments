public class Monster
{
    // Name: Daniel Nguyen
    // Student Number: 32471033
    //
    // Create class Monster, with fields name, attack, defence, health
    // include accessors and mutators
    private String name;
    private int attack;
    private int defence;
    private int health;

    public Monster()
            // set default field values
    {
        name = "Default Monster";
        attack = 1;
        defence = 1;
        health = 10;
    }

    public Monster(String name, int attack, int defence, int health)
            // set field values
    {
        setName(name);
        setAttack(attack);
        setDefence(defence);
        setHealth(health);
    }

    public void setAttack(int attack)
            // if attack not valid, throw error, otherwise set attack
    {
        if (attack < 0 || attack > 10)
        {
            throw new IllegalArgumentException("attack must be an integer 0-10");
        }
        else
        {
            this.attack = attack;
        }
    }

    public void setDefence(int defence)
            // if defence not valid, throw error, otherwise set defence
    {
        if (defence < 0 || defence > 10)
        {
            throw new IllegalArgumentException("defence must be an integer 0-10");
        }
        else
        {
            this.defence = defence;
        }
    }

    public void setHealth(int health)
            // if health not valid, throw error, otherwise set health
    {
        if (health < 0 || health > 100)
        {
            throw new IllegalArgumentException("health must be an integer 0-100");
        }
        else
        {
            this.health = health;
        }
    }

    public void setName(String name)
            // if name not valid, throw error, otherwise set Name
    {
        if (name == null || name.isEmpty())
        {
            throw new IllegalArgumentException("name cannot be null or an empty string");
        }
        else
        {
            this.name = name;
        }
    }

    public int getAttack()
            // return attack value
    {
        return attack;
    }

    public int getDefence()
            // return defence value
    {
        return defence;
    }

    public int getHealth()
            // return health value
    {
        return health;
    }

    public String getName()
            // return name value
    {
        return name;
    }
}
