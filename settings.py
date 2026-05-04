# Game Settings
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60

# Physics
GRAVITY = 0.8
JUMP_STRENGTH = -16
PLAYER_SPEED = 5

MONKEY_HEIGHT = 70
MONKEY_COLOR = 'magenta'
# Game Balance
STARTING_ENERGY = 100
ENERGY_DRAIN_RATE = 0.02  # How fast energy drops per frame
FOOD_RECOVERY = 20        # Energy gained from food

HAZARD_SIZE = 40
HAZARD_COLOR = (255, 0, 0)      # Red
HAZARD_DAMAGE_RATE = 1.5        # How much energy is lost per frame of contact

# --- Platform Settings ---
PLATFORM_DEFAULT_HEIGHT = 20
PLATFORM_COLOR = (100, 100, 100)  # Gray

# --- Level Design ---
# Format: (x, y, width)
PLATFORM_LIST = [
    (100, 450, 200),  # Ledge 1: Low left
    (400, 320, 150),  # Ledge 2: Middle center
    (150, 200, 120),  # Ledge 3: High left
    (600, 400, 180)   # Ledge 4: Mid right
]

DIAMOND_POSITIONS = [(150, 160), (450, 280), (700, 500)]
HAZARD_POSITIONS = [(300, 420), (550, 380), (100, 250)]

# --- Food Placement Settings ---
# Format: (platform_index, offset_x)
# platform_index refers to the index in your PLATFORM_LIST
# offset_x is how far to the left (negative) or right (positive) of the ledge
LEDGE_FOOD_DATA = [
    (0, -40),  # To the left of the first ledge
    (0, 240),  # To the right of the first ledge
    (1, -30),  # To the left of the second ledge
    (2, 130)   # To the right of the high ledge
]

PLAYER_START_X = SCREEN_WIDTH // 2
PLAYER_START_Y = SCREEN_HEIGHT - MONKEY_HEIGHT 