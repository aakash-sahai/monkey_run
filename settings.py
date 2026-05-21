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

# Water Gun Settings
WATER_SPEED = 12

# --- Platform Settings ---
PLATFORM_DEFAULT_HEIGHT = 20
PLATFORM_COLOR = (0, 100, 0)

# --- LEVEL DESIGNS (TILEMAPS) ---
TILE_SIZE = 64

# D = Diamonds F = Food H = Hazard P = Player Start X = Platform W = Water Gun G= Golem
LEVEL_MAPS = [
    # --- LEVEL 1 ---
    [
        '                                                                          ',
        '    D         D               D                      HD               F   ',
        '  XXXXX H    XXXXX           XXXXX         HD       XXXX      H     XXXXX ',
        '         F            H               F    XXXX              XXXXX        ',
        '       XXXX         XXXXX           XXXX                 XXXX             ',
        '                                   H     H                                ',
        '    P        D       F      H             D          H         D     F    ',
        'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX',
    ],
    # --- LEVEL 2 ---
    [
        '                                                                          ',
        '    D         F               H                      HD               D   ',
        '  XXXXX      XXXX           XXXXX          F        XXXX      H     XXXXX ',
        '         H            W               H    XXXX              XXXXX        ',
        '       XXXX         XXXXX           XXXX                 XXXX             ',
        '  W                                H     H                         H      ',
        '  PFFFH      D       F      H       W   D          H     W   F      D     ',
        'XXXXXXXXXXXXXXXX   XXXXX   XXXXXXXXXXXXXXXXXXXXX   XXXXXXXXXXXXXXXXXXXXXXX',
    ],
    # --- LEVEL 3 ---
    [
        '                                                                          ',                     
        '                                   XXXXXXXXX                              ',
        '             F               HF                     HD               D    ',
        '            XXXX           XXXXX             G     XXX        H  F  XXXXX ',
        '         H            G               H    XXXX          G     XXXXX      ',
        '       XXXX         XXXXX           XXXX                 XXXX             ',
        '   P    D  W         H       W F D    G  F  H      W   F      D G         ',
        'XXXXXXXXXXXXXXXX   XXXXX   XXXXXXXXXXXXXXXXXXXXX   XXXXXXXXXXXXXXXXXXXXXXX',
    ]
    ]