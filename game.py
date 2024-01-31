import pygame
from pygame.locals import QUIT, MOUSEBUTTONDOWN
# game.py
import pygame
from board import Board
from graphics import Graphics


WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
GOLD = (255, 215, 0)
HIGH = (160, 190, 255)

NORTHWEST = "northwest"
NORTHEAST = "northeast"
SOUTHWEST = "southwest"
SOUTHEAST = "southeast"


class Game:
    def __init__(self):
        self.graphics = Graphics()
        self.board = Board()
        self.turn = BLUE
        self.selected_piece = None
        self.hop = False
        self.selected_legal_moves = []

    def setup(self):
        self.graphics.setup_window()

    def event_loop(self):
        self.mouse_pos = self.graphics.board_coords(pygame.mouse.get_pos())

        if self.selected_piece is not None:
            self.selected_legal_moves = self.board.legal_moves(self.selected_piece, self.hop)

        for event in pygame.event.get():
            if event.type == QUIT:
                self.terminate_game()

            if event.type == MOUSEBUTTONDOWN:
                self.handle_mouse_click()

    def handle_mouse_click(self):
        if not self.hop:
            self.handle_regular_click()
        elif self.hop:
            self.handle_hop_click()

    def handle_regular_click(self):
        if self.board.location(self.mouse_pos).occupant is not None and \
           self.board.location(self.mouse_pos).occupant.color == self.turn:
            self.selected_piece = self.mouse_pos
        elif self.selected_piece is not None and self.mouse_pos in self.board.legal_moves(self.selected_piece):
            self.board.move_piece(self.selected_piece, self.mouse_pos)
            self.handle_capture()
            self.end_turn()

    def handle_hop_click(self):
        if self.selected_piece is not None and self.mouse_pos in self.board.legal_moves(self.selected_piece, self.hop):
            self.board.move_piece(self.selected_piece, self.mouse_pos)
            self.handle_capture()

            if not self.board.legal_moves(self.mouse_pos, self.hop):
                self.end_turn()
            else:
                self.selected_piece = self.mouse_pos

    def handle_capture(self):
        if self.mouse_pos not in self.board.adjacent(self.selected_piece):
            captured_piece_pos = ((self.selected_piece[0] + self.mouse_pos[0]) >> 1, (self.selected_piece[1] + self.mouse_pos[1]) >> 1)
            self.board.remove_piece(captured_piece_pos)
            self.hop = True
            self.selected_piece = self.mouse_pos

    def update(self):
        self.graphics.update_display(self.board, self.selected_legal_moves, self.selected_piece)

    def terminate_game(self):
        pygame.quit()
        quit()

    def end_turn(self):
        self.turn = RED if self.turn == BLUE else BLUE
        self.selected_piece = None
        self.selected_legal_moves = []
        self.hop = False

        if self.check_for_endgame():
            winner = "RED" if self.turn == BLUE else "BLUE"
            self.graphics.draw_message(f"{winner} WINS!")

    def check_for_endgame(self):
        for x in range(8):
            for y in range(8):
                if self.board.location((x, y)).color == BLACK and self.board.location((x, y)).occupant is not None and \
                        self.board.location((x, y)).occupant.color == self.turn:
                    if self.board.legal_moves((x, y)):
                        return False
        return True
    

