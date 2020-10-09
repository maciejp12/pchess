from .pawn import Pawn
from .tower import Tower
from .knight import Knight
from .bishop import Bishop
from .queen import Queen
from .king import King
import random
import json


class GameState:


    size = 8


    def __init__(self, serv):
        self.build_board()
        self.server = serv
        self.clients = list()


    def add_client(self, client):
        if len(self.clients) < 2:
            self.clients.append(client)
            if len(self.clients) == 2:
                self.on_start()


    def on_start(self):
        #getcolors
        col_0 = random.randint(0, 1)
        col_1 = 0
        if col_0 == 0:
            col_1 = 1

        self.init_pieces()
        
        initstate = {
            'form' : 'signal',
            'data' : {
                'signal_type' : 'onstart',
                'color' : col_0,
                'state' : self.state_to_json() 
            } 
        }
         
        self.clients[0].send_data(json.dumps(initstate))

        initstate['data']['color'] = col_1

        self.clients[1].send_data(json.dumps(initstate))
 

    def send_to_all(self, data):
        for client in self.clients:
            client.send_data(data)


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

        return result
