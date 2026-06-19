# main.py
import pygame
import sys
import random
import copy
from settings import *
from entities import Button, GlitchedBackground

class GameController:
    def __init__(self):
        pygame.init()
        pygame.font.init()
        
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Genre Shifter")
        self.clock = pygame.time.Clock()
        
        self.state = 'START_MENU'
        self.selected_map = None
        self.difficulty = "easy"
        
        self.lvl2_unlocked = False
        self.lvl3_unlocked = False
        
        self.setup_menus()
        self.reset_uttc()
        self.glitched_bkg = GlitchedBackground(FPS)

    def reset_uttc(self):
        self.current_symbol = "X" 
        self.active_board = None  
        self.mini_boards = [[[[None for _ in range(3)] for _ in range(3)] for _ in range(3)] for _ in range(3)]
        self.big_board = [[None for _ in range(3)] for _ in range(3)]
        self.game_winner = None

    def setup_menus(self):
        self.start_button = Button(
            SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 25, 200, 50,
            "START GAME", GREEN, BRIGHT_GREEN, lambda: self.change_state('MAP_SELECT')
        )
        
        self.map_buttons = []
        for i in range(1, 7):
            row, col = (i - 1) // 3, (i - 1) % 3
            x, y = 100 + (col * 200), 250 + (row * 150)
            if i == 1:
                btn = Button(x, y, 150, 80, f"Map {i}", GREEN, BRIGHT_GREEN, lambda m=i: self.select_map(m))
            else:
                btn = Button(x, y, 150, 80, "Locked", DARK_GRAY, RED, lambda: None)
            self.map_buttons.append(btn)

        self.back_button = Button(20, 20, 100, 40, "BACK", GRAY, WHITE, lambda: self.change_state('MAP_SELECT'))

    def update_level_buttons(self):
        self.level_buttons = []
        self.level_buttons.append(Button(
            SCREEN_WIDTH // 2 - 220, SCREEN_HEIGHT // 2, 130, 60, 
            "Lvl 1 (Easy)", GREEN, BRIGHT_GREEN, lambda: self.start_game("easy")
        ))
        
        if self.lvl2_unlocked:
            self.level_buttons.append(Button(
                SCREEN_WIDTH // 2 - 70, SCREEN_HEIGHT // 2, 130, 60, 
                "Lvl 2 (Med)", GREEN, BRIGHT_GREEN, lambda: self.start_game("medium")
            ))
        else:
            self.level_buttons.append(Button(
                SCREEN_WIDTH // 2 - 70, SCREEN_HEIGHT // 2, 130, 60, 
                "Locked", DARK_GRAY, RED, lambda: None
            ))
            
        if self.lvl3_unlocked:
            self.level_buttons.append(Button(
                SCREEN_WIDTH // 2 + 80, SCREEN_HEIGHT // 2, 130, 60, 
                "Lvl 3 (Hard)", GREEN, BRIGHT_GREEN, lambda: self.start_game("hard")
            ))
        else:
            self.level_buttons.append(Button(
                SCREEN_WIDTH // 2 + 80, SCREEN_HEIGHT // 2, 130, 60, 
                "Locked", DARK_GRAY, RED, lambda: None
            ))

    def change_state(self, new_state):
        self.state = new_state
        if new_state == 'PLAYING':
            self.reset_uttc()
        elif new_state == 'LEVEL_SELECT':
            self.update_level_buttons()

    def select_map(self, map_num):
        self.selected_map = map_num
        self.change_state('LEVEL_SELECT')

    def start_game(self, diff):
        self.difficulty = diff
        self.change_state('PLAYING')

    def check_win(self, board):
        for row in board:
            if row[0] and row[0] == row[1] == row[2]: return row[0]
        for col in range(3):
            if board[0][col] and board[0][col] == board[1][col] == board[2][col]: return board[0][col]
        if board[0][0] and board[0][0] == board[1][1] == board[2][2]: return board[0][0]
        if board[0][2] and board[0][2] == board[1][1] == board[2][0]: return board[0][2]
        return None

    def is_board_full(self, board):
        return all(cell is not None for row in board for cell in row)

    def get_valid_moves(self):
        moves = []
        if self.active_board is not None:
            br, bc = self.active_board
            for r in range(3):
                for c in range(3):
                    if self.mini_boards[br][bc][r][c] is None:
                        moves.append((br, bc, r, c))
        else:
            for br in range(3):
                for bc in range(3):
                    if self.big_board[br][bc] is None:
                        for r in range(3):
                            for c in range(3):
                                if self.mini_boards[br][bc][r][c] is None:
                                    moves.append((br, bc, r, c))
        return moves

    def make_move(self, br, bc, r, c, symbol):
        self.mini_boards[br][bc][r][c] = symbol
        mini_winner = self.check_win(self.mini_boards[br][bc])
        if mini_winner and self.big_board[br][bc] is None:
            self.big_board[br][bc] = mini_winner
            self.game_winner = self.check_win(self.big_board)
            if self.game_winner == "X":
                if self.difficulty == "easy":
                    self.lvl2_unlocked = True
                elif self.difficulty == "medium":
                    self.lvl3_unlocked = True

        if self.big_board[r][c] is not None or self.is_board_full(self.mini_boards[r][c]):
            self.active_board = None
        else:
            self.active_board = (r, c)
        self.current_symbol = "O" if symbol == "X" else "X"

    def bot_move(self):
        valid_moves = self.get_valid_moves()
        if not valid_moves or self.game_winner:
            return

        if self.difficulty == "easy":
            move = random.choice(valid_moves)
        elif self.difficulty == "medium":
            for br, bc, r, c in valid_moves:
                temp_board = copy.deepcopy(self.mini_boards[br][bc])
                temp_board[r][c] = "O"
                if self.check_win(temp_board) == "O":
                    self.make_move(br, bc, r, c, "O")
                    return
            for br, bc, r, c in valid_moves:
                temp_board = copy.deepcopy(self.mini_boards[br][bc])
                temp_board[r][c] = "X"
                if self.check_win(temp_board) == "X":
                    self.make_move(br, bc, r, c, "O")
                    return
            move = random.choice(valid_moves)
        elif self.difficulty == "hard":
            best_score = -1000
            best_moves = [valid_moves[0]]
            for br, bc, r, c in valid_moves:
                score = 0
                temp_board = [row[:] for row in self.mini_boards[br][bc]]
                temp_board[r][c] = "O"
                if self.check_win(temp_board) == "O": score += 15
                temp_board[r][c] = "X"
                if self.check_win(temp_board) == "X": score += 10
                if r == 1 and c == 1: score += 3
                if br == 1 and bc == 1: score += 2

                if score > best_score:
                    best_score = score
                    best_moves = [(br, bc, r, c)]
                elif score == best_score:
                    best_moves.append((br, bc, r, c))
            move = random.choice(best_moves)
        self.make_move(*move, "O")

    def run(self):
        while True:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if self.state == 'START_MENU':
                self.start_button.handle_event(event)
            elif self.state == 'MAP_SELECT':
                for btn in self.map_buttons: btn.handle_event(event)
            elif self.state == 'LEVEL_SELECT':
                for btn in self.level_buttons: btn.handle_event(event)
            elif self.state == 'PLAYING':
                self.back_button.handle_event(event)
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and self.current_symbol == "X" and not self.game_winner:
                    mx, my = event.pos
                    self.handle_board_clicks(mx, my)

    def handle_board_clicks(self, mx, my):
        start_x, start_y = 175, 120
        big_dim, small_dim, pad = 140, 40, 10
        for br in range(3):
            for bc in range(3):
                bx = start_x + bc * (big_dim + pad)
                by = start_y + br * (big_dim + pad)
                if pygame.Rect(bx, by, big_dim, big_dim).collidepoint(mx, my):
                    if self.active_board is not None and (br, bc) != self.active_board: return
                    if self.big_board[br][bc] is not None: return
                    for r in range(3):
                        for c in range(3):
                            sx = bx + c * small_dim + 10
                            sy = by + r * small_dim + 10
                            if pygame.Rect(sx, sy, small_dim-4, small_dim-4).collidepoint(mx, my):
                                if self.mini_boards[br][bc][r][c] is None:
                                    self.make_move(br, bc, r, c, "X")

    def update(self):
        self.glitched_bkg.update()
        if self.state == 'PLAYING' and self.current_symbol == "O" and not self.game_winner:
            pygame.time.delay(400) 
            self.bot_move()

    def draw(self):
        self.glitched_bkg.draw(self.screen)
        font = pygame.font.Font(None, 45)
        
        if self.state == 'START_MENU':
            text = font.render("GENRE SHIFTER", True, WHITE)
            self.screen.blit(text, text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4)))
            self.start_button.draw(self.screen)
        elif self.state == 'MAP_SELECT':
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            overlay.fill(BLACK)
            overlay.set_alpha(100)
            self.screen.blit(overlay, (0,0))
            text = font.render("SELECT A MAP", True, WHITE)
            self.screen.blit(text, text.get_rect(center=(SCREEN_WIDTH // 2, 100)))
            for btn in self.map_buttons: btn.draw(self.screen)
        elif self.state == 'LEVEL_SELECT':
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            overlay.fill(BLACK)
            overlay.set_alpha(100)
            self.screen.blit(overlay, (0,0))
            text = font.render(f"MAP {self.selected_map}: SELECT DIFFICULTY", True, WHITE)
            self.screen.blit(text, text.get_rect(center=(SCREEN_WIDTH // 2, 100)))
            for btn in self.level_buttons: btn.draw(self.screen)
        elif self.state == 'PLAYING':
            self.draw_game_play()
        pygame.display.flip()

    def draw_game_play(self):
        font = pygame.font.Font(None, 32)
        info_str = f"Difficulty: {self.difficulty.upper()} | Turn: {self.current_symbol}"
        if self.game_winner:
            info_str = f"GAME OVER! WINNER: {self.game_winner}"
            
        text = font.render(info_str, True, WHITE)
        self.screen.blit(text, text.get_rect(center=(SCREEN_WIDTH // 2, 50)))
        self.back_button.draw(self.screen)
        
        start_x, start_y = 175, 120
        big_dim, small_dim, pad = 140, 40, 10
        
        for br in range(3):
            for bc in range(3):
                bx = start_x + bc * (big_dim + pad)
                by = start_y + br * (big_dim + pad)
                
                bg_color = DARK_GRAY
                if self.big_board[br][bc] is not None: bg_color = BLACK
                elif self.active_board is None: bg_color = GRAY
                elif (br, bc) == self.active_board: bg_color = YELLOW
                    
                pygame.draw.rect(self.screen, bg_color, (bx, by, big_dim, big_dim))
                pygame.draw.rect(self.screen, RED, (bx, by, big_dim, big_dim), 3)
                
                for r in range(3):
                    for c in range(3):
                        sx = bx + c * small_dim + 10
                        sy = by + r * small_dim + 10
                        pygame.draw.rect(self.screen, WHITE, (sx, sy, small_dim-4, small_dim-4))
                        
                        val = self.mini_boards[br][bc][r][c]
                        if val == "X":
                            pygame.draw.line(self.screen, CYAN, (sx+6, sy+6), (sx+small_dim-10, sy+small_dim-10), 3)
                            pygame.draw.line(self.screen, CYAN, (sx+6, sy+small_dim-10), (sx+small_dim-10, sy+6), 3)
                        elif val == "O":
                            pygame.draw.circle(self.screen, MAGENTA, (sx + small_dim//2 - 2, sy + small_dim//2 - 2), 12, 3)

                if self.big_board[br][bc] is not None:
                    b_win = self.big_board[br][bc]
                    if b_win == "X":
                        pygame.draw.line(self.screen, CYAN, (bx+15, by+15), (bx+big_dim-15, by+big_dim-15), 10)
                        pygame.draw.line(self.screen, CYAN, (bx+15, by+big_dim-15), (bx+big_dim-15, by+15), 10)
                    elif b_win == "O":
                        pygame.draw.circle(self.screen, MAGENTA, (bx + big_dim//2, by + big_dim//2), big_dim//2 - 15, 10)

if __name__ == "__main__":
    game = GameController()
    game.run()
