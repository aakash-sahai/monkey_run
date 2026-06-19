from turtle import pos

# In order to run on terminal paste this command: source venv/bin/activate
# Then run: python3 main.py
import pygame
import sys
from settings import *
from entities import Diamond, Food, Hazard, Player, Platform, WaterGunItem, Golem

class Camera:
    def __init__(self, width, height):
        self.camera = pygame.Rect(0, 0, width, height)
        self.width = width
        self.height = height

    def apply(self, entity):
        # This shifts the sprite's position on screen based on camera movement
        return entity.rect.move(self.camera.topleft)

    def update(self, target):
        # Centers the camera on the monkey
        x = -target.rect.centerx + int(SCREEN_WIDTH / 2)
        y = -target.rect.centery + int(SCREEN_HEIGHT / 2)
        
        # Stops the camera at the edges of the map
        x = min(0, x)
        y = min(0, y)
        x = max(-(self.width - SCREEN_WIDTH), x)
        y = max(-(self.height - SCREEN_HEIGHT), y)
        self.camera = pygame.Rect(x, y, self.width, self.height)

class Game:
    def __init__(self):
        print("1. Init started")
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Monkey Run: The Long Migration")
        self.clock = pygame.time.Clock()

        pygame.font.init() 
        self.font = pygame.font.SysFont('Arial', 30, bold=True)

        # Track the active level index (0 = Level 1, 1 = Level 2)
        self.current_level = 0
        self.diamond_count = 0 
        self.game_active = True
        self.game_over_reason = ""

        # Initialize Groups
        self.hazard_group = pygame.sprite.Group() 
        self.diamond_group = pygame.sprite.Group() 
        self.food_group = pygame.sprite.Group()
        self.platform_group = pygame.sprite.Group()
        self.player_group = pygame.sprite.GroupSingle()
        self.water_group = pygame.sprite.Group()
        self.water_gun_group = pygame.sprite.Group()
        self.golem_group = pygame.sprite.Group()
        self.fireball_group = pygame.sprite.Group()

        # Create the Player object
        self.monkey = Player() 
        self.player_group.add(self.monkey)

        # Load the first level map layout
        self.load_level()
        print("4. Init finished successfully")

    def load_level(self):
        # Clear out all old sprites from the previous level
        self.hazard_group.empty()
        self.diamond_group.empty()
        self.food_group.empty()
        self.platform_group.empty()
        self.water_group.empty()
        self.water_gun_group.empty()
        self.golem_group.empty()      
        self.fireball_group.empty()

        # Grab the specific map structure from our settings list
        current_map_layout = LEVEL_MAPS[self.current_level]

        # THE MASTER LOOP (Modified to read our new current_map_layout)
        for row_index, row in enumerate(current_map_layout):
            for col_index, cell in enumerate(row):
                x = col_index * TILE_SIZE
                y = row_index * TILE_SIZE
            
                if cell == 'X':
                    self.platform_group.add(Platform(x, y, TILE_SIZE))
                elif cell == 'H':
                    self.hazard_group.add(Hazard(x, y))
                elif cell == 'D':
                    self.diamond_group.add(Diamond(x, y))
                elif cell == 'F':
                    self.food_group.add(Food(x, y))
                elif cell == 'W':
                    print(f"SPAWNING WATER GUN AT: {x}, {y}") 
                    self.water_gun_group.add(WaterGunItem(x, y))
                elif cell == 'G':
                    print(f"SPAWNING GOLEM AT: {x}, {y}")
                    self.golem_group.add(Golem(x, y - 6)) 
                elif cell == 'P':
                    self.monkey.rect.topleft = (x, y)
                    self.monkey.direction.y = 0  
                    if hasattr(self.monkey, 'pos_x'):
                        self.monkey.pos_x = float(self.monkey.rect.x)
                    if hasattr(self.monkey, 'pos_y'):
                        self.monkey.pos_y = float(self.monkey.rect.y)

        # Set up or recalculate the Camera boundaries for this level size
        level_width = len(current_map_layout[0]) * TILE_SIZE
        level_height = len(current_map_layout) * TILE_SIZE
        self.camera = Camera(level_width, level_height)
        
        # Reset monkey stats for the new level
        self.monkey.energy = 100       
        self.water_group.empty()       
        self.game_active = True
        print(f"4. Level {self.current_level + 1} loaded successfully")

    def check_collisions(self):
        # 1. Check if monkey hits anything in the food group
        # The 'True' means the food disappears (kill) when touched
        food_hit = pygame.sprite.spritecollide(self.player_group.sprite, self.food_group, False)
        for food in food_hit:
            food.kill() # Remove the food from the game

        if food_hit:
            print("Yum!")
            self.monkey.energy += 20 # Boost energy!
            if self.monkey.energy > 100:
                self.monkey.energy = 100 # Cap it at 100

        diamonds_hit = pygame.sprite.spritecollide(self.player_group.sprite, self.diamond_group, False)
        for diamond in diamonds_hit:
            print("Yay!")
            self.diamond_count += 1
            diamond.kill() # Remove the diamond from the game

        if self.monkey.energy <= 0:
            self.monkey.energy = 0
            self.game_active = False

        # --- Water Gun Item Pickup ---
        gun_hit = pygame.sprite.spritecollide(self.player_group.sprite, self.water_gun_group, True)
        if gun_hit:
            print("Water gun equipped! 3 shots loaded.")
            self.monkey.water_ammo += 3  # Add 3 shots per item collected

        # --- Water Droplet Extinguishing Fire Hazards ---
        # True, True means BOTH the water droplet and the fire hazard will get deleted on contact!
        extinguish_hits = pygame.sprite.groupcollide(self.water_group, self.hazard_group, True, True)
        if extinguish_hits:
            print("Sizzle! Fire extinguished!")

# --- Hazard Collision ---
        if pygame.sprite.spritecollide(self.player_group.sprite, self.hazard_group, False):
            print("Ouch!")
            self.monkey.energy -= HAZARD_DAMAGE_RATE
            
            # Keep energy from going below zero
            if self.monkey.energy < 0:
                self.monkey.energy = 0

    # --- Platform Collision (The Floor) ---
        # 1. Check if the player sprite overlaps with any platform
        hits = pygame.sprite.spritecollide(self.player_group.sprite, self.platform_group, False)
        
        if hits:
            #  moving DOWN (falling)
            if self.monkey.direction.y > 0:
                print("Nailed it!")              
                # Snap the monkey's bottom to the platform's top
                self.monkey.rect.bottom = hits[0].rect.top
                
                # 3. Reset physics so he stops falling
                self.monkey.direction.y = 0
                
                # 4. CRITICAL: Sync the internal float position with the rect
                self.monkey.pos_y = float(self.monkey.rect.y)     

            # 2. BUMPING HEAD (Moving Up)
            elif self.monkey.direction.y < 0:
                print("Boink!") 
                # Snap monkey's top to platform's bottom
                self.monkey.rect.top = hits[0].rect.bottom
                # Stop upward momentum (starts falling immediately)
                self.monkey.direction.y = 0
                self.monkey.pos_y = float(self.monkey.rect.y) 
        if pygame.sprite.spritecollide(self.player_group.sprite, self.fireball_group, True):
            print("Ouch! Hit by a fireball!")
            self.monkey.energy -= 15  # Take damage from fireballs

        # --- Water Droplet vs Fireball (Water puts out fire) ---
        pygame.sprite.groupcollide(self.water_group, self.fireball_group, True, True)
        
        # --- Check for Level Completion ---
        # Calculate where the map ends horizontally
        current_map_layout = LEVEL_MAPS[self.current_level]
        level_right_edge = len(current_map_layout[0]) * TILE_SIZE

        if self.monkey.rect.right >= level_right_edge:
            # Check if there is a next level BEFORE changing the counter
            if self.current_level + 1 < len(LEVEL_MAPS):
                self.current_level += 1
                print(f"Heading into Level {self.current_level + 1}!")
                self.load_level()
            else:
                print("Victory! You completed the migration!")
                self.game_active = False
        
        # --- Check if Monkey Fell Off the Screen ---
        # If the top of the monkey goes past the screen height, they fall into the abyss
        if self.monkey.rect.top > SCREEN_HEIGHT:
            self.game_over_reason = "fall"
            self.game_active = False

        # --- Update existing energy death check to track the reason ---
        if self.monkey.energy <= 0:
            self.monkey.energy = 0
            self.game_over_reason = "energy" # Track that they ran out of energy
            self.game_active = False

    def draw_background(self):
        top_color = (25, 20, 20)      # Dark ash charcoal
        bottom_color = (70, 15, 5)    # Deep, smoky fire glow
        
        for y in range(SCREEN_HEIGHT):
            t = y / SCREEN_HEIGHT
            r = int(top_color[0] + (bottom_color[0] - top_color[0]) * t)
            g = int(top_color[1] + (bottom_color[1] - top_color[1]) * t)
            b = int(top_color[2] + (bottom_color[2] - top_color[2]) * t)
            pygame.draw.line(self.screen, (r, g, b), (0, y), (SCREEN_WIDTH, y))

    def draw_trees(self):
        # We use a fixed seed based on positions so the trees don't randomly 
        # shuffle around every frame, but stay fixed to the game world.
        import random
        random.seed(42) # Keeps the forest layout identical every frame

        # Color Palette for burnt tree silhouettes
        CHARCOAL = (20, 15, 15)
        EMBER_RED = (90, 25, 10)

        # Draw 15 trees spaced out across the level
        # We account for the camera movement so they scroll naturally!
        for i in range(15):
            # Space trees out across the map width
            base_x = i * 250 + random.randint(-50, 50)
            # Apply the camera offset horizontally so they move with the world
            tree_x = base_x + self.camera.camera.x
            
            # Keep them anchored near the bottom half of the screen
            tree_y = SCREEN_HEIGHT - 120 + random.randint(-20, 20)
            tree_height = random.randint(80, 140)

            # Only draw if the tree is actually visible on the screen
            if -60 < tree_x < SCREEN_WIDTH + 60:
                # 1. Draw the Main Trunk
                pygame.draw.rect(self.screen, CHARCOAL, (tree_x, tree_y - tree_height, 12, tree_height))
                
                # 2. Draw a faint glowing orange outline on one side (heat reflection)
                pygame.draw.line(self.screen, EMBER_RED, (tree_x + 12, tree_y - tree_height), (tree_x + 12, tree_y), 2)

                # 3. Draw Jagged Branch Layers (Pine/Burnt Jungle style spikes)
                current_y = tree_y - tree_height
                branch_width = 20
                while current_y < tree_y - 20:
                    # Draw a triangle for the branches pointing upward/outward
                    points = [
                        (tree_x + 6, current_y - 15), # Top point
                        (tree_x - branch_width, current_y + 15), # Bottom left
                        (tree_x + 6 + branch_width, current_y + 15) # Bottom right
                    ]
                    pygame.draw.polygon(self.screen, CHARCOAL, points)
                    
                    current_y += 20
                    branch_width += 6 # Branches get wider near the bottom

        # Reset the random seed so it doesn't break your fire hazard particles!
        random.seed()

    def draw_hud(self):
        # 1. Create the text string
        score_text = f"Diamonds: {self.diamond_count}"
        
        # 2. Render the text into an image
        # (Text, Antialias, Color)
        score_surf = self.font.render(score_text, True, (255, 255, 255))
        
        # 3. Draw it on the screen at a specific position (top-left)
        self.screen.blit(score_surf, (20, 20))
        
        # Energy display
        energy_text = f"Energy: {int(self.monkey.energy)}%"
        energy_surf = self.font.render(energy_text, True, (0, 255, 0))
        self.screen.blit(energy_surf, (20, 60))

        water_text = f"Water Ammo: {self.monkey.water_ammo}"
        water_surf = self.font.render(water_text, True, (0, 191, 255))
        self.screen.blit(water_surf, (20, 100))

    def display_game_over(self):
        # 1. Determine the message based on how the player lost
        if self.game_over_reason == "fall":
            msg = "Oops! The monkey fell out of the burning forest!"
        elif self.game_over_reason == "energy":
            msg = "Game Over! The monkey is too tired to continue."
        else:
            msg = "Game Over!" # Fallback default
            
        restart_msg = "Press 'R' to try again"
        
        # 2. Render it
        surf = self.font.render(msg, True, (255, 0, 0))
        restart_surf = self.font.render(restart_msg, True, (255, 255, 255))
        
        # 3. Center it on the screen
        rect = surf.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        restart_rect = restart_surf.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50))
        
        # 4. Draw a dark overlay to make it look "frozen"
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(128) # Semi-transparent
        overlay.fill((0, 0, 0))
        self.screen.blit(overlay, (0,0))
        
        # 5. Draw the text boxes
        self.screen.blit(surf, rect)
        self.screen.blit(restart_surf, restart_rect)

    def run(self):
            print("5. Run loop entered")
            while True:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                
                    # Restart logic
                    if not self.game_active and event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_r:
                            # Re-initialize the whole game object to reset back to Level 1
                            self.__init__()

                    # Check for shooting action
                    if self.game_active and event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_SPACE:
                            if self.monkey.water_ammo > 0:
                                # Spawn a water droplet at the monkey's center position
                                from entities import WaterDroplet
                                droplet = WaterDroplet(self.monkey.rect.centerx, self.monkey.rect.centery, self.monkey.facing_direction)
                                self.water_group.add(droplet)
                                
                                # Deduct one shot
                                self.monkey.water_ammo -= 1

                if self.game_active:
                    self.monkey.update() 
                    self.player_group.update()
                    self.hazard_group.update()
                    self.water_group.update()
                    self.golem_group.update(self.fireball_group) 
                    self.fireball_group.update()
                    self.camera.update(self.monkey) 
                    self.check_collisions()

                self.draw_background()

                self.draw_trees()

                # Draw world
                for sprite in self.platform_group:
                    self.screen.blit(sprite.image, self.camera.apply(sprite))
                for sprite in self.food_group:
                    self.screen.blit(sprite.image, self.camera.apply(sprite))
                for sprite in self.diamond_group:
                    self.screen.blit(sprite.image, self.camera.apply(sprite))
                for sprite in self.hazard_group:
                    self.screen.blit(sprite.image, self.camera.apply(sprite))

                for sprite in self.golem_group:                  
                    self.screen.blit(sprite.image, self.camera.apply(sprite))
                for sprite in self.fireball_group:               
                    self.screen.blit(sprite.image, self.camera.apply(sprite))

                for sprite in self.water_gun_group:
                    self.screen.blit(sprite.image, self.camera.apply(sprite))
                for sprite in self.water_group:
                    self.screen.blit(sprite.image, self.camera.apply(sprite))

                self.screen.blit(self.monkey.image, self.camera.apply(self.monkey))
                self.draw_hud()

                # Game Over Overlay
                if not self.game_active:
                    self.display_game_over()

                pygame.display.update()
                self.clock.tick(60)

if __name__ == "__main__":
    print ("Main")
    game = Game()
    game.run()
