from Const import *


worldItems = {
        'Basic steel sword' : {
            TYPE : 'Weapon',
            DESC : 'A simple sword, made of steel. Average size, average weight.',
            GROUNDDESC : 'A Basic steel sword is ready to be used right there.',
            USABLE : True,
            WEIGHT : 2,
            DAMAGE : 5,
            LVL : 1,
            SELL_PRICE : 10,
            BUY_PRICE : 20,
            },

        'Basic magic wand' : {
            TYPE : 'Weapon',
            TAKEABLE : True,
            TRADABLE : True,
            DAMAGE : 4,
            SELL_PRICE : 2,
            BUY_PRICE : 5,
            LVL : 1,
            WEIGHT : 6,
            USABLE : True,
            CONSUMABLE : False,
            GROUNDDESC : 'A magic wand lies on the ground.',
            DESC : 'This is a description',
            },
        
        'Small health potion' : {
            TAKEABLE : True,
            TRADABLE : True,
            SELL_PRICE : 2,
            BUY_PRICE : 4,
            WEIGHT : 1,
            CONSUMABLE : True,
            HEAL : 5,
            GROUNDDESC : 'A Small health potion is on that shelf.',
            DESC : 'They say drinking this potion can sometimes save life.',
            },

        'Health potion' : {
            TYPE : 'Potion',
            TAKEABLE : True,
            TRADABLE : True,
            SELL_PRICE : 4,
            BUY_PRICE : 8,
            WEIGHT : 1,
            CONSUMABLE : True,
            HEAL :  10,
            GROUNDDESC : 'A red cup is on that shelf. It looks like a Health potion.',
            DESC : 'This is a description',
            },

        'Wind Cloak' : {
            TYPE : 'Panoply',
            TAKEABLE :  True,
            TRADABLE : True,
            SELL_PRICE : 10,
            BUY_PRICE : 25,
            WEIGHT : 10,
            DEFENSE : 10,
            GROUNDDESC : 'Grey cloak.',
            DESC : 'A grey and used cloak but still functionnal.',
        }
    }
