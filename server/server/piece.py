class Piece:

    white = 0
    black = 1

    init_fields = ()


    def get_movable(self, depth=0):
        return list()


    def remove_check_moves(self, moves, depth=0):
        to_remove = list()

        for move in moves:
            state_copy = self.state.copy_state()
            board_copy = state_copy.board
            self_copy = board_copy[self.x][self.y]
            board_copy[move[0]][move[1]] = self_copy
            board_copy[self.x][self.y] = None
            self_copy.x = move[0]
            self_copy.y = move[1]
            self_copy.idle = False

            if state_copy.is_checked(board_copy, self.color, depth + 1):
                to_remove.append(move)
        
        for move in to_remove:
            moves.remove(move)
        
        


    def on_init(self, x, y, color, state):
        self.x = x
        self.y = y
        self.color = color
        self.state = state
        self.state.board[x][y] = self
        self.idle = True
        self.promoted = False


    def after_move(self):
        if self.idle:
            self.idle = False


    def is_promoted(self):
        return False


    def piece_to_json(self):
        result = dict()

        return {'cord' : (self.x, self.y),
                'type' : type(self).__name__.lower(),
                'color' : self.color
                }

