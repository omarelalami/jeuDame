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


class Square:
    def __init__(self, color, occupant=None):
        self.color = color
        self.occupant = occupant


class Piece:
    def __init__(self, color, king=False):
        self.color = color
        self.king = king


class Board:

    def __init__(self):
        self.matrix = self.new_board()
        self.eating_moves = []

    def new_board(self):
        matrix = [[None] * 8 for _ in range(8)]

        for x in range(8):
            for y in range(8):
                if (x % 2 != 0) and (y % 2 == 0):
                    matrix[y][x] = Square(WHITE)
                elif (x % 2 != 0) and (y % 2 != 0):
                    matrix[y][x] = Square(BLACK)
                elif (x % 2 == 0) and (y % 2 != 0):
                    matrix[y][x] = Square(WHITE)
                elif (x % 2 == 0) and (y % 2 == 0):
                    matrix[y][x] = Square(BLACK)

        for x in range(8):
            for y in range(3):
                if matrix[x][y].color == BLACK:
                    matrix[x][y].occupant = Piece(RED)
            for y in range(5, 8):
                if matrix[x][y].color == BLACK:
                    matrix[x][y].occupant = Piece(BLUE)

        return matrix

    def location(self, pixel):
        x, y = pixel
        return self.matrix[x][y]

    def adjacent(self, pixel):
        x, y = pixel
        return [self.rel(NORTHWEST, (x, y)), self.rel(NORTHEAST, (x, y)), self.rel(SOUTHWEST, (x, y)),
                self.rel(SOUTHEAST, (x, y))]

    def on_board(self, pixel):
        x, y = pixel
        return 0 <= x <= 7 and 0 <= y <= 7

    def rel(self, dir, pixel):
        x, y = pixel
        if dir == NORTHWEST:
            return x - 1, y - 1
        elif dir == NORTHEAST:
            return x + 1, y - 1
        elif dir == SOUTHWEST:
            return x - 1, y + 1
        elif dir == SOUTHEAST:
            return x + 1, y + 1
        else:
            return 0

    def remove_piece(self, pixel):
        x, y = pixel
        self.matrix[x][y].occupant = None

    def move_piece(self, pixel_start, pixel_end):
        start_x, start_y = pixel_start
        end_x, end_y = pixel_end
        self.matrix[end_x][end_y].occupant = self.matrix[start_x][start_y].occupant
        self.remove_piece((start_x, start_y))
        self.king((end_x, end_y))

    def king(self, pixel):
        x, y = pixel
        if self.location((x, y)).occupant is not None:
            if (self.location((x, y)).occupant.color == BLUE and y == 0) or \
                    (self.location((x, y)).occupant.color == RED and y == 7):
                self.location((x, y)).occupant.king = True

    def blind_legal_moves(self, pixel):
        x, y = pixel
        occupant = self.location((x, y)).occupant

        if occupant is not None:
            if occupant.king == False and occupant.color == BLUE:
                return [self.rel(NORTHWEST, (x, y)), self.rel(NORTHEAST, (x, y))]
            elif occupant.king == False and occupant.color == RED:
                return [self.rel(SOUTHWEST, (x, y)), self.rel(SOUTHEAST, (x, y))]
            else:
                return [self.rel(NORTHWEST, (x, y)), self.rel(NORTHEAST, (x, y)), self.rel(SOUTHWEST, (x, y)),
                        self.rel(SOUTHEAST, (x, y))]
        else:
            return []

    def legal_moves(self, pixel, hop=False):
        x, y = pixel
        blind_legal_moves = self.blind_legal_moves((x, y))
        legal_moves = []

        if not hop:
            for move in blind_legal_moves:
                if self.on_board(move):
                    if self.location(move).occupant is None:
                        legal_moves.append(move)
                    elif self.location(move).occupant.color != self.location((x, y)).occupant.color and \
                            self.on_board((move[0] + (move[0] - x), move[1] + (move[1] - y))) and \
                            self.location((move[0] + (move[0] - x), move[1] + (move[1] - y))).occupant is None:
                        legal_moves.append((move[0] + (move[0] - x), move[1] + (move[1] - y)))
                        # if not self.eating_moves:
                        #     self.eating_moves.append([pixel, (move[0] + (move[0] - x), move[1] + (move[1] - y))])
                        # elif [pixel, (move[0] + (move[0] - x), move[1] + (move[1] - y))] not in self.eating_moves:
                        #     self.eating_moves.append([pixel, (move[0] + (move[0] - x), move[1] + (move[1] - y))])

        else:  # hop == True
            for move in blind_legal_moves:
                if self.on_board(move) and self.location(move).occupant is not None:
                    if self.location(move).occupant.color != self.location((x, y)).occupant.color and \
                            self.on_board((move[0] + (move[0] - x), move[1] + (move[1] - y))) and \
                            self.location((move[0] + (move[0] - x), move[1] + (move[1] - y))).occupant is None:
                        legal_moves.append((move[0] + (move[0] - x), move[1] + (move[1] - y)))

        return legal_moves

    def update_eating_moves(self, color):
        self.eating_moves = []
        for x in range(8):
            for y in range(8):
                square = self.matrix[x][y]
                if square.occupant is not None:
                    if square.occupant.color == color:
                        moves = self.legal_moves((x, y))
                        if moves:
                            for move in moves:
                                if move not in self.blind_legal_moves((x, y)):
                                    self.eating_moves.append(((x, y), move))

    def all_possible_moves(self, color):
        all_moves = []
        for x in range(8):
            for y in range(8):
                square = self.matrix[x][y]
                if square.occupant is not None and square.occupant.color == color:
                    moves = self.legal_moves((x, y))
                    if moves:
                        all_moves.extend([((x, y), move) for move in moves])
        return all_moves

