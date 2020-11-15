from .piece import Piece


class Knight(Piece):


    init_fields = ({'position' : (1, 0), 'color' : Piece.black},
                   {'position' : (6, 0), 'color' : Piece.black},
                   {'position' : (1, 7), 'color' : Piece.white},
                   {'position' : (6, 7), 'color' : Piece.white})


    move_fields = {(1, 2), (2, 1), (2, -1), (1, -2),
                   (-1, -2), (-2, -1), (-2, 1), (-1, 2)}


    def __init__(self, x, y, color, state):
        self.on_init(x, y, color, state)
    

    def get_movable(self, depth=0):
        board = self.state.board
        limit = 8

        movables = []
        
        for field in self.move_fields:
            x_pos = self.x + field[0]
            y_pos = self.y + field[1]

            if 0 <= x_pos < limit and 0 <= y_pos < limit:
                if board[x_pos][y_pos] == None:
                    movables.append((x_pos, y_pos))
                else:
                    if board[x_pos][y_pos].color != self.color:
                        movables.append((x_pos, y_pos))

        if depth < 1:
            self.remove_check_moves(movables, depth)
        return movables



