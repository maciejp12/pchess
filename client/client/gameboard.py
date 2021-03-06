import pygame
import json


class Gameboard:

 
    black = (181, 136, 99)
    white = (240, 217, 181)
    t_green = (0, 255, 0)
    size = 8


    def __init__(self, x, y, wid, hei):

        self.rect = pygame.Rect(x, y, wid, hei)
        self.field_wid = self.rect.width / self.size
        self.field_hei = self.rect.height / self.size
    
        path = './resources/images/'
        
        self.piece_images = {
            'w_piece' : pygame.image.load(path + 'w_test_piece.png'),
            'w_pawn' : pygame.image.load(path + 'w_pawn_piece.png'),
            'w_rook' : pygame.image.load(path + 'w_rook_piece.png'),
            'w_knight' : pygame.image.load(path + 'w_knight_piece.png'),
            'w_bishop' : pygame.image.load(path + 'w_bishop_piece.png'),
            'w_queen' : pygame.image.load(path + 'w_queen_piece.png'),
            'w_king' : pygame.image.load(path + 'w_king_piece.png'),

            'b_piece' : pygame.image.load(path + 'b_test_piece.png'),
            'b_pawn' : pygame.image.load(path + 'b_pawn_piece.png'),
            'b_rook' : pygame.image.load(path + 'b_rook_piece.png'),
            'b_knight' : pygame.image.load(path + 'b_knight_piece.png'),
            'b_bishop' : pygame.image.load(path + 'b_bishop_piece.png'),
            'b_queen' : pygame.image.load(path + 'b_queen_piece.png'),
            'b_king' : pygame.image.load(path + 'b_king_piece.png')
        }

        self.movable_img = pygame.image.load(path + 'movable_field.png')
        self.moved_from = pygame.image.load(path + 'moved_from.png')
        self.moved_to = pygame.image.load(path + 'moved_to.png')

        self.side = None
        self.turn = None
        self.waiting = False

        self.fields = []
        self.selected = None

        self.last_move = None
        self.promotion_move = None

        for i in range(0, self.size):
            self.fields.append([])
            for j in range(0, self.size):
                field = dict()
                field['piece'] = {'type' : None, 'color' : None}
                field['movable'] = False

                if (i % 2 == 0 and j % 2 == 0) or (i % 2 != 0 and j % 2 != 0):
                    field['color'] = self.white
                else:
                    field['color'] = self.black
                
                self.fields[i].append(field)


    def set_client(self, cli):
        self.client = cli


    def handle_click(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                if self.side != None and self.turn != None and not self.waiting:
                    pos = pygame.mouse.get_pos()
                    x_pos = int((pos[0] - self.rect.left) / self.field_wid)
                    y_pos = int((pos[1] - self.rect.top) / self.field_hei)

                    self.handle_field_action(x_pos, y_pos)
                        

    def handle_field_action(self, x, y):
        if self.side == 1:
            y = 7 - y
        
        field = self.fields[x][y]
        if self.side == self.turn:
            if field['movable']:
                if self.selected != None:
                    action = self.build_move_request(x, y)
                    self.unselect_all()
                    self.waiting = True
                    self.send_to_server(json.dumps(action)) 
                else:
                    self.unselect_all()
            else:
                if self.selected != None:
                    if self.selected == (x, y):
                        self.unselect_all()
                        return
                    else:
                        self.unselect_all()
                    
                if field['piece']['type'] != None:
                    piece = field['piece']

                    side_col = None
                    if self.side == 0:
                        side_col = 'white'
                    else:
                        side_col = 'black'

                    if piece['color'] == side_col: 

                        self.unselect_all()
                        self.selected = (x, y)
                        
                        action = self.build_movable_request()
                        self.send_to_server(json.dumps(action))
                    else:
                        self.unselect_all()
                else:
                    self.unselect_all()
        else:
            self.unselect_all()


    def unselect_all(self):
        for column in self.fields:
            for field in column:
                if field['movable']:
                    field['movable'] = False
        
        self.selected = None


    def get_source(self):
        source = {
            'name' : self.client.conn.name,
            'side' : self.side
        }

        return source


    def build_action_package(self):
        action = {
            'source' : self.get_source(),
            'form' : 'action',
            'data' : None
        }

        return action


    def build_movable_request(self):
        data = {
            'action_type' : 'get_movable',
            'cords' : self.selected
        }

        action = self.build_action_package()
        action['data'] = data

        return action


    def build_move_request(self, x, y):
        data = {
            'action_type' : 'move',
            'source_cords' : self.selected,
            'target_cords' : (x, y)
        }

        action = self.build_action_package()
        action['data'] = data

        return action


    def handle_movable_response(self, data):
        if data['valid']: 
            mov = data['mov_list']
            for field in mov:
                self.fields[field[0]][field[1]]['movable'] = True
        else:
            self.unselect_all()


    def load_state(self, state):
        for piece in state:
            cord = piece['cord']
            p_col = piece['color']
            color = None
            if p_col == 0:
                color = 'white'
            elif p_col == 1:
                color = 'black'

            field = self.fields[cord[0]][cord[1]]
            field['piece']['type'] = piece['type']
            field['piece']['color'] = color
 

    def update_turn(self, data):
        #TODO log moves history (handle hits)
        move = data['move']
        source = move['source']
        target = move['target']

        source_field = self.fields[source[0]][source[1]]
        target_field = self.fields[target[0]][target[1]]

        target_field['piece']['type'] = source_field['piece']['type']
        target_field['piece']['color'] = source_field['piece']['color']
        source_field['piece']['type'] = None
        source_field['piece']['color'] = None

        if move['special']['type'] == 'castling':
            rook_move = move['special']['data']
            rook_source = rook_move['source']
            rook_target = rook_move['target']

            rook_source_field = self.fields[rook_source[0]][rook_source[1]]
            rook_target_field = self.fields[rook_target[0]][rook_target[1]]

            rook_target_field['piece']['type'] = rook_source_field['piece']['type']
            rook_target_field['piece']['color'] = rook_source_field['piece']['color']
            rook_source_field['piece']['type'] = None
            rook_source_field['piece']['color'] = None
        
        if move['special']['type'] == 'enpassant':
            passed_pawn = move['special']['data']['passed_pawn']
            passed_pawn_field = self.fields[passed_pawn[0]][passed_pawn[1]]
            passed_pawn_field['piece']['type'] = None
            passed_pawn_field['piece']['type'] = None

        self.last_move = {
                            'source' : (source[0], source[1]),
                            'target' : (target[0], target[1])
                         }


        if move['promotion']:
            if self.turn == self.side:
                self.handle_promotion(move)
            return

        self.turn = data['cur_turn']
        self.waiting = False

        if data['checkmated']:
            self.client.handle_message(self.build_checkmate_message(
                data['datetime'], self.turn))


    def build_checkmate_message(self, date, side):
        lose_side = 'WHITE'
        win_side = 'BLACK'
        if side == 1:
            lose_side = 'BLACK'
            win_side = 'WHITE'

        content = f'CHECKMATE {win_side} WINS, {lose_side} LOST'
        message = {
            'source' : {
                'name' : '',
                'side' : -1
            },
            'content' : content,
            'datetime' : date
        }

        return message


    def handle_promotion(self, move):
        self.promotion_move = move
        self.client.handling_promotion = True


    def finish_promotion(self, piece_type):
        promotion_response = {
            'action_type' : 'promotion_response',
            'piece_selected' : piece_type,
            'move' : self.promotion_move
        }

        action = self.build_action_package()
        action['data'] = promotion_response
        self.send_to_server(json.dumps(action))

        self.promotion_move = None
        self.client.handling_promotion = False


    def after_promotion(self, data):
        promotion = data['promotion']
        cords = promotion['cords']
        piece_replacement = promotion['piece_replacement']
        self.fields[cords[0]][cords[1]]['piece']['type'] = piece_replacement 
        self.turn = data['cur_turn']
        self.waiting = False

        if data['checkmated']:
            self.client.handle_message(self.build_checkmate_message(
                data['datetime'], self.turn))




    def on_invalid_move(self, data):
        self.unselect_all()
        self.waiting = False
        #TODO handle error logging


    def send_to_server(self, data):
        self.client.conn.send(data)


    def draw(self, surface):
        for i in range(0, self.size):
            for j in range(0, self.size):

                field = self.fields[i][j]
                x = i * self.field_wid + self.rect.left
                y = j * self.field_hei + self.rect.top
                
                if self.side == 1:
                    y = (7 - j) * self.field_hei + self.rect.top
                
                r = (x, y, self.field_wid, self.field_hei)
                pygame.draw.rect(surface, field['color'], r)
                
                if field['piece']['type'] != None:
                    self.draw_piece(surface, field, x, y)

                if self.last_move != None:
                    lms = self.last_move['source']
                    lmt = self.last_move['target']
        
                    if lms[0] == i and lms[1] == j:
                        self.draw_last_move_source(surface, x, y)
        
                    if lmt[0] == i and lmt[1] == j:
                        self.draw_last_move_target(surface, x, y)

                if field['movable']:
                    self.draw_movable(surface, x, y)

                if self.selected != None:
                    if (i, j) == self.selected:
                        self.draw_selected(surface, r)


    def draw_piece(self, surface, field, x, y):
        piece = field['piece']
        color = None
        if piece['color'] == 'white':
            color = 'w_'
        else:
            color = 'b_'

        piece_img = self.piece_images[color + piece['type']]
        scale = (int(self.field_wid), int(self.field_hei))

        piece_img = pygame.transform.scale(piece_img, scale)
        
        surface.blit(piece_img, (x, y))


    def draw_last_move_source(self, surface, x, y):
        scale = (int(self.field_wid), int(self.field_hei))
        img = pygame.transform.scale(self.moved_from, scale)
        surface.blit(img, (x, y))


    def draw_last_move_target(self, surface, x, y):
        scale = (int(self.field_wid), int(self.field_hei))
        img = pygame.transform.scale(self.moved_to, scale)
        surface.blit(img, (x, y))


    def draw_movable(self, surface, x, y):
        scale = (int(self.field_wid), int(self.field_hei))
        img = pygame.transform.scale(self.movable_img, scale)
        surface.blit(img, (x, y))


    def draw_selected(self, surface, r):
        pygame.draw.rect(surface, (0, 255, 0), r, 3)
