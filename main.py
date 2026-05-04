from turtle import pos

import pygame
import sys
from settings import *
from entities import Diamond, Food, Hazard, Player, Platform

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Monkey Run: The Long Migration")
        self.clock = pygame.time.Clock()

        pygame.font.init() # Initialize the font engine
        self.font = pygame.font.SysFont('Arial', 30, bold=True)

        self.hazard_group = pygame.sprite.Group() 

        self.diamond_group = pygame.sprite.Group() 
        self.diamond_count = 0 

        # Build Diamonds
        for pos in DIAMOND_POSITIONS:
            self.diamond_group.add(Diamond(pos[0], pos[1]))

        # Build Hazards
        for pos in HAZARD_POSITIONS:
            self.hazard_group.add(Hazard(pos[0], pos[1]))

        # Create the Player object
        self.monkey = Player() 

        # 2. Create an empty GroupSingle
        self.player_group = pygame.sprite.GroupSingle()

        # 3. Add the player to the group
        self.player_group.add(self.monkey)
        self.food_group = pygame.sprite.Group()
        
       
        for data in LEDGE_FOOD_DATA:
            plat_index = data[0]
            offset_x = data[1]
            
            # Get the platform from our list
            # PLATFORM_LIST[plat_index] = (x, y, width)
            target_plat = PLATFORM_LIST[plat_index]
            
            # Calculate food position
            # x = platform_x + offset
            # y = platform_y (roughly the same height)
            food_x = target_plat[0] + offset_x
            food_y = target_plat[1] 
            
            # Add to group
            self.food_group.add(Food(food_x, food_y))


        self.platform_group = pygame.sprite.Group()

        # Loop through the list in settings and create each platform
        for plat_data in PLATFORM_LIST:
            # plat_data[0] is x, [1] is y, [2] is width
            new_plat = Platform(plat_data[0], plat_data[1], plat_data[2])
            self.platform_group.add(new_plat)

    def check_collisions(self):
        # 1. Check if monkey hits anything in the food group
        # The 'True' means the food disappears (kill) when touched
        food_hit = pygame.sprite.spritecollide(self.player_group.sprite, self.food_group, False)

        if food_hit:
            print("Yum!")
            self.monkey.energy += 20 # Boost energy!
            if self.monkey.energy > 100:
                self.monkey.energy = 100 # Cap it at 100

        diamonds_hit = pygame.sprite.spritecollide(self.player_group.sprite, self.diamond_group, False)
        for diamond in diamonds_hit:
            print("Yay!")
            self.diamond_count += 1

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

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            self.screen.fill((50, 50, 50)) # Background
            
            # 2. UPDATE EVERYTHING <--- Check for this!
            self.monkey.update() # Update the player (handles input, movement, energy)
            self.player_group.update()
            self.check_collisions()
            #print("Running the loop...")
            
            # Draw
            self.screen.fill((50, 50, 50))

            # Draw the platforms BEFORE the player (so they are in the background)
            self.platform_group.draw(self.screen)

            self.player_group.draw(self.screen)
            self.food_group.draw(self.screen) # Draw food next
            self.diamond_group.draw(self.screen) # Draw diamonds next
            self.hazard_group.draw(self.screen) # Draw hazards!
            

            # Draw HUD last so it's always visible!
            self.draw_hud()

            pygame.display.update()
            self.clock.tick(FPS)

if __name__ == "__main__":
    print ("Main")
    game = Game()
    game.run()