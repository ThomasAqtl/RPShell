from ItemsData import *
from item import *
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
        self.gold = 50
        self.host = ''
        self.weapon = None
        self.panoply = None

    def heal(self, amount: int):
        """
        Parameters
        ----------
        amount : int
        """
        print('You heal yourself {0} hp. '.format(amount), end="")
        self.hp()
        self.hp = min(self.hpmax,self.hp + amount)

    def suffer(self, amount):
        """Lose <amount> hp."""
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

    
    def take(self, arg): # FUNCTIONNAL
        """
        Parameters 
        ----------
        arg : list of items to take, possibly one element
        """
        try:
            if len(worldRooms[self.location][GROUND]) == 0:
                print('There is no item to take here.')

            else:
                # if no arguments
                if arg == '':
                    print('What do you want to take ? type "look" to see what is on the ground.')

                elif arg == 'all':
                    old_ground = []
                    for i in worldRooms[self.location][GROUND]:
                        if self.weight() + worldItems[i][WEIGHT] <= self.capacity:
                            taken_item = item(i, **worldItems[i])
                            self.inventory.append(taken_item)
                            old_ground.append(taken_item)
                            print(i, 'added to your inventory.')
                        else:
                            print('Your inventory is full !')
                    for i in old_ground:
                        worldRooms[self.location][GROUND].remove(i.name) 
                            
                else:
                    # transform input into list filled with items to take
                    temp = ["".join(i) for i in arg]
                    if temp[-1] ==  ',' : temp.pop() # remove the last automatic',' from user input
                    items_to_take_names = "".join(temp).split(', ')

                    for i in items_to_take_names:
                        try:
                            if worldItems[i][WEIGHT] + self.weight() <= self.capacity:
                                self.inventory.append(item(i, **worldItems[i]))
                                worldRooms[self.location][GROUND].remove(i)
                                print(i, 'added to your inventory.')
                            else:
                                print('Your inventory is full !')
                                return
                        except:
                            print('\nSome items do not exist or are not in the room.')
        except:
            print('There is no item to take here.') # in case no GROUND key in the dictionnary

    def drop(self, arg):
        """Remove items from the inventory and leave them on the current room's ground"""
        if (len(self.inventory)) ==  0:
                print('You have nothing to drop, your inventory is empty.')
        else:
            if arg == '':
                print('What do you want to drop ?')

            elif arg ==  'all':
                for i in self.inventory:
                    worldRooms[self.location][GROUND].append(i.name)
                self.inventory.clear()
                print('You have emptied your bag on the ground.')

            else:
                # transform input into list filled with items to take
                temp = ["".join(i) for i in arg]
                if temp[-1] ==  ',' : temp.pop() # remove the last ',' from user input
                items_to_drop_names = "".join(temp).split(', ')
                
                for i in items_to_drop_names:
                    try:
                        item_to_drop = item(i, **worldItems[i])
                        self.inventory.remove(item_to_drop)
                        worldRooms[self.location][GROUND].append(item_to_drop.name)
                        print(i, 'dropped.')
                    except:
                        print(i, 'is not in your inventory.')
        
    
    def inv(self):
        """Shows the player's inventory"""
        
        if len(self.inventory) == 0:
            print('Your inventory is empty.')
            print(BYELLOW+str(self.gold)+' gold.'+RESET)

        else: # counts qty/items and retrieve infos about them
            counter = collections.Counter(self.inventory)
            L = []
            L.append([BYELLOW+'GOLD'+RESET, YELLOW+str(self.gold)+RESET, '', '', ''])
            weight = []
            prices = []
            for i in counter.keys():
                l = []
                l.append(i)
                l.append(counter[i])
                l.append(i.sell_price)
                l.append(i.weight)
                l.append(i.desc)
                weight.append(i.weight)
                prices.append(i.sell_price)
                L.append(l)
            
            # Sums prices and weight for total, and max for capacity. 
            L.append(['TOTAL', len(self.inventory), sum(j for j in prices), sum(i for i in weight), ''])
            L.append(['MAX', 'N/A', 'N/A', self.capacity, 'N/A'])

            # Better display
            headers = ['Name', 'Quantity', 'Sell price', 'Weight', 'Description']
            L.insert(1, ['-'*len(headers[i]) for i in range(len(headers))])
            L.insert(len(set(self.inventory))+2, ['='*len(headers[i]) for i in range(len(headers))])
            L.insert(len(L)-1, ['='*len(headers[i]) for i in range(len(headers))])
            print(INVERTED+BOLD+'INVENTORY :'+RESET)
            print(columnar(L, headers, no_borders=True, justify=['l','r','r','r','l']))

    def move(self, direction: str) -> bool:
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
                self.host = ''
                print('You move', direction)
                return True
            else:
                print('[INFO] The room you are trying to join is not structured yet.')
                return False
        else:
            print('You cannot go', direction)
            return False

    def look(self):
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
                ground = worldRooms[loc][GROUND]
                if len(ground) > 0:
                    for items in ground:
                        l = []
                        i = item(items, **worldItems[items])
                        l.extend([i, i.grounddesc])
                        L.append(l)
                headers = ['Name', 'Description']
                print(columnar(L, headers, no_borders=True, justify=['r','l']))
            except:
                print('None\n')

            # Present NPCs
            print(INVERTED+BOLD+'PRESENT NPC(S) :'+RESET)
            try:
                L = []
                npcs = worldRooms[loc][NPC]
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
            return False
        
        elif arg == '':
            print('Who do you want to talk to ? Type "look" to see present NPC(s)')
            return False
        
        elif arg in worldRooms[self.location][NPC]:
            print(BOLD + BGREEN + arg + ' : ' + RESET + GREEN+ random.choice(worldNpcs[arg][WELCOME_LINE]) + RESET )
    
            if len(worldNpcs[arg][STOCK]) > 0:
                shop = []
                for item in worldNpcs[arg][STOCK]:
                    shop.append([item, worldItems[item][BUY_PRICE], worldItems[item][DESC]])
                
                print(INVERTED +BOLD + BGREEN +arg+' shop :'+RESET)
                headers = ('Name', 'Price', 'Description')
                print(columnar(shop, headers, no_borders=True))
            
            else:
                print(BGREEN+arg+RESET+'\'s shop is empty.')

            # print player's inventory (to sell items)
            self.inv()
            self.host = arg
            return True

        else:
            print('The person you want to talk to does not exists or is not in the room.')
            return False

    def leave(self):
        """Leave the current NPC"""
        
        if self.host == '':
            print('You are not talking to anyone right now.')
            return False
        
        else:
            print(BGREEN + BOLD + self.host + ' : ' + RESET + GREEN + random.choice(worldNpcs[self.host][BYE_LINE]) + RESET )
            self.host = ''
            return True

    def shop(self):
        """Show host shop"""
        stock = worldNpcs[self.host][STOCK]

        if self.host == '':
            print('You are not talking to anyone right now.')
        
        elif len(stock) > 0:
            shop = []
            for i in stock:
                shop.append([i, worldItems[i][BUY_PRICE], worldItems[i][DESC]])
            
            print(INVERTED +BOLD + BGREEN + self.host +' shop :'+RESET)
            headers = ('Name', 'Price', 'Description')
            print(columnar(shop, headers, no_borders=True))
        
        else:
            print(BGREEN+self.host+RESET+'\'s shop is empty.')

    def sell(self, arg):
        """sell items to specific NPC."""

        if self.host != '':
            if arg == '':
                print ('What do you want to sell ?')
            
            elif arg == 'all':
                sold_items = []
                for i in self.inventory:
                    worldNpcs[self.host][STOCK].append(i.name)
                    sold_items.append(i)
                    self.gold += worldItems[i.name][SELL_PRICE]
                    print(i.name +' sold for ' + BYELLOW + str(worldItems[i.name][SELL_PRICE]) + \
                        ' gold.' + RESET + GREEN + PLUS +RESET)
                for i in sold_items:
                    self.inventory.remove(i)
            
            else:
                # lines 334 -> 335 transform input into list filled with items' names
                temp = ["".join(i) for i in arg]
                if temp[-1] ==  ',' : temp.pop() # remove the last ',' from user input
                items_to_sell_names = "".join(temp).split(', ') 
                
                for i in items_to_sell_names:
                    try:
                        item_to_sell = item(i, **worldItems[i])
                        self.inventory.remove(item_to_sell)
                        worldNpcs[self.host][STOCK].append(item_to_sell.name)
                        self.gold += worldItems[i][SELL_PRICE]
                        print(i +' sold for ' + BYELLOW + str(worldItems[i][SELL_PRICE]) +\
                             ' gold.' + RESET + GREEN + PLUS + RESET)
                    except:
                        print(i, 'is not in your inventory.')
        else:
            print('You need to be talking to a NPC to sell items. Use "look" to see present NPCs.')
        
    def buy(self, arg):
        """buy items to specific NPC."""
        if self.host != '':
            if arg == '':
                print ('What do you want to buy ? Use "shop" to see '+BGREEN+self.host+RESET+' \'s shop.')
            
            elif arg == 'all':
                items_to_buy_names = []
                for i in worldNpcs[self.host][STOCK]:
                    if worldItems[i][BUY_PRICE] <= self.gold:
                        if worldItems[i][WEIGHT] + self.weight() <= self.capacity:
                            self.inventory.append(item(i, **worldItems[i]))
                            items_to_buy_names.append(i)
                            self.gold -= worldItems[i][BUY_PRICE]
                            print(i + ' bought for ' + BYELLOW + str(worldItems[i][BUY_PRICE]) + ' gold.' 
                            + RESET + RED + MINUS + RESET )
                        else:
                            print(i, 'is too heavy. You cannot buy it.')
                    else:
                        print(i, 'is too expensive. You need', worldItems[i][BUY_PRICE] - self.gold, 'more gold to buy it.')
                
                for i in items_to_buy_names:
                    worldNpcs[self.host][STOCK].remove(i)

            else:
                # lines 378 -> 380 transform input into list filled with items' names
                temp = ["".join(i) for i in arg]
                if temp[-1] ==  ',' : temp.pop() # remove the last ',' from user input
                items_to_buy_names = "".join(temp).split(', ') 

                for i in items_to_buy_names:
                    #try:
                        if self.gold >= worldItems[i][BUY_PRICE]:
                            if worldItems[i][WEIGHT] <= self.capacity - self.weight():
                                worldNpcs[self.host][STOCK].remove(i)
                                self.inventory.append(item(i, **worldItems[i]))
                                self.gold -= worldItems[i][BUY_PRICE]
                                print(i+' bought for '+BYELLOW+str(worldItems[i][BUY_PRICE])+' gold.'+RESET+RED+MINUS+RESET)
                            else:
                                print(i+' exceeds your inventory capacity. Transaction cancelled.')
                        else:
                            print('You cannot buy '+i+'. You need '+BYELLOW+str(int(worldItems[i][BUY_PRICE])-self.gold)+' gold.'+RESET)
                   # except:
                    #    print('Some item(s) do no exist or are not in the shop.')
        else:
            print('You need to be talking to a NPC to buy items. Use "look" to see present NPCs.')


    def stuff(self):
        if self.weapon is None and self.panoply is None:
            print('You do not have any equipment at the moment.')

        else:
            L = list()
            if self.weapon is not None:
                l1 = list()
                l1.extend(['WEAPON', self.weapon.name, worldItems[self.weapon.name][DAMAGE], 'N/A', worldItems[self.weapon.name][DESC]])
                L.append(l1)
            if self.panoply is not None:
                l2 = list()
                l2.extend(['PANOPLY', self.panoply.name, 'N/A', worldItems[self.panoply.name][DEFENSE], worldItems[self.panoply.name][DESC]])
                L.append(l2)

            headers = ['TYPE', 'NAME', 'DAMAGE', 'DEFENSE', 'ABOUT']
            print(columnar(L, headers, no_borders=True))

    def equip(self, arg: item):
        if arg == '':
            print('What do you want to equip ? Use "inv" to see your inventory.')
        
        else:
            try:
                # lines 408 -> 412 transform input into list filled with items (objects) to equip
                temp = ["".join(i) for i in arg]
                if temp[-1] ==  ',' : temp.pop() # remove the last comma from user input
                items_name = "".join(temp).split(', ') 
                items_to_equip = [item(i, **worldItems[i]) for i in items_name]

                for i in items_to_equip: 
                    if worldItems[i.name][TYPE] == 'Weapon':
                        self.weapon = i
                        self.inventory.remove(i)
                        print(i, 'equiped.')
                    elif worldItems[i.name][TYPE] == 'Panoply':
                        self.panoply = i
                        self.inventory.remove(i)
                        print(i, 'equiped.')
                    else:
                        print(i, 'cannot be equiped.')
                    
            except:
                print('Some item(s) do not exist.')

    def unequip(self, arg: item):
        if self.weapon is None and self.panoply is None:
            print('You do not have any equipment at the moment.')

        elif arg == 'all':
            if self.weapon is not None:
                self.inventory.append(self.weapon)
                print(self.weapon, 'unequiped.')
                self.weapon = None
            if self.panoply is not None:
                self.inventory.append(self.panoply)
                print(self.panoply, 'unequiped.')
                self.panoply = None
        
        else:
            try:
                # lines 408 -> 412 transform input into list filled with items (objects) to unequip
                temp = ["".join(i) for i in arg]
                if temp[-1] ==  ',' : temp.pop() # remove the last comma from user input
                items_name = "".join(temp).split(', ') 
                items_to_unequip = [item(i, **worldItems[i]) for i in items_name]
            
                for i in items_to_unequip:
                    if i.type == 'Panoply':
                        if self.panoply is not None:
                            self.inventory.append(i)
                            print(i, 'unequiped.')
                            self.panoply = None
                    elif i.type == 'Weapon':
                        if self.weapon is not None:
                            self.inventory.append(i)
                            print(i, 'unequiped.')
                            self.weapon = None
                    else:
                        print(i, 'is not equiped at the moment')   
            except:
                print('Some item(s) do not exist or are not in your stuff.')
              
    def weight(self):
        return sum(i.weight for i in self.inventory)