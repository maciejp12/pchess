from .piece import Piece


class Pawn(Piece):


    init_fields = ({'position' : (0, 1), 'color' : Piece.black},
                   {'position' : (1, 1), 'color' : Piece.black},
                   {'position' : (2, 1), 'color' : Piece.black},
                   {'position' : (3, 1), 'color' : Piece.black},
                   {'position' : (4, 1), 'color' : Piece.black},
                   {'position' : (5, 1), 'color' : Piece.black},
                   {'position' : (6, 1), 'color' : Piece.black},
                   {'position' : (7, 1), 'color' : Piece.black},
                   
                   {'position' : (0, 6), 'color' : Piece.white},
                   {'position' : (1, 6), 'color' : Piece.white},
                   {'position' : (2, 2), 'color' : Piece.white},
                   {'position' : (3, 6), 'color' : Piece.white},
                   {'position' : (4, 6), 'color' : Piece.white},
                   {'position' : (5, 6), 'color' : Piece.white},
                   {'position' : (6, 6), 'color' : Piece.white},
                   {'position' : (7, 6), 'color' : Piece.white})

    def __init__(self, x, y, color, state):
        self.on_init(x, y, color, state)


    def get_special_moves(self):
        board = self.state.board
        
        special_list = super().get_special_moves()
        special_type = 'enpassant'
        
        dy = 0

        if self.color == Piece.white:
            dy = -1
        else:
            dy = 1

        for move in special_list:
            cords = move['cords']
            if cords == (self.x - 1, self.y + dy):
                if board[self.x - 1][self.y + dy] == None:
                    move['special'] = special_type

            if cords == (self.x + 1, self.y + dy):
                if board[self.x + 1][self.y + dy] == None:
                    move['special'] = special_type
        
        return special_list


    def get_movable(self, depth=0):
        board = self.state.board
        limit = 8

        movables = []

        dy = 0

        if self.color == Piece.white:
            dy = -1
        else:
            dy = 1

        y_pos = self.y + dy

        if 0 <= y_pos < limit:
            if board[self.x][y_pos] == None:
                movables.append((self.x, y_pos))
            
            x_pos = self.x - 1

            if 0 <= x_pos < limit:
                if board[x_pos][y_pos] != None:
                    if board[x_pos][y_pos].color != self.color:
                        movables.append((x_pos, y_pos))
                else:
                    pass_pawn = board[x_pos][y_pos - dy]
                    if pass_pawn != None:
                        if pass_pawn.piece_to_json()['type'] == 'pawn':
                            if pass_pawn.color != self.color:
                                if not pass_pawn.idle and pass_pawn.after_first_move:
                                    movables.append((x_pos, y_pos))
                
            x_pos = self.x + 1
            
            if 0 <= x_pos < limit:
                if board[x_pos][y_pos] != None:
                    if board[x_pos][y_pos].color != self.color:
                        movables.append((x_pos, y_pos))
                else:
                    pass_pawn = board[x_pos][y_pos - dy]
                    if pass_pawn != None:
                        if pass_pawn.piece_to_json()['type'] == 'pawn':
                            if pass_pawn.color != self.color:
                                if not pass_pawn.idle and pass_pawn.after_first_move:
                                    movables.append((x_pos, y_pos))



        y_pos = self.y + (2 * dy)

        if 0 <= y_pos < limit:
            if self.idle and board[self.x][y_pos] == None:
                if board[self.x][self.y + dy] == None:
                    movables.append((self.x, y_pos))



        if depth < 1:
            self.remove_check_moves(movables, depth)
        
        return movables


    def is_promoted(self):
        if self.color == Piece.white:
            if self.y == 0:
                return True
        elif self.color == Piece.black:
            if self.y == 7:
                return True
        
        return False
