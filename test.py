LVL = 'lvl'
DAMAGE = 'damage'

Items = {
    'Sword':{
        LVL : 1,
        DAMAGE : 5,
    },

    'Wand':{
        LVL : 1,
        DAMAGE : 3,
    },
}

class player():
    def __init__(self):
        self.inventory = []

class item():
    def __init__(self, name: str, **kwarg):
        self.name = name
        self.dmg = kwarg.get(DAMAGE)
        self.lvl = kwarg.get(LVL)

    def __eq__(self, other):
        return self.name == other.name

    def __str__(self):
        return self.name

if __name__ == "__main__":
    user = player()
    for i in Items.keys():
        it = item(i, **Items[i])
        user.inventory.append(it)

    # check user's inventory
    print('Inventory after append items :')
    for i in user.inventory:
        print(i)

    # let's say i want the user to drop items
    items_name = [i for i in Items.keys()]
    items_to_drop = [item(i, **Items[i]) for i in items_name]
    for i in items_to_drop:
        user.inventory.remove(i)

    # check again
    print('Inventory after removing items:')
    for i in user.inventory:
        print(i)