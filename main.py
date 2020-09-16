"""

"""

import cmd
import os
#from termcolor import colored

from player import player
from roomsData import *


user = player(15,30,'Home')


class rpshellPrompt(cmd.Cmd):

    prompt = BIGCYAN+worldRooms[user.location][REGION].upper()+'\u276D '+user.location+' \u232A '+ RESET


    def default(self, arg):
        print('I do not know this command. Type "help" to list available commands.')

    def update_prompt(self, old_loc, direction):
        self.prompt = BIGCYAN+worldRooms[user.location][REGION].upper()+'\u276D '+ worldRooms[old_loc][direction]+' \u232A '+RESET

    def do_east(self, arg):
        """Go east if possible."""
        old_loc = user.location
        if user.move('east'):
            self.update_prompt(old_loc, EAST)
    
    def do_west(self, arg):
        """Go west if possible."""
        old_loc = user.location
        if user.move('west'):
            self.update_prompt(old_loc, WEST)

    def do_north(self, arg):
        """Go north if possible."""
        old_loc = user.location
        if user.move('north'):
            self.update_prompt(old_loc, NORTH)

    def do_south(self, arg):
        """Go south if possible."""
        old_loc = user.location
        if user.move('south'):
            self.update_prompt(old_loc, SOUTH)

    def do_northwest(self, arg):
        """Go northwest if possible."""
        old_loc = user.location
        if user.move('northwest'):
            self.update_prompt(old_loc, NORTHWEST)
 
    def do_northeast(self, arg):
        """Go northeast if possible."""
        old_loc = user.location
        if user.move('northeast'):
            self.update_prompt(old_loc, NORTHEAST)

    def do_southwest(self, arg):
        """Go southwest if possible."""
        old_loc = user.location
        if user.move('southwest'):
            self.update_prompt(old_loc, SOUTHWEST)

    def do_southeast(self, arg):
        """Go southeast if possible."""
        old_loc = user.location
        if user.move('southeast'):
            self.update_prompt(old_loc, SOUTHEAST)
        
    def do_take(self, arg):
        """Put item(s) in player's inventory if possible.

        Parameters
        ----------
        arg : item's names followed by comma, possibly one.

        Use
        ---
        1. take [item 1], [item2], ... 
        2. take all (put every item in your inventory)
        """
        user.take(arg)

    def complete_take(self, text, line, begidx, endidx):
        """Auto completion when player uses 'take'
        
        Parameters
        ----------
        text : whole line including 'take'
        line : all that comes after 'take'
        """
        return tuple(i+', ' for i in worldRooms[user.location][GROUND] if i.startswith(text))

    def do_drop(self, arg):
        """You drop item(s) on the ground.

        Parameters
        ----------
        arg : item's names followed by comma, possibly one.

        Use
        ---
        1. drop [item 1], [item 2], ...
        2. drop all (empty inventory)
        """
        user.drop(arg)

    def complete_drop(self, text, line, begidx, endix):
        """Auto completion when player uses 'drop'
        
        Parameters
        ----------
        text : whole line including 'take'
        line : all that comes after 'take'
        """
        return tuple(i+', ' for i in user.inventory if i.startswith(text))

    def do_hp(self, arg):
        """Display player's health points"""
        user.showHp()
    
    def do_look(self, arg):
        """Display info about current location."""
        user.displayLoc()

    def do_inv(self, arg):
        """Shows your inventory."""
        user.inv()

    def do_talk(self, arg):
        """Talk to a present NPC

        Parameters
        ----------
        arg : str, npc's name

        """
        user.talk(arg)
    
    def complete_talk(self, text, line, begidx, endix):
        """Auto complete when player uses 'talk' """
        return tuple(i for i in worldRooms[user.location][NPC] if i.startswith(text))

    def sell(self, arg):
        """ todo """
        user.sell(arg)

    def complete_sell(self, text, line, begidx, endix):
        """Auto completion when player uses 'talk'"""
        args_array = line.split(" ")
        if len(args_array) == 2:
            return [npc for npc in worldRooms[user.location][NPC] if npc.startswith(text)]
        elif len(args_array) >= 3:
            return [item for item in user.inventory if item.startswith(text)]

    def do_quit(self, arg):
        """Quit the game."""
        print('See you soon ! Thanks for playing.')
        return 1

os.system('clear')
rpshellPrompt().cmdloop()