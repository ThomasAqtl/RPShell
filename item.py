from ItemsData import *

class item():

    def __init__(self, name: str, desc: str, grounddesc: str, weight: int, consumable: bool, usable: bool):
        self.name = name
        self.desc = desc
        self.grounddesc = grounddesc
        self.weight = weight
        self.consumable = consumable
        self.usable = usable

    def __str__(self):
        print('NAME : ', self.name)
        print('DESC : ', self.desc)
        print('WEIGHT : ', self.weight)
        print('CONSUMABLE : ', self.consumable)
        print('USABLE : ', self.usable)
        return self.name

class weapon(item):

    def __init__(self, name: str, desc: str, grounddesc: str, weight: int, damage: int, lvl: int):
        self.name = name
        self.desc = desc
        self.grounddesc = grounddesc
        self.weight = weight
        self.consumable = False
        self.usable =  True
        self.damage = damage
        self.lvl = lvl

class panoply(item):

    def __init__(self, name: str, desc: str, grounddesc: str, weight: int, defense: int, lvl: int):
        self.name = name
        self.desc = desc
        self.grounddesc = grounddesc
        self.weight = weight
        self.consumable = False
        self.usable =  True
        self.defense = defense
        self.lvl = lvl

class potion(item):

    def __init__(self, name: str, desc: str, weight: int):
        self.name = name
        self.desc = desc
        self.weight = weight
        self.consumable = True
        self.usable = False

def main():
    arg = [i for i in worldItems['Basic steel sword'].values()]
    item2 = weapon('Basic steel sword', *arg)

    print(item2)


if __name__ == "__main__":
    main()