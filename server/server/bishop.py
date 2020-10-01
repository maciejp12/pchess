from .piece import Piece
from .linearpiece import LinearPiece


class Bishop(LinearPiece):


    init_fields = ({'position' : (2, 0), 'color' : Piece.black},
                   {'position' : (5, 0), 'color' : Piece.black},
                   {'position' : (2, 7), 'color' : Piece.white},
                   {'position' : (5, 7), 'color' : Piece.white})


    move_cords = {(1, 1), (1, -1), (-1, 1), (-1, -1)}


    def __init__(self, x, y, color, state):
        self.on_init(x, y, color, state)
