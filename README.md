# RPShell
**Updated on 29/09/2020**
#
## What is RPShell ?

RPShell is a personnal project that aims to propose a simple but enjoyable shell-based RPG. It is written in Python but I do not exclude the idea of using other languages if I need to.The idea is to offer a simple experience where the player can interact with an environment only using command line.

## TEMP : mini-doc
<div style="text-align: justify"> 

The code documentation does not exist yet, but here is the main idea of "how it works".

The only class we use is `user`, in which we implements every needed function for the player, i.e. handling directions, interactions, consultation of inventory, having descriptions of the world around, etc. Each of these functions are called *via* the `main.py` file in which we create the second class `rpshellPrompt` that inherits Python library `cmd`.

Game data are stored in dictionnaries. One for NPCs, one for rooms, one for items, one for mobs. Each of them are structured with keys that are declared in the `Const.py` file (other constants are declared for syntax facilitation purpose, such as unicode characters). </div>

## How to play
<div style="text-align: justify"> 

The code on the `master` branch is always supposed to work, even if the game is incomplete. Of course you will need to install aditional libraries. Last paragraph discusses this.

So far, open a terminal, go in the folder where you cloned the repo and simply use `python3 main.py` to launch the game. Since `cmd` is used you can simply type `help` to display list available commands, and type `help [command]` to have more info about a specific command.

The command prompt always appears as follow :

> [**Region**] \> [Room] \> [NPC if applicable] \>
 
 and is updated whenever needed. </div>

 ## Additionnal libraries
<div style="text-align; justify>

Some additionnal libraries have to be installed to run the game. This list **is still to be updated**.

- columnar :  

        $ pip3 install columnar

</div>