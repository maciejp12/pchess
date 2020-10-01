from .piece import Piece


class LinearPiece(Piece):


    move_cords = {}
    
    
    def __init__(self, x, y, color, state):
        self.on_init(x, y, color, state)


    def get_movable(self):
        return self.get_movable_lines(self.move_cords)

    
    def get_movable_line(self, dx, dy, mov):
        board = self.state.board
        limit = 8

        x_pos = self.x + dx
        y_pos = self.y + dy

        while 0 <= x_pos < limit and 0 <= y_pos < limit:
            if board[x_pos][y_pos] == None:
                if x_pos != self.x or y_pos != self.y:
                    mov.append((x_pos, y_pos))
                    x_pos += dx
                    y_pos += dy
            else:
                if board[x_pos][y_pos].color != self.color:
                    mov.append((x_pos, y_pos))
                    break
                else:
                    break


    def get_movable_lines(self, cords):
        movables = []

        for cord in cords:
            self.get_movable_line(cord[0], cord[1], movables)
        
        return movables

            