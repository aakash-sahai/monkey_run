import pygame
from settings import *

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        # Monkey Appearance
        self.image = pygame.Surface((40, 40))
        self.image.fill(MONKEY_COLOR)

        # 1. Start at 0,0. Your Master Loop in main.py will move 
        # this to the 'P' position immediately.
        self.rect = self.image.get_rect(topleft=(0, 0))
        
        # Physics and Precise Movement
        self.direction = pygame.math.Vector2(0, 0)
        self.pos_x = float(self.rect.x)
        self.pos_y = float(self.rect.y) 
        
        # Stats
        self.energy = STARTING_ENERGY
        self.diamonds = 0

    def apply_gravity(self):
        # Adds gravity to vertical direction
        self.direction.y += GRAVITY
        self.pos_y += self.direction.y
        self.rect.y = int(self.pos_y) 

    def update(self):
        self.get_input()

        # Horizontal Movement
        self.pos_x += self.direction.x * PLAYER_SPEED
        self.rect.x = int(self.pos_x) 

        # --- Level Constraints ---
        # Stop the monkey from going back past the start of the level
        if self.rect.left < 0:
            self.rect.left = 0
            self.pos_x = float(self.rect.x)

        # We allow the monkey to go as far Right as they want now!
        
        # Stop the monkey from flying off the top of the screen
        if self.rect.top < 0:
            self.rect.top = 0
            self.direction.y = 0 
            self.pos_y = float(self.rect.y)

        # Apply Physics
        self.apply_gravity()

        # Constant Energy Drain
        self.energy -= ENERGY_DRAIN_RATE

    def get_input(self):
        self.direction.x = 0 
        keys = pygame.key.get_pressed()
        
        # Horizontal Input
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.direction.x = 1
        elif keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.direction.x = -1

        # Jump Input
        if keys[pygame.K_SPACE] or keys[pygame.K_UP] or keys[pygame.K_w]:
            self.jump() 
    
    def jump(self):
        # Only jump if the monkey is standing on something (y direction is 0)
        if self.direction.y == 0:
            self.direction.y = JUMP_STRENGTH 

class Food(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((20, 20))
        self.image.fill('yellow') 
        self.rect = self.image.get_rect(center=(x, y))

class Diamond(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((25, 25))
        self.image.fill('cyan') 
        self.rect = self.image.get_rect(center=(x, y))

class Hazard(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((HAZARD_SIZE, HAZARD_SIZE), pygame.SRCALPHA)
        
        center = HAZARD_SIZE // 2
        radius = HAZARD_SIZE // 2
        pygame.draw.circle(self.image, HAZARD_COLOR, (center, center), radius)
        
        self.rect = self.image.get_rect(center=(x, y))

class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, width):
        super().__init__()
        self.image = pygame.Surface((width, PLATFORM_DEFAULT_HEIGHT))
        self.image.fill(PLATFORM_COLOR)
        self.rect = self.image.get_rect(topleft=(x, y))