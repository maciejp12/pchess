from .piece import Piece
from .linearpiece import LinearPiece


class King(LinearPiece):


    init_fields = ({'position' : (4, 0), 'color' : Piece.black},
                   {'position' : (4, 7), 'color' : Piece.white})


    move_cords = {(1, 0), (-1, 0), (0, 1), (0, -1),
                  (1, 1), (1, -1), (-1, 1), (-1, -1)}


    def __init__(self, x, y, color, state):
        self.on_init(x, y, color, state)


    def get_special_moves(self):
        special_list = super().get_special_moves()
        special_type = 'castling'

        if self.idle:
            special_list.append(
                {
                    'cords' : (self.x - 2, self.y),
                    'special' : special_type
                }
            )

            special_list.append(
                {
                    'cords' : (self.x + 2, self.y),
                    'special' : special_type
                }
            )

        return special_list


    def get_movable(self, depth=0):
        movables = []

        x = self.x
        y = self.y

        for field in super().get_movable(depth):
            if x - 1 <= field[0] <= x + 1 and y - 1 <= field[1] <= y + 1:
                movables.append(field)
    

        if depth < 1:
            self.remove_check_moves(movables, depth)

        return movables
