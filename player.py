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
        self.weapon = ''
        self.panoply = ''

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
            L.insert(1, ['-'*len(headers[i]) for i in range(len(headers))])
            L.insert(len(set(self.inventory))+2, ['='*len(headers[i]) for i in range(len(headers))])
            L.insert(len(L)-1, ['='*len(headers[i]) for i in range(len(headers))])
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
                    for item in ground:
                        l = []
                        arg = [j for j in worldItems[item].values()]
                        print(item, arg)
                        i = item(*(str(item), tuple(arg)))
                        l.append(i)
                        L.append(l)
                headers = ['Name', 'Description']
                print(columnar(L, headers, no_borders=True))
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
        
        elif arg not in worldNpcs.keys():
            print('[INFO] This NPC is not configured yet.')
            return False

        # elif self.host != '':
        #     print('You are already talking to '+ BGREEN + self.host + RESET + ' at the moment.')
        #     return False

        elif arg == '':
            print('Who do you want to talk to ? Type "look" to see present NPC(s)')
            return False
        
        elif arg in worldRooms[self.location][NPC]:
            print(BOLD + BGREEN + arg + ' : ' + RESET + GREEN+ random.choice(worldNpcs[arg][WELCOME_LINE]) + RESET )
    
            if len(worldNpcs[arg][STOCK]) > 0:
                shop = []
                for item in worldNpcs[arg][STOCK]:
                    shop.append([item, worldItems[item][PRICE], worldItems[item][DESC]])
                
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
            counter = collections.Counter(stock)
            shop = []
            for i in counter.keys():
                shop.append([i, counter[i], worldItems[i][PRICE], worldItems[i][DESC]])
            
            print(INVERTED +BOLD + BGREEN +self.host+' shop :'+RESET)
            headers = ('Name', 'Quantity', 'Price', 'Description')
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
                for item in self.inventory:
                    worldNpcs[self.host][STOCK].append(item)
                    sold_items.append(item)
                    self.gold += worldItems[item][PRICE]
                    print(item +' sold for ' + BYELLOW + str(worldItems[item][PRICE]) + ' gold.' + RESET + GREEN + '\u2191'+RESET)
                for item in sold_items:
                    self.inventory.remove(item)
            
            else:
               # transform input into list filled with items to sell
                temp = ["".join(i) for i in arg]
                # remove the last ',' from user input
                if temp[-1] ==  ',' : temp.pop()
                items = "".join(temp).split(', ') 

                wrong_item = False
                for item in items:
                    try:
                        self.inventory.remove(item)
                        self.gold += worldItems[item][PRICE]
                        worldNpcs[self.host][STOCK].append(item)
                        print(item +' sold for ' + BYELLOW + str(worldItems[item][PRICE]) + ' gold.' + RESET)
                    except:
                        wrong_item = True
                
                if wrong_item:
                    print('Some item do no exist or are not in your inventory.')
        else:
            print('You need to be talking to a NPC to sell items. Use "look" to see present NPCs.')
        
    def buy(self, arg):
        """buy items to specific NPC."""

        if self.host != '':
            if arg == '':
                print ('What do you want to buy ? Use "shop" to see '+BGREEN+self.host+RESET+' \'s shop.')

            elif arg == 'all':
                bought_item = []
                for item in worldNpcs[self.host][STOCK]:
                    if self.gold >= worldItems[item][PRICE]:
                        if worldItems[item][WEIGHT] <= (self.capacity-self.weight()):
                            self.inventory.append(item)
                            self.gold -= worldItems[item][PRICE]
                            print(item+' bought for '+BYELLOW+str(worldItems[item][PRICE])+' gold.'+ RED + MINUS + RESET)
                            bought_item.append(item)
                        else:
                            print(item+' exceeds your inventory capacity. Transaction cancelled.')
                    else:
                        print('You cannot buy '+item+'. You need '+BYELLOW+str(int(worldItems[item][PRICE])-self.gold)+' gold.'+RESET)
                    
                
                for item in bought_item:
                    worldNpcs[self.host][STOCK].remove(item)

            else:
                # transform input into list filled with items to sell
                temp = ["".join(i) for i in arg]
                # remove the last ',' from user input
                if temp[-1] ==  ',' : temp.pop()
                items = "".join(temp).split(', ') 

                wrong_item = False
                for item in items:
                    try:
                        if self.gold >= worldItems[item][PRICE]:
                            if worldItems[item][WEIGHT] <= self.capacity - self.weight():
                                worldNpcs[self.host][STOCK].remove(item)
                                self.inventory.append(item)
                                self.gold -= worldItems[item][PRICE]
                                print(item+' bought for '+BYELLOW+str(worldItems[item][PRICE])+RESET+' gold.')
                            else:
                                print(item+' exceeds your inventory capacity. Transaction cancelled.')
                        else:
                            print('You cannot buy '+item+'. You need '+BYELLOW+str(int(worldItems[item][PRICE])-self.gold)+' gold.'+RESET)
                    except:
                        wrong_item = True
                
                if wrong_item:
                    print('Some item(s) do no exist or are not in the shop.')
        else:
            print('You need to be talking to a NPC to buy items. Use "look" to see present NPCs.')


    def equip(self, arg):
        
        if arg == '':
            print('What do you want to equip ? Use "inv" to see your inventory.')
        
        elif arg not in self.inventory:
            print('The item you want to equip is not in your inventory or does not exist.')
        
        else:
            try:
                if worldItems[arg][TYPE] == 'Weapon':
                    self.weapon = arg
                    self.inventory.remove(arg)
                elif worldItems[arg][TYPE] == 'Panoply':
                    self.panoply = arg
                    self.inventory.remove(arg)
            except:
                print('You cannot equip this item.')

              
    def weight(self):
        return sum(worldItems[item][WEIGHT] for item in self.inventory)