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
        self.next_moves = None
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

        #self.board.eating_moves=[]

    def handle_regular_click(self):

        if self.board.location(self.mouse_pos).occupant is not None and \
           self.board.location(self.mouse_pos).occupant.color == self.turn:
            self.selected_piece = self.mouse_pos
        elif self.selected_piece is not None and self.mouse_pos in self.board.legal_moves(self.selected_piece):
            self.board.update_eating_moves(self.turn)
            print(self.board.eating_moves)
            if self.board.eating_moves:
                for move in self.board.eating_moves:
                    print("move:")
                    print(move[0])
                    print("selected_piece:")
                    print(self.selected_piece)
                    if move[0] == self.selected_piece and self.mouse_pos == move[1]:
                        print("working")
                        self.board.move_piece(self.selected_piece, self.mouse_pos)
                        self.handle_capture()
                        if not self.hop:
                            self.end_turn()
                    else: pass
            else:
                self.board.move_piece(self.selected_piece, self.mouse_pos)
                self.handle_capture()
                if not self.hop:
                    self.end_turn()
    def handle_capture(self):
        if self.mouse_pos not in self.board.adjacent(self.selected_piece):
            captured_piece_pos = (
            (self.selected_piece[0] + self.mouse_pos[0]) >> 1, (self.selected_piece[1] + self.mouse_pos[1]) >> 1)
            self.board.remove_piece(captured_piece_pos)
            self.selected_piece = self.mouse_pos
            if self.board.legal_moves(self.selected_piece):
                print("other options")
                print(self.board.legal_moves(self.selected_piece))
                for move in self.board.legal_moves(self.selected_piece):
                    if move not in self.board.adjacent(self.selected_piece):
                        self.hop = True
            print("Capture successful")


    def handle_hop_click(self):
        if self.selected_piece is not None and self.mouse_pos in self.board.legal_moves(self.selected_piece, self.hop):
            self.board.move_piece(self.selected_piece, self.mouse_pos)
            self.handle_capture()
            self.next_moves = self.board.legal_moves(self.mouse_pos, self.hop)
            if self.next_moves:
                print("Continue capturing")
                self.selected_piece = self.mouse_pos  # Update selected piece
                self.selected_legal_moves = self.next_moves  # Update legal moves
                self.update()
            else:
                print("No more captures, ending turn")
                self.end_turn()
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
    

