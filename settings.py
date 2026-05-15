# Game Settings
SCREEN_WIDTH = 1600
SCREEN_HEIGHT = 1000
FPS = 60

# Physics
GRAVITY = 0.8
JUMP_STRENGTH = -16
PLAYER_SPEED = 5

MONKEY_HEIGHT = 70
MONKEY_COLOR = 'orange'

# Game Balance
STARTING_ENERGY = 100
ENERGY_DRAIN_RATE = 0.02  
FOOD_RECOVERY = 25

HAZARD_SIZE = 40
HAZARD_COLOR = (255, 0, 0)      
HAZARD_DAMAGE_RATE = 2

# --- Platform Settings ---
PLATFORM_DEFAULT_HEIGHT = 20
PLATFORM_COLOR = (0, 100, 0)

# --- NEW LEVEL DESIGN (TILEMAP) ---
TILE_SIZE = 64

# X = Platform, H = Hazard, D = Diamond, F = Food, P = Player Start
# Each line is a row. Space = empty air.
LEVEL_MAP = [
    '                                                ',
    '    D         D               D                 ',
    '  XXXXX H    XXXXX           XXXXX         HD   ',
    '         F            H               F    XXXX ',
    '       XXXX         XXXXX           XXXX        ',
    '                                                ',
    '    P        D              H             D     ',
    'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX',
]