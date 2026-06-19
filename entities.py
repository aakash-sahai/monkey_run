# entities.py
import pygame
import random
from settings import SCREEN_WIDTH, SCREEN_HEIGHT, BLACK, DARK_GRAY, WHITE

class Button:
    def __init__(self, x, y, width, height, text, base_color, hover_color, callback):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.base_color = base_color
        self.hover_color = hover_color
        self.callback = callback
        self.font = pygame.font.Font(None, 36)

    def draw(self, surface):
        mouse_pos = pygame.mouse.get_pos()
        color = self.hover_color if self.rect.collidepoint(mouse_pos) else self.base_color
        
        pygame.draw.rect(surface, color, self.rect, border_radius=12)
        
        text_surf = self.font.render(self.text, True, BLACK)
        text_rect = text_surf.get_rect(center=self.rect.center)
        surface.blit(text_surf, text_rect)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                self.callback()


class GlitchedBackground:
    def __init__(self, fps):
        self.fps = fps
        self.base_surf = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        
        # Binary stream setup
        self.font = pygame.font.Font(None, 24)
        self.binary_streams = []
        for _ in range(18): # Increased density
            self.binary_streams.append({
                'x': random.randint(10, SCREEN_WIDTH - 20),
                'y': random.randint(-100, SCREEN_HEIGHT),
                'speed': random.randint(4, 12),
                'text': ''.join(random.choice(['0', '1', 'X', 'ERROR', '?', 'SYSTEM']) for _ in range(10))
            })

    def draw_glitched_geometry(self, surface):
        """Draws chaotic glitch rectangles and horizontal color bars"""
        num_shapes = random.randint(8, 15)
        for _ in range(num_shapes):
            # Random glitch neon colors (greens, cyans, magentas, reds)
            glitch_color = random.choice([
                (0, random.randint(100, 255), 0, random.randint(20, 70)),      # Neon Green
                (0, random.randint(100, 255), random.randint(100, 255), random.randint(20, 70)), # Cyan
                (random.randint(100, 255), 0, random.randint(100, 255), random.randint(20, 70)), # Magenta
                (random.randint(150, 255), random.randint(0, 50), 0, random.randint(30, 80))     # Bright Red
            ])
            
            # Draw thin horizontal malicious-looking bars
            w = random.choice([random.randint(50, 300), SCREEN_WIDTH])
            h = random.randint(2, 20)
            r_surf = pygame.Surface((w, h), pygame.SRCALPHA)
            r_surf.fill(glitch_color)
            surface.blit(r_surf, (random.randint(-50, SCREEN_WIDTH), random.randint(0, SCREEN_HEIGHT)))

    def update(self):
        for stream in self.binary_streams:
            stream['y'] += stream['speed']
            if stream['y'] > SCREEN_HEIGHT:
                stream['y'] = random.randint(-200, -10)
                stream['x'] = random.randint(10, SCREEN_WIDTH - 20)
                stream['text'] = ''.join(random.choice(['0', '1', '!', 'FAIL', 'Ø']) for _ in range(12))

    def draw(self, surface):
        # 1. Start with solid canvas base
        self.base_surf.fill(BLACK)
        
        # 2. Draw our glitch blocks and digital bars
        self.draw_glitched_geometry(self.base_surf)

        # 3. Draw falling corrupted text matrix
        for stream in self.binary_streams:
            txt_surf = self.font.render(stream['text'], True, (0, random.randint(80, 180), 0))
            txt_surf.set_alpha(180) 
            self.base_surf.blit(txt_surf, (stream['x'], stream['y']))

        # 4. Generate random White-Noise Static Blocks (Corrupted memory blocks)
        if random.random() < 0.4: # 40% chance per frame
            for _ in range(random.randint(2, 5)):
                nx = random.randint(0, SCREEN_WIDTH - 50)
                ny = random.randint(0, SCREEN_HEIGHT - 50)
                nw = random.randint(10, 80)
                nh = random.randint(10, 40)
                # Fill block with pure random salt-and-pepper pixels
                for _ in range(15): 
                    pygame.draw.rect(self.base_surf, WHITE, (nx + random.randint(0, nw), ny + random.randint(0, nh), 2, 2))

        # 5. Apply brutal slice offsets (Chromatic horizontal shifting)
        temp_screen = self.base_surf.copy()
        glitch_lines = random.randint(8, 20) # Heavily increased line count
        for _ in range(glitch_lines):
            line_y = random.randint(0, SCREEN_HEIGHT - 30)
            line_h = random.randint(2, 25)
            line_offset = random.randint(-25, 25) # Wild displacement jump
            
            line_rect = pygame.Rect(0, line_y, SCREEN_WIDTH, line_h)
            line_surf = temp_screen.subsurface(line_rect).copy()
            self.base_surf.blit(line_surf, (line_offset, line_y))

        # 6. Screen Jitter / Shake (Move the entire background randomly)
        shake_x = random.randint(-6, 6) if random.random() < 0.15 else 0
        shake_y = random.randint(-4, 4) if random.random() < 0.15 else 0
        
        # Final pass blit to the real game window with shake offset
        surface.blit(self.base_surf, (shake_x, shake_y))

        # 7. Heavy CRT Scanlines
        for y in range(0, SCREEN_HEIGHT, 3): # Thicker, closer scanlines
            pygame.draw.line(surface, (0, 0, 0, 150), (0, y), (SCREEN_WIDTH, y), 1)
