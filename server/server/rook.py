from .piece import Piece
from .linearpiece import LinearPiece


class Rook(LinearPiece):


    init_fields = ({'position' : (0, 0), 'color' : Piece.black},
                   {'position' : (7, 0), 'color' : Piece.black},
                   {'position' : (0, 7), 'color' : Piece.white},
                   {'position' : (7, 7), 'color' : Piece.white})


    move_cords = {(1, 0), (-1, 0), (0, 1), (0, -1)}


    def __init__(self, x, y, color, state):
        self.on_init(x, y, color, state)
