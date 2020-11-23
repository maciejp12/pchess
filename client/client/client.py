import sys
import os
import pygame
import json
from datetime import datetime
from .clientconnection import ClientConnection
from .gameboard import Gameboard
from .textinput import TextInput
from .submitname import SubmitName
from .sendmsg import SendMsg


class Client:


    def __init__(self):
        pygame.init()
        x = 64
        y = 64

        os.environ['SDL_VIDEO_WINDOW_POS'] = str(x) + ',' + str(y)
        pygame.font.init()

        self.main_font = pygame.font.Font('./resources/Ubuntu-R.ttf', 17)
        self.debug_text = self.main_font.render('', True, (0, 128, 128))

        self.width = 800
        self.height = 600

        self.running = True
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.surface = pygame.Surface((self.width, self.height))

        self.clock = pygame.time.Clock()
        self.max_fps = 60.0
        self.show_debug = True
        
        self.gameboard = Gameboard(0, 0, 512, 512)
        self.gameboard.set_client(self)

        self.name_input = TextInput(600, 0, 160, 40, self.main_font)

        self.submit_name = SubmitName(600, 50, 150, 40, self.main_font, 
                                      'submit', self)

        self.msg_input = TextInput(600, 300, 150, 40, self.main_font)
        self.send_msg = SendMsg(600, 350, 150, 40, self.main_font, 'send',
                                self)

        self.block_input = False
        self.connected = False
        self.waiting = False
        self.in_game = False

        self.conn = None
        #self.conn = ClientConnection(self)
        #self.conn.connect()


    def start(self):

        while self.running:
            dt = self.clock.tick(self.max_fps)

            self.input()
            self.update(dt)
            self.draw(dt)

        if self.conn != None:
            self.conn.disconnect()
        pygame.display.quit()
        pygame.quit()
        sys.exit()


    def input(self):

        for event in pygame.event.get():

            if not self.block_input:
                self.name_input.handle_event(event)
                self.submit_name.handle_event(event)
            
            if self.in_game:
                self.gameboard.handle_click(event)
                self.msg_input.handle_event(event)
                self.send_msg.handle_event(event)
            if event.type == pygame.QUIT: 
                self.running = False

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    print('space')
                if event.key == pygame.K_t:
                    self.send_message('test_message 1')
                if not self.name_input.active:
                    if event.key == pygame.K_f:
                        self.show_debug = not self.show_debug

            elif event.type == pygame.MOUSEBUTTONDOWN:
                click = pygame.mouse.get_pos()
                x = click[0]
                y = click[1]

        keys = pygame.key.get_pressed()

        if keys[pygame.K_F4] and keys[pygame.K_LALT]:
            self.running = False


    def update(self, delta):
        self.name_input.update(delta)

    
    def draw(self, delta):
        self.surface.fill((30, 30, 30))

        if self.in_game:
            self.gameboard.draw(self.surface)
            self.msg_input.draw(self.surface)
            self.send_msg.draw(self.surface)

        if not self.connected:
            self.name_input.draw(self.surface)
            self.submit_name.draw(self.surface)
        
        if self.show_debug:
            t_str = ' turn=' + str(self.gameboard.turn)
            s_str = ' side=' + str(self.gameboard.side)

            db_text = str(delta) + t_str + s_str
            self.debug_text = self.main_font.render(db_text, True, (0, 128, 128))
            self.surface.blit(self.debug_text, (0, 0))

        self.screen.blit(self.surface, (0, 0))

        pygame.display.flip()


    def init_connection(self, new_name):
        self.block_input = True 
        self.conn = ClientConnection(self)
        self.conn.name = new_name
        self.conn.connect()


    def send_message(self, content):
        if self.conn == None:
            return

        side = self.gameboard.side
 
        msg = {
            'source' : {
                'name' : self.conn.name,
                'side' : side
            },
            'form' : 'message',
            'data' : {
                'content' : content, 
            }
        }

        self.conn.send(json.dumps(msg))

