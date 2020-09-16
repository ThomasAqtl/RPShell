from ItemsData import *
from roomsData import *
from npcData import *
from columnar import columnar
import collections
import textwrap
import random

class player():
    
    def __init__(self, hp, hp_max, location):
        self.hp = hp
        self.hpmax = hp_max
        self.inventory = []
        self.capacity = 50
        self.location = location
        self.gold = 0

    def heal(self, amount):
        """Deals [amount] hp"""
        print('You heal yourself {0} hp. '.format(amount), end="")
        self.hp()
        self.hp = min(self.hpmax,self.hp + amount)

    def suffer(self, amount):
        """Deal [amount] damages"""
        self.hp = max(0, self.hp - amount)
        if self.hp == 0:
            print('You died !')
        else:
            print('You have been hit ! You lost {0} hp. '.format(amount), end="")
            self.showHp()
    
    # \u25AA and u25AB are python encodings for little white and black squares
    def showHp(self):
        """Display current health points"""
        print('Health : ',HP * self.hp,MHP * (self.hpmax-self.hp),' ',self.hp,'/',self.hpmax, sep='')

    
    def take(self, arg):
        """
        Parameters 
        ----------
        arg : list of items to take, possibly one element
        """
        if len(worldRooms[self.location][GROUND]) == 0:
            print('There is no item to take here.')

        else:
            # if no arguments
            if arg == '':
                print('What do your want to take ? type "look" to see what is on the ground.')

            elif arg == 'all':
                old_ground = []
                for item in worldRooms[self.location][GROUND]:
                    if self.weight() + worldItems[item][WEIGHT] <= self.capacity:
                        self.inventory.append(item)
                        old_ground.append(item)
                        print(item, ' added to your inventory.')
                    else:
                        print('Your inventory is full !')
                for item in old_ground:
                    worldRooms[self.location][GROUND].remove(item) 
                        
            else:
                # transform input into list filled with items to take
                temp = ["".join(i) for i in arg]
                # remove the last ',' from user input
                if temp[-1] ==  ',' : temp.pop()
                items = "".join(temp).split(', ')

                old_ground = []
                wrong_item = False
                for item in items:
                    try:
                        if worldItems[item][WEIGHT] + self.weight() <= self.capacity:
                            self.inventory.append(item)
                            old_ground.append(item)
                            worldRooms[self.location][GROUND].remove(item)
                            print(item, 'added to your inventory.')
                        else:
                            print('Your inventory is full !')
                            return
                    except:
                        wrong_item =  True
                
                if wrong_item:
                    print('\nSome items do not exists or are not in the room.')
            
                                    
    def drop(self, arg):
        """Remove items from the inventory and leave them on the current room's ground"""
        if (len(self.inventory)) ==  0:
                print('You have nothing to drop, your inventory is empty.')
        else:
            if arg == '':
                print('What do you want to drop ?')

            elif arg ==  'all':
                for item in self.inventory:
                    worldRooms[self.location][GROUND].append(item)
                self.inventory.clear()
                print('You have emptied your bag on the ground.')

            else:
                # transform input into list filled with items to take
                temp = ["".join(i) for i in arg]
                if temp[-1] ==  ',' : temp.pop() # remove the last ',' from user input
                items = "".join(temp).split(', ')

                for item in items:
                    try:
                        self.inventory.remove(item)
                        worldRooms[self.location][GROUND].append(item)
                        print('You dropped', item)
                    except:
                        print('You do not have this item. Use <inv> to see your inventory.')
                        return
        
    
    def inv(self):
        """Shows the player's inventory"""
        
        if len(self.inventory) == 0:
            print('Your inventory is empty.')

        else: # counts qty/items and retrieve infos about them
            counter = collections.Counter(self.inventory)
            L = []
            weight = []
            prices = []
            for i in counter.keys():
                l = []
                l.append(i)
                l.append(counter[i])
                l.append(worldItems[i][PRICE])
                l.append(worldItems[i][WEIGHT])
                l.append(worldItems[i][DESC])
                weight.append(worldItems[i][WEIGHT])
                prices.append(worldItems[i][PRICE])
                L.append(l)
            
            # Sums prices and weight for total, and max for capacity. 
            L.append(['TOTAL', len(self.inventory), sum(j for j in prices), sum(i for i in weight), ''])
            L.append(['MAX', 'N/A', 'N/A', self.capacity, 'N/A'])

            # Better display
            headers = ['Name', 'Quantity', 'Unit price', 'Weight', 'About']
            L.insert(len(set(self.inventory)), ['-'*len(headers[i]) for i in range(len(headers))])
            L.insert(len(L)-1, ['-'*len(headers[i]) for i in range(len(headers))])
            print(INVERTED+BOLD+'INVENTORY :'+RESET)
            print(columnar(L, headers, no_borders=True, justify=['l','r','r','r','l']))

    def move(self, direction):
        """If possible, moves the player to an adjacent location according to parameter
        
        Parameters
        ----------
        direction : str, has to be in (north, south, east, west, northwest, northeast, southwest, southeast)

        Returns
        -------
        Boolean :  True if the move is possible, False if not.
        """
        
        loc = self.location

        if direction in worldRooms[loc]:
            if worldRooms[loc][direction] in worldRooms:
                self.location = worldRooms[loc][direction]
                print('You move', direction)
                return True
            else:
                print('[INFO] The room you are trying to join is not structured yet.')
                return False
        else:
            print('You cannot go', direction)
            return False

    def displayLoc(self):
        """Display infos about the current location : current room description,
        takeable items, present npcs and possible exits."""

        # highlighted location name
        loc = self.location
        print(INVERTED+BOLD+loc.upper()+RESET)

        if loc in worldRooms : 

            # description of the room
            print('\n'.join(textwrap.wrap(worldRooms[loc][DESC], SCREEN_WIDTH)))
            print()

            # Takeable items (items on the ground)
            print(INVERTED+BOLD+'TAKEABLE ITEMS :'+RESET)
            try:
                L = []
                ground = worldRooms[self.location][GROUND]
                if len(ground) > 0:
                    for item in ground:
                        l = []
                        l.extend([item, worldItems[item][GROUNDDESC]])
                        L.append(l)
                headers = ['Name', 'Description']
                print(columnar(L, headers, no_borders=True))
            except:
                print('None\n')

            # Present NPCs
            print(INVERTED+BOLD+'PRESENT NPC(S) :'+RESET)
            try:
                L = []
                npcs = worldRooms[self.location][NPC]
                if len(npcs) > 0:
                    for npc in npcs:
                        l = []
                        l.extend([npc, worldNpcs[npc][TYPE]])
                        L.append(l)
                headers = ['Name', 'Type']
                print(columnar(L, headers, no_borders=True))
            except:
                print('None\n')


            # All possible exits with associated room
            exits = []
            for direction in {NORTH,SOUTH,EAST,WEST,NORTHEAST,NORTHWEST,SOUTHEAST,SOUTHWEST}:
                if direction in worldRooms[loc].keys():
                    exits.append([direction.upper(), worldRooms[loc][direction]])
            
            print(INVERTED+BOLD+'POSSIBLE PATHS :'+RESET)
            headers = ['Direction','Room']
            print(columnar(exits, headers, no_borders=True))
        else:
            print('There is no information about this room.')

    def talk(self, arg):
        """Talk to a specific npc. If the NPC can trade items, his shop and player's inventory are displayed."""
        #Todo ajouter carac des items dans le shop
        # check if npc are present in the room
        if len(worldRooms[self.location][NPC]) == 0:
            print('There is none to talk to here.')
        
        else:
            if arg in worldRooms[self.location][NPC]:
                print('\u001b[33;1m' + arg + ' : \u001b[0m' + '\u001b[33m' + random.choice(worldNpcs[arg][LINE]) + '\u001b[0m' )
        
            shop = []
            for item in worldNpcs[arg][STOCK]:
                shop.append([item, worldItems[item][PRICE], worldItems[item][DESC]])
            
            print('\u001b[7m\u001b[33;1m'+arg+' shop \u001b[0m')
            headers = ('Name', 'Price', 'Description')
            print(columnar(shop, headers, no_borders=True))


            # print player's inventory (to sell items)
            self.inv()

    def sell(self, arg):
        """sell items to specific NPC."""
        pass
            
    def buy(self, arg):
        """buy items to specific NPC."""
        pass


    def weight(self):
        return sum(worldItems[item][WEIGHT] for item in self.inventory)
