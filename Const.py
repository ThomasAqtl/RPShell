# key words for descriptions : items, npcs, rooms...
DESC = 'desc'
LONGDESC = 'longdesc'
SHORTDESC = 'shortdesc'
GROUNDDESC = 'grounddesc'
GROUND = 'ground'

# key words for movements
NORTH = 'north'
SOUTH = 'south'
EAST = 'east'
WEST = 'west'
NORTHEAST = 'northeast'
NORTHWEST = 'northwest'
SOUTHEAST = 'southeast'
SOUTHWEST = 'southwest'
REGION = 'region'

# specs for weapons
DAMAGE = 'damage' 
DEFENSE = 'defense'
LVL = 'lvl' 

# key words for consumable effects
HEAL = 'heal'
HURT = 'hurt'

# key words 
CONSUMABLE = 'consumable' # items that can be eaten
TAKEABLE = 'takeable' # items that can be placed in player's inventory
USABLE = 'usable' # for items that can be used as an equipments and not 'consumed'
TRADABLE = 'tradable' # form items that can be sold or not
SELL_PRICE = 'sell_price'
BUY_PRICE = 'buy_price'
WEIGHT = 'weight'

# key words for npcs
TYPE = 'type'
STOCK = 'stock'
WALLET = 'wallet'
WELCOME_LINE = 'welcome_line'
BYE_LINE =  'bye_line'
NPC =  'npc'
MOBS = 'mobs'

SCREEN_WIDTH = 80

# key word for special characters and colors
INVERTED = '\u001b[7m'
BOLD = '\u001b[1m'
RESET = '\u001b[0m'

YELLOW = '\u001b[33m'
BYELLOW = YELLOW.replace('m',';1m')

CYAN = '\u001b[36m'
BCYAN = CYAN.replace('m',';1m')

MAGENTA = '\u001b[35m'
BMAGENTA = MAGENTA.replace('m',';1m')

GREEN = '\u001b[32m'
BGREEN = GREEN.replace('m',';1m')

RED = '\u001b[31m'
BRED = RED.replace('m',';1m')

GREY = '\u001b[30m'
BGREY = GREY.replace('m',';1m')

PLUS = '\u2191'
MINUS = '\u2193'

HP = '\u25AA'
MHP = '\u25AB' # Missing HP