import pygame

WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
GOLD = (255, 215, 0)
HIGH = (160, 190, 255)

class Graphics:
    def __init__(self):
        self.caption = "Checkers"
        self.fps = 60
        self.clock = pygame.time.Clock()
        self.window_size = 600
        self.screen = pygame.display.set_mode((self.window_size, self.window_size))
        self.background = pygame.image.load('board.png')
        self.square_size = self.window_size >> 3
        self.piece_size = self.square_size >> 1
        self.message = False
        self.start_button_rect = pygame.Rect(self.window_size // 4, self.window_size // 2, self.window_size // 2, 50)
        self.player_names = ["Player 1", "Player 2"]
        self.game_started = False

    def setup_window(self):
        pygame.init()
        pygame.display.set_caption(self.caption)

    def update_display(self, board, legal_moves, selected_piece):
        self.screen.blit(self.background, (0, 0))

        if not self.game_started:
            self.draw_start_screen()
            self.check_start_button_click()
        else:
            self.highlight_squares(legal_moves, selected_piece)
            self.draw_board_pieces(board)

        if self.message:
            self.screen.blit(self.text_surface_obj, self.text_rect_obj)

        pygame.display.update()
        self.clock.tick(self.fps)

    def draw_start_screen(self):
        pygame.draw.rect(self.screen, GOLD, (0, 0, self.window_size, self.window_size))
        self.draw_start_button()
        self.draw_player_names()

    def draw_start_button(self):
        pygame.draw.rect(self.screen, RED, self.start_button_rect)
        font = pygame.font.Font(pygame.font.get_default_font(), 32)
        text_surface = font.render("Start Game", True, WHITE)
        text_rect = text_surface.get_rect(center=self.start_button_rect.center)
        self.screen.blit(text_surface, text_rect)

    def draw_player_names(self):
        font = pygame.font.Font(pygame.font.get_default_font(), 20)
        for i, name in enumerate(self.player_names):
            text_surface = font.render(name, True, WHITE)
            text_rect = text_surface.get_rect(center=(self.window_size // 2, self.window_size // 2 - 50 + i * 50))
            self.screen.blit(text_surface, text_rect)

    def check_start_button_click(self):
        mouse_pos = pygame.mouse.get_pos()
        click, _, _ = pygame.mouse.get_pressed()
        if self.start_button_rect.collidepoint(mouse_pos) and click:
            self.game_started = True

    def draw_board_pieces(self, board):
        for x in range(8):
            for y in range(8):
                occupant = board.matrix[x][y].occupant
                if occupant is not None:
                    self.draw_piece(occupant.color, self.pixel_coords((x, y)))
                    if occupant.king:
                        self.draw_king_circle(self.pixel_coords((x, y)))

    def draw_piece(self, color, pixel_coords):
        pygame.draw.circle(self.screen, color, pixel_coords, self.piece_size)

    def draw_king_circle(self, pixel_coords):
        pygame.draw.circle(self.screen, GOLD, pixel_coords, int(self.piece_size / 1.7), self.piece_size >> 2)

    def pixel_coords(self, board_coords):
        return (board_coords[0] * self.square_size + self.piece_size, board_coords[1] * self.square_size + self.piece_size)

    def board_coords(self, pixel):
        return (pixel[0] // self.square_size, pixel[1] // self.square_size)


    def highlight_squares(self, squares, origin):
        for square in squares:
            pygame.draw.rect(self.screen, HIGH, (square[0] * self.square_size, square[1] * self.square_size, self.square_size, self.square_size))
        if origin is not None:
            pygame.draw.rect(self.screen, HIGH, (origin[0] * self.square_size, origin[1] * self.square_size, self.square_size, self.square_size))

    def draw_message(self, message):
        self.message = True
        font_obj = pygame.font.Font(pygame.font.get_default_font(), 44)
        text_surface_obj = font_obj.render(message, True, HIGH, BLACK)
        text_rect_obj = text_surface_obj.get_rect()
        text_rect_obj.center = (self.window_size >> 1, self.window_size >> 1)

        self.screen.blit(text_surface_obj, text_rect_obj)
        pygame.display.update()
        pygame.time.delay(2000)  # Display the message for 2 seconds
        self.message = False
