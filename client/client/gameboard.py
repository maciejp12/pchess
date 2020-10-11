import pygame
import json


class Gameboard:


    black = (71, 60, 35) 
    white = (235, 210, 160)
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
            'w_tower' : pygame.image.load(path + 'w_tower_piece.png'),
            'w_knight' : pygame.image.load(path + 'w_knight_piece.png'),
            'w_bishop' : pygame.image.load(path + 'w_bishop_piece.png'),
            'w_queen' : pygame.image.load(path + 'w_queen_piece.png'),
            'w_king' : pygame.image.load(path + 'w_king_piece.png'),

            'b_piece' : pygame.image.load(path + 'b_test_piece.png'),
            'b_pawn' : pygame.image.load(path + 'b_pawn_piece.png'),
            'b_tower' : pygame.image.load(path + 'b_tower_piece.png'),
            'b_knight' : pygame.image.load(path + 'b_knight_piece.png'),
            'b_bishop' : pygame.image.load(path + 'b_bishop_piece.png'),
            'b_queen' : pygame.image.load(path + 'b_queen_piece.png'),
            'b_king' : pygame.image.load(path + 'b_king_piece.png')
        }

        self.movable_img = pygame.image.load(path + 'movable_field.png')

        self.side = None
        self.turn = None

        self.fields = []
        self.selected = None

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
                if self.side != None and self.turn != None:
                    pos = pygame.mouse.get_pos()
                    x_pos = int((pos[0] - self.rect.left) / self.field_wid)
                    y_pos = int((pos[1] - self.rect.top) / self.field_hei)

                    self.handle_field_action(x_pos, y_pos)
                        

    def handle_field_action(self, x, y):
        field = self.fields[x][y]
        if self.side == self.turn:
            if field['movable']:
                if self.selected != None:
                    action = self.build_move_request(x, y)
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
                        print((x, y))

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
 

    def update_turn(self, turn):
        self.turn = turn


    def send_to_server(self, data):
        self.client.conn.send(data)


    def draw(self, surface):
        for i in range(0, self.size):
            for j in range(0, self.size):
                field = self.fields[i][j]
                x = i * self.field_wid + self.rect.left
                y = j * self.field_hei + self.rect.top
                r = (x, y, self.field_wid, self.field_hei)
                pygame.draw.rect(surface, field['color'], r)
                
                if field['piece']['type'] != None:
                    self.draw_piece(surface, field, x, y)

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

    
    def draw_movable(self, surface, x, y):
        scale = (self.field_wid, self.field_hei)
        img = pygame.transform.scale(self.movable_img, scale)
        surface.blit(img, (x, y))


    def draw_selected(self, surface, r):
        pygame.draw.rect(surface, (0, 255, 0), r, 3)
