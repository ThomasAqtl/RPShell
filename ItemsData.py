from Const import *


worldItems = {
        'Basic steel sword' : {
            DESC : 'A simple sword, made of steel. Average size, average weight.',
            GROUNDDESC : 'A Basic steel sword is ready to be used right there.',
            WEIGHT : 2,
            DAMAGE : 5,
            LVL : 1,
            },

        'Basic magic wand' : {
            TAKEABLE : True,
            TRADABLE : True,
            DAMAGE : 4,
            PRICE : 2,
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
            PRICE : 2,
            WEIGHT : 1,
            CONSUMABLE : True,
            HEAL : 5,
            GROUNDDESC : 'A Small health potion is on that shelf.',
            DESC : 'They say drinking this potion can sometimes save life.',
            },

        'Health potion' : {
            TAKEABLE : True,
            TRADABLE : True,
            PRICE : 4,
            WEIGHT : 1,
            CONSUMABLE : True,
            HEAL :  10,
            GROUNDDESC : 'A red cup is on that shelf. It looks like a Health potion.',
            DESC : 'This is a description',
            },
        }
