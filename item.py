from ItemsData import *

class item():

    def __init__(self, name: str, **kwargs: dict):

        # regular parameters
        self.name = name
        self.desc = kwargs.get(DESC)
        self.grounddesc = kwargs.get(GROUNDDESC)
        self.weight = kwargs.get(WEIGHT)

        # optionnal parameters, depend on the item
        if CONSUMABLE in kwargs:
            self.consumable = kwargs.get(CONSUMABLE)
        else:
            self.consumable = False

        if USABLE in kwargs:
            self.usable = kwargs.get(USABLE)
        else:
            self.usable =  False

        if DAMAGE in kwargs:
            self.damage = kwargs.get(DAMAGE)
        
        if DEFENSE in kwargs:
            self.defense = kwargs.get(DEFENSE)
        
        if LVL in kwargs:
            self.lvl = kwargs.get(LVL)

        if SELL_PRICE in kwargs:
            self.sell_price = kwargs.get(SELL_PRICE)
        
        if BUY_PRICE in kwargs:
            self.buy_price = kwargs.get(BUY_PRICE)

        if TYPE in kwargs:
            self.type = kwargs.get(TYPE)

    # return the name of the item after printing info about it
    def __str__(self) -> str:
        return self.name

    # the name of the item is unique (i.e. different stats => different item)
    def __eq__(self, other) -> bool:
        try:
            return self.name == other.name
        except:
            return False

    def __hash__(self):
        return hash((self.name))