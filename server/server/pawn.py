from .piece import Piece


class Pawn(Piece):


    init_fields = ({'position' : (0, 1), 'color' : Piece.black},
                   {'position' : (1, 1), 'color' : Piece.black},
                   {'position' : (2, 1), 'color' : Piece.black},
                   {'position' : (3, 1), 'color' : Piece.black},
                   {'position' : (4, 1), 'color' : Piece.black},
                   {'position' : (5, 1), 'color' : Piece.black},
                   {'position' : (6, 1), 'color' : Piece.black},
                   {'position' : (7, 1), 'color' : Piece.black},
                   
                   {'position' : (0, 6), 'color' : Piece.white},
                   {'position' : (1, 6), 'color' : Piece.white},
                   {'position' : (2, 6), 'color' : Piece.white},
                   {'position' : (3, 6), 'color' : Piece.white},
                   {'position' : (4, 6), 'color' : Piece.white},
                   {'position' : (5, 6), 'color' : Piece.white},
                   {'position' : (6, 6), 'color' : Piece.white},
                   {'position' : (7, 6), 'color' : Piece.white})

    def __init__(self, x, y, color, state):
        self.on_init(x, y, color, state)
        self.idle = True


    def get_movable(self):
        board = self.state.board
        limit = 8

        movables = []

        dy = 0

        if self.color == Piece.white:
            dy = -1
        else:
            dy = 1

        y_pos = self.y + dy

        if 0 <= y_pos < limit:
            if board[self.x][y_pos] == None:
                movables.append((self.x, y_pos))
            
            x_pos = self.x - 1

            if 0 <= x_pos < limit:
                if board[x_pos][y_pos] != None:
                    if board[x_pos][y_pos].color != self.color:
                        movables.append((x_pos, y_pos))
            
            x_pos = self.x + 1
            
            if 0 <= x_pos < limit:
                if board[x_pos][y_pos] != None:
                    if board[x_pos][y_pos].color != self.color:
                        movables.append((x_pos, y_pos))




        y_pos = self.y + (2 * dy)

        if 0 <= y_pos < limit:
            if self.idle and board[self.x][y_pos] == None:
                if board[self.x][self.y + dy] == None:
                    movables.append((self.x, y_pos))


        return movables


    def after_move(self):
        if self.idle:
            self.idle = False

