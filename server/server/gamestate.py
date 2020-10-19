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


    def __init__(self):
        self.build_board()
        self.clients = list()
        self.cur_turn = None


    def set_server(self, serv):
        self.server = serv


    def add_client(self, client):
        if len(self.clients) < 2:
            self.clients.append(client)
            if len(self.clients) == 2:
                self.on_start()


    def on_start(self):
        print('STARTING GAME')
        cols = list()
        cols.append(random.randint(0, 1))

        if cols[0] == 0:
            cols.append(1)
        else:
            cols.append(0)

        self.init_pieces()
        self.cur_turn = 0

        initstate = self.build_initstate_signal(cols[0])
        self.clients[0].send_data(json.dumps(initstate))
        
        initstate = self.build_initstate_signal(cols[1])
        self.clients[1].send_data(json.dumps(initstate))
 


    def build_initstate_signal(self, color):
        initstate = {
            'form' : 'signal',
            'data' : {
                'signal_type' : 'onstart',
                'color' : color,
                'state' : self.state_to_json(),
                'turn' : self.cur_turn
            }
        }

        return initstate


    def build_before_turn_action(self, move):
        before = {
            'form' : 'action',
            'data' : {
                'action_type' : 'before_turn',
                'move' : move,
                'cur_turn' : self.cur_turn
            }
        }

        return before


    def build_invalid_move_action(self, move):
        invalid = {
            'form' : 'action',
            'data' : {
                'action_type' : 'invalid_move',
                'move' : move
            }
        }

        return invalid


    def handle_get_movable(self, data, client): 
        cl_side = data['source']['side']
        cords = data['data']['cords']

        response = {
            'form' : 'action',
            'data' : {
                'action_type' : 'movable_response',
                'valid' : False,
                'mov_list' : None
            }
        }

        if self.cur_turn == cl_side:
            piece = self.board[cords[0]][cords[1]]
            if piece != None:
                if piece.color == cl_side:
                    mov = piece.get_movable() 
                    response['data']['valid'] = True
                    response['data']['mov_list'] = mov

        client.send_data(json.dumps(response))


    def handle_move(self, data, client):
        cl_side = data['source']['side']

        source = data['data']['source_cords']
        target = data['data']['target_cords']

        if self.cur_turn == cl_side:     
            piece = self.board[source[0]][source[1]]
            if piece != None:
                if piece.color == cl_side:
                    if tuple(target) in piece.get_movable():
                        move = self.make_move(source, target)
                        
                        if self.cur_turn == 1:
                            self.cur_turn = 0
                        else:
                            self.cur_turn = 1

                        action = self.build_before_turn_action(move)
                        self.send_to_all(json.dumps(action))
                        return
        
        move = {'source' : source, 'target' : target}
        client.send_data(json.dumps(build_invalid_move_action(move))


    def make_move(self, source, target):
        source_piece = self.board[source[0]][source[1]]
        target_field = self.board[source[0]][source[1]]
        hit = False
        if target_field != None:
            hit = True

        self.board[target[0]][target[1]] = source_piece
        self.board[source[0]][source[1]] = None
        source_piece.x = target[0]
        source_piece.y = target[1]

        source_piece.after_move()

        move_log = {
            'source' : source,
            'target' : target,
            'hit' : hit
        }

        return move_log


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
