class Piece:

    white = 0
    black = 1

    init_fields = ()


    def get_movable(self):
        return []


    def on_init(self, x, y, color, state):
        self.x = x
        self.y = y
        self.color = color
        self.state = state
        self.state.board[x][y] = self
        self.idle = True


    def after_move(self):
        if self.idle:
            self.idle = False


    def piece_to_json(self):
        result = dict()

        return {'cord' : (self.x, self.y),
                'type' : type(self).__name__.lower(),
                'color' : self.color
                }

