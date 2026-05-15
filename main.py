from turtle import pos

# In order to run on terminal paste this command: source venv/bin/activate
# Then run: python3 main.py
import pygame
import sys
from settings import *
from entities import Diamond, Food, Hazard, Player, Platform

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

        # 1. Initialize Groups
        self.hazard_group = pygame.sprite.Group() 
        self.diamond_group = pygame.sprite.Group() 
        self.food_group = pygame.sprite.Group()
        self.platform_group = pygame.sprite.Group()
        self.player_group = pygame.sprite.GroupSingle()
        self.diamond_count = 0 
        print("2. Groups and Player initialized")

        # 2. Create the Player object
        self.monkey = Player() 
        self.player_group.add(self.monkey)

        # 3. THE MASTER LOOP
        for row_index, row in enumerate(LEVEL_MAP):
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
                elif cell == 'P':
                    self.monkey.rect.topleft = (x, y)
                    if hasattr(self.monkey, 'pos_y'):
                        self.monkey.pos_y = float(self.monkey.rect.y)
            print("3. Level Map loaded")

        # 4. Set up the Camera
        level_width = len(LEVEL_MAP[0]) * TILE_SIZE
        level_height = len(LEVEL_MAP) * TILE_SIZE
        self.camera = Camera(level_width, level_height)
        
        self.game_active = True
        print("4. Init finished successfully")

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
            

    def draw_hud(self):
        # 1. Create the text string
        score_text = f"Diamonds: {self.diamond_count}"
        
        # 2. Render the text into an image
        # (Text, Antialias, Color)
        score_surf = self.font.render(score_text, True, (255, 255, 255))
        
        # 3. Draw it on the screen at a specific position (top-left)
        self.screen.blit(score_surf, (20, 20))
        
        # Optional: Add Energy display here too!
        energy_text = f"Energy: {int(self.monkey.energy)}%"
        energy_surf = self.font.render(energy_text, True, (0, 255, 0))
        self.screen.blit(energy_surf, (20, 60))

    def display_game_over(self):
        # 1. Create the text
        msg = "Game Over! The monkey is too tired to continue."
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
                            self.__init__() 

                if self.game_active:
                    self.monkey.update() 
                    self.player_group.update()
                    self.camera.update(self.monkey) 
                    self.check_collisions()
            
                self.screen.fill((50, 50, 50)) 

                # Draw world
                for sprite in self.platform_group:
                    self.screen.blit(sprite.image, self.camera.apply(sprite))
                for sprite in self.food_group:
                    self.screen.blit(sprite.image, self.camera.apply(sprite))
                for sprite in self.diamond_group:
                    self.screen.blit(sprite.image, self.camera.apply(sprite))
                for sprite in self.hazard_group:
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