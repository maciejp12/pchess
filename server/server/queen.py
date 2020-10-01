from .piece import Piece
from .linearpiece import LinearPiece


class Queen(LinearPiece):


    init_fields = ({'position' : (3, 0), 'color' : Piece.black},
                   {'position' : (3, 7), 'color' : Piece.white})


    move_cords = {(1, 0), (-1, 0), (0, 1), (0, -1),
                  (1, 1), (1, -1), (-1, 1), (-1, -1)}


    def __init__(self, x, y, color, state):
        self.on_init(x, y, color, state)
