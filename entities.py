import pygame
import random
from settings import *

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        # 1. Create a transparent surface for the monkey's body parts to sit on
        self.image = pygame.Surface((40, 40), pygame.SRCALPHA)
        
        # Color Palette
        BROWN = (139, 69, 19)
        BEIGE = (222, 184, 135)
        BLACK = (0, 0, 0)

        # Draw Left Ear
        pygame.draw.circle(self.image, BROWN, (8, 15), 8)
        pygame.draw.circle(self.image, BEIGE, (8, 15), 4)
        
        # Draw Right Ear
        pygame.draw.circle(self.image, BROWN, (32, 15), 8)
        pygame.draw.circle(self.image, BEIGE, (32, 15), 4)

        # Draw Main Head
        pygame.draw.circle(self.image, BROWN, (20, 22), 15)

        # Draw Face/Muzzle (Beige overlay)
        pygame.draw.ellipse(self.image, BEIGE, (10, 16, 20, 16))

        # Draw Eyes
        pygame.draw.circle(self.image, BLACK, (16, 16), 2)
        pygame.draw.circle(self.image, BLACK, (24, 16), 2)

        # Physics and Precise Movement (Keep your original code here)
        self.rect = self.image.get_rect(topleft=(0, 0))
        self.direction = pygame.math.Vector2(0, 0)
        self.pos_x = float(self.rect.x)
        self.pos_y = float(self.rect.y) 
        
        # Stats
        self.energy = STARTING_ENERGY
        self.diamonds = 0

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
        self.water_ammo = 0          # Starts with 0 until they collect an item
        self.facing_direction = 1    # 1 = Right, -1 = Left

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
        
        # Horizontal Input (Combined Arrow keys + WASD cleanly)
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.direction.x = 1
            self.facing_direction = 1   # Facing Right
        elif keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.direction.x = -1
            self.facing_direction = -1  # Facing Left

        # Jump Input
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.jump()

    def jump(self):
        # Only jump if the monkey is standing on something (y direction is 0)
        if self.direction.y == 0:
            self.direction.y = JUMP_STRENGTH 

class Food(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        # 1. Create a transparent canvas slightly wider than a square
        self.image = pygame.Surface((30, 25), pygame.SRCALPHA)
        self.rect = self.image.get_rect(center=(x, y))
        
        # Color Palette
        YELLOW = (255, 223, 0)
        DARK_YELLOW = (204, 163, 0)
        BROWN = (101, 67, 33)
        
        # 2. Draw the outer curve (Dark Yellow background layer)
        pygame.draw.ellipse(self.image, DARK_YELLOW, (4, 4, 22, 16))
        
        # 3. Create the "bite" out of the circle to make it a crescent shape
        temp_surf = pygame.Surface((30, 25), pygame.SRCALPHA)
        pygame.draw.ellipse(temp_surf, YELLOW, (6, 2, 20, 14))
        
        # 4. Fill in the bright main yellow body
        pygame.draw.ellipse(self.image, YELLOW, (6, 5, 18, 12))
        
        # 5. Mask out the top to keep it looking like a neat crescent 
        pygame.draw.ellipse(self.image, (0, 0, 0, 0), (7, -2, 18, 12))
        
        # 6. Add the details (Brown stem at the left, brown tip at the right)
        # The Stem
        pygame.draw.line(self.image, BROWN, (4, 10), (7, 7), 3)
        # The Tip
        pygame.draw.circle(self.image, BROWN, (24, 11), 2)

class Diamond(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        # 1. Create a transparent surface for the diamond
        self.image = pygame.Surface((30, 30), pygame.SRCALPHA)
        self.rect = self.image.get_rect(center=(x, y))
        
        # Color Palette
        CYAN = (0, 238, 238)
        LIGHT_CYAN = (174, 238, 238)
        WHITE = (255, 255, 255)
        DARK_CYAN = (0, 139, 139)

        # 2. Define the outer diamond shape points (tapered jewel shape)
        # Coordinates are relative to our local 30x30 surface
        outer_points = [
            (7, 10),   # Top left
            (23, 10),  # Top right
            (15, 27),  # Bottom point
        ]
        
        # Base diamond structure
        pygame.draw.polygon(self.image, DARK_CYAN, outer_points)
        
        # 3. Draw the top "table" facet of the gem
        top_facet = [(7, 10), (23, 10), (19, 15), (11, 15)]
        pygame.draw.polygon(self.image, LIGHT_CYAN, top_facet)
        
        # 4. Draw the center facet lines to give it depth
        pygame.draw.polygon(self.image, CYAN, [(11, 15), (19, 15), (15, 27)])
        pygame.draw.polygon(self.image, DARK_CYAN, [(7, 10), (11, 15), (15, 27)])
        pygame.draw.polygon(self.image, CYAN, [(23, 10), (19, 15), (15, 27)])

        # 5. Add a tiny white sparkle highlight on the top left
        pygame.draw.line(self.image, WHITE, (9, 12), (13, 12), 2)
        pygame.draw.line(self.image, WHITE, (11, 10), (11, 14), 2)

class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, width):
        super().__init__()
        self.image = pygame.Surface((width, PLATFORM_DEFAULT_HEIGHT))
        self.image.fill(PLATFORM_COLOR)
        self.rect = self.image.get_rect(topleft=(x, y))

# --- Fire Effect Helper Class ---
class FireParticle:
    def __init__(self, x, y):
        self.x = x + random.randint(-10, 10)  # Randomize spawn width
        self.y = y + random.randint(-5, 5)
        self.radius = random.randint(8, 14)
        self.speed_y = random.uniform(-3, -1) # Move upwards
        self.speed_x = random.uniform(-1, 1)  # Drifts slightly sideways
        # Start bright yellow/orange, fade to deep red
        self.color = [255, random.randint(150, 220), 0] 

    def update(self):
        self.x += self.speed_x
        self.y += self.speed_y
        self.radius -= 0.3  # Shrink as it rises
        self.color[1] = max(0, self.color[1] - 4)  # Turn redder
        self.color[0] = max(0, self.color[0] - 2)  # Fade out slow

    def draw(self, surface):
        if self.radius > 0:
            pygame.draw.circle(surface, self.color, (int(self.x), int(self.y)), int(self.radius))

# --- Hazard Class ---
class Hazard(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        # 1. Create a generous bounding box so the fire has room to breathe
        self.width = HAZARD_SIZE * 2
        self.height = HAZARD_SIZE * 3
        self.image = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        
        # 2. Position the rect so its bottom-center rests on the spawn point (x, y)
        self.rect = self.image.get_rect(midbottom=(x, y))
        
        # 3. Spawn point for particles, relative to the bottom center of the local image
        self.spawn_x = self.width // 2
        self.spawn_y = self.height - (HAZARD_SIZE // 2)
        
        self.particles = []

    def update(self):
        # 1. Spawn particles locally relative to the sprite's own center
        if len(self.particles) < 30:  
            # We spawn them at (0, 0) relative to the emitter point, then let them drift
            self.particles.append(FireParticle(self.spawn_x, self.spawn_y))

        # 2. Clear the surface so it stays transparent
        self.image.fill((0, 0, 0, 0))

        # 3. Update and draw particles directly onto the image
        for p in self.particles[:]:
            p.update()
            
            # If particle dies or shrinks too much, remove it
            if p.radius <= 0 or p.color[0] <= 10:
                self.particles.remove(p)
            else:
                # Ensure we only draw if it falls within the boundaries of our surface
                if 0 <= p.x < self.width and 0 <= p.y < self.height:
                    pygame.draw.circle(self.image, p.color, (int(p.x), int(p.y)), int(p.radius))

class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, width):
        super().__init__()
        self.image = pygame.Surface((width, PLATFORM_DEFAULT_HEIGHT), pygame.SRCALPHA)
        self.rect = self.image.get_rect(topleft=(x, y))
        
        # Color Palette for a Volcanic Burning Jungle
        CHARCOAL = (35, 30, 30)       # Dark, burnt soil/rock
        DARK_BROWN = (70, 40, 20)     # Mud/earth layer
        LAVA_ORANGE = (255, 69, 0)    # Glowing magma vein
        MAGMA_YELLOW = (255, 140, 0)  # Core heat line

        # 1. Fill the base with dark burnt earth
        self.image.fill(DARK_BROWN)
        
        # 2. Add jagged charcoal rock layers across the bottom half
        # We loop across the width in steps of 10 pixels to make it look uneven
        for i in range(0, width, 10):
            rock_height = random.randint(8, 15)
            pygame.draw.rect(
                self.image, 
                CHARCOAL, 
                (i, PLATFORM_DEFAULT_HEIGHT - rock_height, 10, rock_height)
            )

        # 3. Draw a glowing lava/magma crust across the top edge
        # Top lava line (base orange)
        pygame.draw.rect(self.image, LAVA_ORANGE, (0, 0, width, 4))
        
        # 4. Add dynamic, flickering heat cracks along the surface
        for i in range(0, width, 15):
            # Glowing hot spots
            if random.random() < 0.6:
                crack_width = random.randint(5, 12)
                # Bright yellow core cracks
                pygame.draw.rect(self.image, MAGMA_YELLOW, (i, 0, crack_width, 2))
                # Small drips of orange lava leaking downward into the dirt
                drip_height = random.randint(3, 8)
                pygame.draw.line(self.image, LAVA_ORANGE, (i, 0), (i + random.randint(-2, 2), drip_height), 2)

class WaterDroplet(pygame.sprite.Sprite):
    def __init__(self, x, y, direction_x):
        super().__init__()
        # Create a small transparent canvas for the droplet
        self.image = pygame.Surface((16, 10), pygame.SRCALPHA)
        self.rect = self.image.get_rect(center=(x, y))
        
        # Draw a blue droplet shape
        pygame.draw.ellipse(self.image, (0, 191, 255), (0, 0, 16, 10)) # Deep Sky Blue
        pygame.draw.ellipse(self.image, (240, 248, 255), (4, 2, 8, 6)) # Light core highlight
        
        # Set movement speed and direction (-1 for left, 1 for right)
        self.speed_x = direction_x * WATER_SPEED
        
        # Track spawn position to kill it if it flies too far without hitting anything
        self.spawn_x = x

    def update(self):
        # Move the droplet horizontally
        self.rect.x += self.speed_x
        
        # If the droplet travels more than 600 pixels away from where it started, delete it
        if abs(self.rect.x - self.spawn_x) > 600:
            self.kill()

class WaterGunItem(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((32, 24), pygame.SRCALPHA)
        
        self.rect = self.image.get_rect(midbottom=(x + TILE_SIZE // 2, y + TILE_SIZE))
        
        # Draw a quick vector water gun (bright neon blue/plastic look)
        pygame.draw.rect(self.image, (0, 255, 255), (8, 4, 20, 10))  # Barrel
        pygame.draw.rect(self.image, (0, 200, 255), (6, 10, 6, 12))  # Handle
        pygame.draw.rect(self.image, (255, 69, 0), (20, 0, 6, 4))    # Bright orange water tank cap

class Fireball(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        # 2. FIX: Make the fireball much bigger (32x32 pixels instead of 16)
        self.image = pygame.Surface((32, 32), pygame.SRCALPHA)
        
        # Give the fireball a detailed appearance (bright core, fiery outer ring)
        pygame.draw.circle(self.image, (255, 69, 0), (16, 16), 16) # Outer dark orange
        pygame.draw.circle(self.image, (255, 140, 0), (16, 16), 11) # Inner light orange
        pygame.draw.circle(self.image, (255, 255, 0), (16, 16), 5)  # Bright yellow core
        
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = -7 # Traveling left
        
        # 3. FIX: Track distance traveled to limit its range
        self.distance_traveled = 0
        self.max_range = 450 # Max pixels it can fly before despawning

    def update(self):
        self.rect.x += self.speed
        self.distance_traveled += abs(self.speed)
        
        # Despawn if it goes past its maximum range, or hits the edge of screen
        if self.distance_traveled >= self.max_range or self.rect.right < 0:
            self.kill()

class Golem(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        # 1. FIX: Make the Golem detailed using layered rects and shapes
        self.image = pygame.Surface((50, 70), pygame.SRCALPHA)
        
        # Draw Golem Body/Torso (Stone Grey)
        pygame.draw.rect(self.image, (100, 100, 100), (5, 20, 40, 50))
        # Draw Shoulder Plates (Darker Accent Grey)
        pygame.draw.rect(self.image, (70, 70, 70), (0, 15, 50, 15))
        # Draw Head
        pygame.draw.rect(self.image, (110, 110, 110), (12, 0, 26, 20))
        # Draw Glowing Fire Eyes (Red/Yellow)
        pygame.draw.rect(self.image, (255, 0, 0), (16, 5, 6, 4))
        pygame.draw.rect(self.image, (255, 0, 0), (28, 5, 6, 4))
        # Draw Cracks/Markings on the Stone Body
        pygame.draw.line(self.image, (40, 40, 40), (15, 30), (25, 45), 2)
        pygame.draw.line(self.image, (255, 69, 0), (25, 45), (35, 40), 2) # Glowing magma crack
        
        self.rect = self.image.get_rect(topleft=(x, y))
        
        # Shooting timer mechanics
        self.shoot_cooldown = 90 
        self.timer = random.randint(0, 40) 

    def update(self, fireball_group):
        self.timer += 1
        if self.timer >= self.shoot_cooldown:
            self.timer = 0
            # Spawn fireball from the left side of the Golem's chest
            new_fireball = Fireball(self.rect.left, self.rect.centery)
            fireball_group.add(new_fireball)