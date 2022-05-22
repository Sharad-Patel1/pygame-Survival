# Sharad_Patel_19768944



To use this application the user will run this program like they would any other python program. 
    Python3 [main.py]

## File description

### background

This class is in charge of handling the creation and display of the background of the game.
The class also handles the view for the in game commands that the player can type to change the game mode. 

### bullet
    
This class is in charge of handling the creation display and the physics of the bullet. 
The class handles the movement and collision detection of the bullet. 

### commands

This class is in charge of handling the in game commands that the user will input to change the way the game behaves
The current commands are /day, /night to change the in game "time" to change whether the player is fighting humans or 
zombies. 

### gunner

This class is in charge of the human enemies in the game. 
This class inherits the attributes of the player class. 
The class handles the movement of the enemy, the sight, the collision detection,
the animation of the enemy for various modes i.e. idle, moving shooting, etc. 

### item

This class is in charge if the food and water.


### level

This file is incharge of developing the noise and the construction of the initial spawn point of the player in game.

### main

The main driver code for the game, this is where the game is run.

### map

This class handles any and all things related to the map. 
The file handles the "Spawning" of elements on the map. i.e. display all the objects on the map. 

### player

This is the class that defines the player class, this is where all the attributes and the functionalities of the player is defined. 
This class is also inherited by the zombie and gunner class to be able to share the attributes and functionalities.

### settings

This is the file where the main global variables for the game is stored. 

### test

This is the file used initially to test the game and check for bugs


### tile

This is the file that creates the tile from the asset and defines where the tile needs to be placed.
The file also has another function to show that newly created Tile. 

### zombie 

This class is in charge of the zombies in the game.
This class inhertis the attributes of the player class.
The class handles the movement of the zombie, the sight, the collision detection,
the animation of the zombie for various modes i.e. idle, moving, etc. 



The user can also give some parameter tweaks:
    
    Zombies mode
        This is the game mode where the player is “locked” in the environment with randomly spawning zombies and they have to last for as long as they can. 
        The longer they last the higher the score is. 
            Played by inputting python3 [main.py] -z
    
    Normal Mode / Day mode
        This is the game mode where the player runs in an infinitely generating random map that spawns enemies and and they earn points by killing enemies
            Played by inputting python3 [game.py] -d 
    
    Night Mode
        This game mode is similar to the normal / day mode, but in this game mode the player is running through the map and its “night time” where the colors are a lot darker, and the enemies can only see the player when he gets within a certain range of them. 
            Played by inputting python3 [game.py] -n 

## Few Bugs

1. Zombies currently do no damage to the player, 
2. Sometimes while playing the player can if they go to the left side of the screen can fall off the playable area. 


## References

Assets imported from
    itch.io

The BG
    https://brullov.itch.io/oak-woods

The Zombies
    https://sungraphica.itch.io/zombie-pixel-art

The Gunners 
    https://secrethideout.itch.io/team-wars-platformer-battle

The Player
    https://rgsdev.itch.io/animated-top-down-character-base-template-in-pixel-art-rgsdev


    