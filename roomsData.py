from Const import *

worldRooms = {
        'Home' : {
            DESC : 'This is my home.',
            SHORTDESC : 'home',
            LONGDESC : 'This is my home. There is a welcome sign on the top of the door. It reads "Please knock if I do not know you".',
            GROUND : ['Basic steel sword', 'Health potion'],
            NORTH : 'My garden',
            SOUTH : 'Easten street of Homeland',
            REGION : 'White Mountains',
            NPC : ['Oliver'],
            },

        'My garden' : {
            DESC : 'This is my garden',
            SHORTDESC : 'garden',
            NORTH : 'Nothing important',
            SOUTH : 'Home',
            REGION : 'White Mountains',
            NPC : ['Bob', 'Emma']
            },
        }
