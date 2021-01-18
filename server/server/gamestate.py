from .pawn import Pawn
from .rook import Rook
from .knight import Knight
from .bishop import Bishop
from .queen import Queen
from .king import King
from .piece import Piece
import random
import json
from datetime import datetime



class GameState:


    size = 8


    def __init__(self):
        self.build_board()
        self.clients = list()
        self.cur_turn = None


    def set_server(self, serv):
        self.server = serv


    def add_client(self, client):
        """
            Add a client to clients list is its empty
            If there is already one client connected and second one 
            and start game
            
            If there are at least two clients in clients list
            do nothing
        """

        if len(self.clients) < 2:
            self.clients.append(client)
            if len(self.clients) == 2:
                self.on_start()


    def handle_on_connect(self, client):
        """
            After only one client is connected to game send to the only client
            `waiting for second client` signal
        """

        if len(self.clients) == 1:
            if self.clients[0] == client:
                wait_signal = {
                    'form' : 'signal',
                    'data' : {
                        'signal_type' : 'waiting'
                    }
                }
                client.send_data(json.dumps(wait_signal))


    def on_start(self):
        """
            Called after two connected clients are on game clients list

            Give clients randomly selected side(black(1) or white(0) color),
            initialize pieces on board and send to both clients signal with
            color and board data
        """

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
        """
            Build signal with all pieces on board data
        """

        initstate = {
            'form' : 'signal',
            'data' : {
                'signal_type' : 'onstart',
                'color' : color,
                'state' : self.state_to_json(),
                'turn' : self.cur_turn,
                'datetime' : str(datetime.now())
            }
        }

        return initstate


    def build_before_turn_action(self, move, checkmate):
        """
            Build signal with data about last move made
        """

        before = {
            'form' : 'action',
            'data' : {
                'action_type' : 'before_turn',
                'move' : move,
                'cur_turn' : self.cur_turn,
                'checkmated' : checkmate,
                'datetime' : str(datetime.now())
            }
        }

        return before


    def build_promotion_action(self, promotion, checkmate):
        promotion_action = {
            'form' : 'action',
            'data' : {
                'action_type' : 'after_promotion',
                'promotion' : promotion,
                'cur_turn' : self.cur_turn,
                'checkmated' : checkmate,
                'datetime' : str(datetime.now())
            }
        }

        return promotion_action


    def build_invalid_move_action(self, move):
        """
            Build signal with data about invalid move request
        """

        invalid = {
            'form' : 'action',
            'data' : {
                'action_type' : 'invalid_move',
                'move' : move
            }
        }

        return invalid


    def handle_get_movable(self, data, client):
        """
            Handle get_movable request signal from client
            
            Gets data of selected piece by client, sends to only this client
            data signal with all possible moves of the piece in current
            board state

            If given cord is invalid(no piece in cords, not clients turn
            or piece is not clients color) send back invalide response to
            client
        """

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
                    
                    if not (self.is_checked(self.board, self.cur_turn)):
                        if piece.piece_to_json()['type'] == 'king':
                            moves = self.handle_castling_movable(self.cur_turn, piece)
                            for m in moves:
                                mov.append(m)
                    
                    response['data']['valid'] = True
                    response['data']['mov_list'] = mov

        client.send_data(json.dumps(response))


    def handle_castling_movable(self, side, king):        
        moves = list()

        if king == None:
            return moves

        if not king.idle:
            return moves

        x = king.x
        y = king.y

        for d in (0, 7):
            rook = self.board[d][y]
            if rook != None:
                if rook.color == side and rook.idle:
                    clear = True
                    ran = range(1, x)
        
                    if d == 7:
                        ran = range(x + 1, 7)
        
                    for i in ran:
                        if self.board[i][y] != None:
                            clear = False
                            break

                    if clear:
                        state_copy = self.copy_state()
                        board_copy = state_copy.board
                        king_copy = board_copy[x][y]
                        rook_copy = board_copy[d][y]
                        
                        dx = x - 2
                        if d == 7:
                            dx = x + 2
                        board_copy[dx][y] = king_copy
                        board_copy[x][y] = None
                        king_copy.x = dx

                        dx = x - 1
                        if d == 7:
                            dx = x + 1

                        board_copy[dx][y] = rook_copy
                        board_copy[d][y] = None
                        rook_copy.x = dx

                        if not state_copy.is_checked(board_copy, side):
                            dx = x - 2
                            if d == 7:
                                dx = x + 2
                            moves.append((dx, y))

        return moves


    def handle_move(self, data, client):
        """
            Handle move request signal from client

            If the move is valid call make_move, change current turn to
            opposite and build before turn action and send it to all clients

            If the move is invalid build invalid action move and send it to
            client from given move request
        """

        cl_side = data['source']['side']

        source = data['data']['source_cords']
        target = data['data']['target_cords']

        if self.cur_turn == cl_side:
            piece = self.board[source[0]][source[1]]
            if piece != None:
                if piece.color == cl_side:
                    moves = piece.get_special_moves()
                    valid_move = False
                    special = None
                    for move in moves:
                        if move['cords'] == tuple(target):
                            valid_move = True
                            special = move['special']
                            break
                        
                    if valid_move:
                        move = self.make_move(source, target, special)
                        
                        if move['promotion']:
                            action = self.build_before_turn_action(move, False)
                            self.send_to_all(json.dumps(action))
                            return

                        if self.cur_turn == 1:
                            self.cur_turn = 0
                        else:
                            self.cur_turn = 1

                        checkmate = False
                        if self.is_checked(self.board, self.cur_turn):
                            if not self.has_moves(self.cur_turn):
                                checkmate = True

                        action = self.build_before_turn_action(move, checkmate)
                        self.send_to_all(json.dumps(action))
                        return

        move = {'source' : source, 'target' : target}
        client.send_data(json.dumps(self.build_invalid_move_action(move)))


    def handle_promotion_response(self, data, client):
        promotion = data['data']
        
        piece_type = promotion['piece_selected']
        piece_replacement = None
        x = promotion['move']['target'][0]
        y = promotion['move']['target'][1]
        
        side = data['source']['side']

        if piece_type == 'rook':
            piece_replacement = Rook(x, y, side, self)
        elif piece_type == 'knight':
            piece_replacement = Knight(x, y, side, self)
        elif piece_type == 'bishop':
            piece_replacement = Bishop(x, y, side, self)
        else:
            piece_replacement = Queen(x, y, side, self)

        piece_replacement.idle = False
        piece_replacement.promoted = True

        if self.cur_turn == 1:
            self.cur_turn = 0
        else:
            self.cur_turn = 1

        checkmate = False
        if self.is_checked(self.board, self.cur_turn):
            if not self.has_moves(self.cur_turn):
                checkmate = True

        promotion_data = {
            'piece_replacement' : piece_type,
            'cords' : (x, y)
        }

        action = self.build_promotion_action(promotion_data, checkmate)
        self.send_to_all(json.dumps(action))


    def make_move(self, source, target, special=None):
        """
            Moves source piece to target fieed

            Field of source piece is set to None

            Returns move log with source and target fields before and after
            making move and if target field was not None before moving
            hit is set to True if target field was None before moving
            hit is set to False
        """

        source_piece = self.board[source[0]][source[1]]
        target_field = self.board[target[0]][target[1]]

        hit = False

        if target_field != None:
            hit = True

        source_pre = source_piece.piece_to_json()
        target_pre = None
        
        if hit:
            target_pre = target_field.piece_to_json()

        self.board[target[0]][target[1]] = source_piece
        self.board[source[0]][source[1]] = None
        source_piece.x = target[0]
        source_piece.y = target[1]

        special_data = None

        if special == 'castling':
            xside = 0
            dx = 1
            if source[0] < target[0]:
                xside = 7
                dx = -1
            rook = self.board[xside][target[1]]
            
            self.board[target[0] + dx][target[1]] = rook
            self.board[xside][target[1]] = None
            rook.x = target[0] + dx
            rook.idle = False
            
            special_data = {
                'source' : (xside, target[1]),
                'target' : (target[0] + dx, target[1])
            }
        
        if special == 'enpassant':
            dy = 0

            if source_piece.color == Piece.white:
                dy = -1
            else:
                dy = 1

            self.board[target[0]][target[1] - dy] = None

            hit = True

            special_data = {
                'passed_pawn' : (target[0], target[1] - dy)
            }

        for row in self.board:
            for field in row:
                if field != None:
                    field.after_first_move = False

        source_piece.after_move()
        promotion = source_piece.is_promoted()
    
        move_log = {
            'source' : source,
            'target' : target,
            'hit' : hit,
            'promotion' : promotion,
            'special' : {
                'type' : special,
                'data' : special_data
            },
            'log' : {
                'source_pre' : source_pre,
                'target_pre' : target_pre
            }
        }

        return move_log


    def is_checked(self, board, side, level=0):
        """
            Returns True if king of given side on given board state
            is being checked, else returns False

            If there is no king of given side on given board returns False
        """

        checked = False

        oponent_side = 0
        if side == 0:
            oponent_side = 1

        side_king = None
        side_king_cords = None

        for i in range(0, len(board)):
            row = board[i]
            for j in range(0, len(row)):
                piece = board[i][j]
                if piece != None:
                    if piece.color == side:
                        if piece.piece_to_json()['type'] == 'king':
                            side_king = piece
                            side_king_cords = (i, j)
                            break

        if side_king == None: 
            return checked
 

        for row in board:
            for piece in row:
                if piece != None: 
                    if piece.color == oponent_side:
                        for field in piece.get_movable(level):
                            if field == side_king_cords:
                                checked = True


        return checked


    def has_moves(self, side):
        """
            Return True if side pameter side has any moves aviable in current turn
            else return False
        """

        all_moves = list()
        for row in self.board:
            for piece in row:
                if piece != None:
                    if piece.color == side:
                        for move in piece.get_movable():
                            all_moves.append(move)
        return len(all_moves) > 0


    def send_to_all(self, data):
        """
            Send data to all clients connected to this game
        """

        for client in self.clients:
            client.send_data(data)


    def build_board(self):
        """
            Build initial empty chess board

            Board is represented as list (len equal to self.size) of lists
            of length of self.size, initially all elements of them are set to
            None
        """

        self.board = []
        
        for i in range(0, self.size):
            self.board.append([])
            for j in range(0, self.size):
                self.board[i].append(None)


    def init_pieces(self):
        """
            Make standard initial chess setup, add pieces to board
            Called after two players connect to game and game is ready to start
        """
        
        types = (King, Queen, Bishop, Knight, Rook, Pawn)
        
        for piece in types:
            for field in piece.init_fields:
                pos = field['position']
                col = field['color']
                self.board[pos[0]][pos[1]] = piece(pos[0], pos[1], col, self)


    def parse_board(self):
        """
            Return current game state board as list of lists of dicts of pieces
            If field on board in (x, y) cords is None, field on result list
            in (x, y) is None too
        """


        result = list()

        for i in range(0, self.size):
            result.append(list())
            for j in range(0, self.size):
                if self.board[i][j] == None:
                    result[i].append(None)
                else:
                    piece = self.board[i][j]
                    result[i].append(piece.piece_to_json())
        
        return result


    def copy_state(self):
        copy = GameState()

        for i in range(0, self.size):
            for j in range(0, self.size):
                piece = self.board[i][j]
                if piece != None:
                    piece_class = piece.__class__
                    piece_copy = piece_class(piece.x, piece.y, piece.color, 
                                             copy)
                    
                    piece_copy.idle = piece.idle
                    copy.board[i][j] = piece_copy

        return copy


    def state_to_json(self):
        """
            Return current game state (data of all pieces on board) as dict
        """

        result = list()
        
        for i in range(0, self.size):
            for j in range(0, self.size):
                if self.board[j][i] != None:
                    piece = self.board[j][i]
                    result.append(piece.piece_to_json())

        return result

