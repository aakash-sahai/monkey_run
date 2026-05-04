import pygame
from settings import *

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((40, 40))
        self.image.fill(MONKEY_COLOR)

        # Use the constants from settings.py
        self.rect = self.image.get_rect(center=(PLAYER_START_X, PLAYER_START_Y))
        
        # Sync your float positions
        self.pos_x = float(self.rect.x)
        self.pos_y = float(self.rect.y)
        
        self.direction = pygame.math.Vector2(0, 0)
        
        # 1. ADD THIS: A shadow variable for precise Y position
        self.pos_x = float(self.rect.x)
        self.pos_y = float(self.rect.y) 
        
        self.direction = pygame.math.Vector2(0, 0)
        self.energy = STARTING_ENERGY
        self.diamonds = 0

    def apply_gravity(self):
        # 2. Add gravity to the direction
        self.direction.y += GRAVITY
        
        # 3. Add direction to the SHADOW variable (which allows decimals)
        self.pos_y += self.direction.y
        
        # 4. Update the Rect using the shadow variable
        self.rect.y = int(self.pos_y) 

        # Floor collision logic
        if self.rect.bottom >= SCREEN_HEIGHT - 50:
            self.rect.bottom = SCREEN_HEIGHT - 50
            self.pos_y = float(self.rect.y) # Reset shadow variable on floor
            self.direction.y = 0

    def update(self):
            #print("Heartbeat!") # If this doesn't show in the console, the method isn't running
            # 1. Capture the keys (Right, Left, Space)
            self.get_input()

            # 2. Horizontal Movement
            # We multiply direction (1, -1, or 0) by our speed constant
            self.pos_x += self.direction.x * PLAYER_SPEED
            self.rect.x = int(self.pos_x) # Apply the math to the visual box

            # --- Screen Constraints (Invisible Walls) ---
        # 1. Check the Left side
            if self.rect.left < 0:
                self.rect.left = 0
                self.pos_x = float(self.rect.x) # Reset the math to the wall

            # 2. Check the Right side
            if self.rect.right > SCREEN_WIDTH:
                self.rect.right = SCREEN_WIDTH
                self.pos_x = float(self.rect.x) # Reset the math to the wall

            if self.rect.top < 0:
                self.rect.top = 0
                self.direction.y = 0 # Stop the upward momentum
                self.pos_y = float(self.rect.y)

            # 3. Vertical Movement
            self.apply_gravity() # This handles gravity and the Y-position

            # 4. Energy Drain (The "Sustainability" Mechanic)
            self.energy -= ENERGY_DRAIN_RATE
            #print(f" Position:  ({self.rect.x}, {self.rect.y})") # Debugging: Check if X position changes when pressing arrows

    def get_input(self):
            self.direction.x = 0 # Reset horizontal direction each frame

            keys = pygame.key.get_pressed()
            if keys[pygame.K_RIGHT]:
                #print("Right Arrow Pressed!") # If this doesn't show in the console, the method isn't running
                self.direction.x = 1
            elif keys[pygame.K_LEFT]:
                self.direction.x = -1
            else:
                self.direction.x = 0

            # Vertical (Jump)
            # We add 'keys[pygame.K_UP]' or 'keys[pygame.K_w]' to the list
            if keys[pygame.K_SPACE] or keys[pygame.K_UP] or keys[pygame.K_w]:
                self.jump() 
            
            if keys[pygame.K_SPACE] and self.rect.bottom >= SCREEN_HEIGHT - 50:
                self.direction.y = JUMP_STRENGTH
    
    def jump(self):
        # Only allow jump if vertical movement is 0 (standing still)
        if self.direction.y == 0:
            self.direction.y = JUMP_STRENGTH 

class Food(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        # Create a small yellow square (or use a banana image!)
        self.image = pygame.Surface((20, 20))
        self.image.fill('yellow') 
        self.rect = self.image.get_rect(center=(x, y))

    def update(self):
        # Food doesn't move, but we can make it "bob" later!
        pass

class Diamond(pygame.sprite.Sprite): # Renamed from Reward
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((25, 25))
        self.image.fill('cyan') 
        self.rect = self.image.get_rect(center=(x, y))

class Hazard(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        # Use HAZARD_SIZE for the surface and the circle math
        self.image = pygame.Surface((HAZARD_SIZE, HAZARD_SIZE), pygame.SRCALPHA)
        
        # Draw the circle in the center of the surface
        center = HAZARD_SIZE // 2
        radius = HAZARD_SIZE // 2
        pygame.draw.circle(self.image, HAZARD_COLOR, (center, center), radius)
        
        self.rect = self.image.get_rect(center=(x, y))

from settings import *

class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, width):
        super().__init__()
        # Use constants for height and color
        self.image = pygame.Surface((width, PLATFORM_DEFAULT_HEIGHT))
        self.image.fill(PLATFORM_COLOR)
        
        # Position the ledge
        self.rect = self.image.get_rect(topleft=(x, y))
