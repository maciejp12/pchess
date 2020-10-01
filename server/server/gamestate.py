from .pawn import Pawn
from .tower import Tower
from .knight import Knight
from .bishop import Bishop
from .queen import Queen
from .king import King
import json


class GameState:


    size = 8


    def __init__(self):
        self.build_board()


    def build_board(self):
        self.board = []
        
        for i in range(0, self.size):
            self.board.append([])
            for j in range(0, self.size):
                self.board[i].append(None)
        

    def init_pieces(self):
        types = (King, Queen, Bishop, Knight, Tower, Pawn)
        
        for piece in types:
            for field in piece.init_fields:
                pos = field['position']
                col = field['color']
                self.board[pos[0]][pos[1]] = piece(pos[0], pos[1], col, self)
    

    def state_to_json(self):
        result = []
        
        for i in range(0, self.size):
            for j in range(0, self.size):
                if self.board[j][i] != None:
                    piece = self.board[j][i]
                    result.append({'cord' : (j, i),
                                   'type' : type(piece).__name__.lower(),
                                   'color' : piece.color})

        return json.dumps(result)