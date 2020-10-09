import pygame


class Gameboard:


    black = (71, 60, 35) 
    white = (235, 210, 160)
    t_green = (0, 255, 0)
    size = 8


    def __init__(self):
        self.top = 0
        self.left = 0

        self.field_wid = 64
        self.width = self.size * self.field_wid

        self.field_hei = 64
        self.height = self.size * self.field_hei

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

        self.fields = []

        for i in range(0, self.size):
            self.fields.append([])
            for j in range(0, self.size):
                field = {'piece' : {'type' : None, 'color' : None}, 'movable' : False}
                if (i % 2 == 0 and j % 2 == 0) or (i % 2 != 0 and j % 2 != 0):
                    field['color'] = self.white
                else:
                    field['color'] = self.black
                self.fields[i].append(field)



    def handle_click(self, x, y):
        x_pos = int((x - self.left) / self.field_wid)
        y_pos = int((y - self.top) / self.field_hei)
        print((x_pos, y_pos))


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
 

    def draw(self, surface):
        for i in range(0, self.size):
            for j in range(0, self.size):
                field = self.fields[i][j]
                x = i * self.field_wid + self.left
                y = j * self.field_hei + self.top
                r = (x, y, self.field_wid, self.field_hei)
                pygame.draw.rect(surface, field['color'], r)
                
                if field['piece']['type'] != None:
                    self.draw_piece(surface, field, x, y)

                if field['movable']:
                    self.draw_movable(surface, x, y)


    def draw_piece(self, surface, field, x, y):
        piece = field['piece']
        color = None
        if piece['color'] == 'white':
            color = 'w_'
        else:
            color = 'b_'

        piece_img = self.piece_images[color + piece['type']]
        scale = (self.field_wid, self.field_hei)
        piece_img = pygame.transform.scale(piece_img, scale)
        
        surface.blit(piece_img, (x, y))

    
    def draw_movable(self, surface, x, y):
        scale = (self.field_wid, self.field_hei)
        img = pygame.transform.scale(self.movable_img, scale)
        surface.blit(img, (x, y))
    
    
    
    
    #self.board:
    #[
    #{color : white, movable : True, piece : {type : 'queen', color : 'black'}}  
    #{color : black, movable : False, piece : None} ...
    #]

    #after connection get json with full init piece list from server
    
    #click on field: (client)
    #if turn => if has piece => if piece color same as client => then send action json to server with piece cords, recieve movable list from server and set movable to true
    #        => if has no piece => then cancel all movable
    #        => if field is movable then send action json(move) to server with cords and end turn

