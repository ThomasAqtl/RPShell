"""

"""

import cmd
import os
#from termcolor import colored

from player import player, worldNpcs
from roomsData import *
from ItemsData import *


user = player(15,30,'Home')


class rpshellPrompt(cmd.Cmd):

    prompt = BCYAN+worldRooms[user.location][REGION].upper()+'\u276D '+user.location+' \u232A'+ RESET


    def default(self, arg):
        print('I do not know this command. Type "help" to list available commands.')


    def update_prompt(self, loc, npc):
        if npc == '' :
            self.prompt = BCYAN+worldRooms[user.location][REGION].upper()+' \u276D '+ loc +' \u232A'+ RESET
        else:
            self.prompt = BCYAN+worldRooms[user.location][REGION].upper()+' \u276D '+ loc +' \u232A'+ GREEN + npc + ' \u232A' + RESET
    
    def do_clear(self, arg):
        """Clear console."""
        os.system('clear')

    def do_east(self, arg):
        """Go east if possible."""
        if user.move('east'):
            self.update_prompt(user.location, '')
    
    def do_west(self, arg):
        """Go west if possible."""
        if user.move('west'):
            self.update_prompt(user.location, '')

    def do_north(self, arg):
        """Go north if possible."""
        if user.move('north'):
            self.update_prompt(user.location, '')

    def do_south(self, arg):
        """Go south if possible."""
        if user.move('south'):
            self.update_prompt(user.location, '')

    def do_northwest(self, arg):
        """Go northwest if possible."""
        if user.move('northwest'):
            self.update_prompt(user.location, '')
 
    def do_northeast(self, arg):
        """Go northeast if possible."""
        if user.move('northeast'):
            self.update_prompt(user.location, '')

    def do_southwest(self, arg):
        """Go southwest if possible."""
        if user.move('southwest'):
            self.update_prompt(user.location, '')

    def do_southeast(self, arg):
        """Go southeast if possible."""
        if user.move('southeast'):
            self.update_prompt(user.location, '')
        
    def do_take(self, arg):
        """Put given item(s) in your inventory if possible.
        -- take [item 1], [item2], ... 
        -- take all (put every item in your inventory)
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
        """Drop given item(s) on the ground.
        -- drop [item 1], [item 2], ...
        -- drop all (empty inventory)
        """
        user.drop(arg)

    def complete_drop(self, text, line, begidx, endix):
        """Auto completion when player uses 'drop'
        
        Parameters
        ----------
        text : whole line including 'take'
        line : all that comes after 'take'
        """
        return tuple(i.name+', ' for i in user.inventory if i.name.startswith(text))

    def do_hp(self, arg):
        """Display your health points"""
        user.showHp()
    
    def do_look(self, arg):
        """Display info about current location."""
        user.look()

    def do_inv(self, arg):
        """Shows your inventory."""
        user.inv()

    def do_talk(self, arg):
        """Talk to a present NPC.
        -- talk [NPC]
        """
        if user.talk(arg):
            self.update_prompt(user.location, arg)

    def complete_talk(self, text, line, begidx, endix):
        """Auto completion when player uses 'talk'"""
        return tuple(i for i in worldRooms[user.location][NPC] if i.startswith(text))

    def do_shop(self, arg):
        """Shows NPC's shop if player is talking to a NPC"""
        user.shop()

    def do_sell(self, arg):
        """Sell item(s) to the NPC you are talking to.
        -- sell [item1], [item2], ...
        -- sell all (sell all item(s) you have)
        """
        user.sell(arg)

    def complete_sell(self, text, line, begidx, endix):
        """Auto compeltion when player uses 'sell'"""
        return tuple(i.name+', ' for i in user.inventory if i.name.startswith(text))

    def do_buy(self, arg):
        """Buy item(s) to the NPC you are talking to.
        -- buy [item1], [item2], ...
        -- buy all (buy every available items in the current shop)
        """
        user.buy(arg)

    def complete_buy(self, text, line, begidx, endix):
        """Auto completion when player uses 'buy'"""
        return tuple(i+', ' for i in worldNpcs[user.host][STOCK] if i.startswith(text))

    def do_equip(self, arg):
        """Equip yourself with item(s) if possible.
        -- equip [item1], [item2], ...
        """
        user.equip(arg)

    def complete_equip(self, text, line, begidx, endix):
        """Auto completion when player uses 'equip'"""
        return tuple(i.name+', ' for i in user.inventory if i.type == 'Weapon' \
            or i.type == 'Panoply')

    def do_leave(self, arg):
        """Leave conversation with NPC."""
        if user.leave():
            self.update_prompt(user.location, '')

    def do_quit(self, arg):
        """Quit the game."""
        print('See you soon ! Thanks for playing.')
        return 1

    # for shorter commands
    do_i =  do_inv
    do_l =  do_look
    do_s = do_south
    do_se = do_southeast
    do_sw = do_southwest
    do_n = do_north
    do_ne = do_northeast
    do_nw = do_northwest
    do_e = do_east
    do_w = do_west

if __name__ == "__main__":
    os.system('clear')
    rpshellPrompt().cmdloop()