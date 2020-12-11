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
from .msgbox import MsgBox
from .promotionselector import PromotionSelector


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
        self.height = 640

        self.running = True
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.surface = pygame.Surface((self.width, self.height))

        pygame.display.set_caption('Pchess')

        self.clock = pygame.time.Clock()
        self.max_fps = 60.0
        self.show_debug = False
        
        self.gameboard = Gameboard(0, 0, 512, 512)
        self.gameboard.set_client(self)

        self.name_input = TextInput(600, 520, 200, 40, self.main_font)

        self.submit_name = SubmitName(600, 560, 200, 40, self.main_font, 
                                      'submit', self)

        self.msg_input = TextInput(540, 520, 260, 40, self.main_font)
        self.send_msg = SendMsg(540, 560, 260, 40, self.main_font, 'send',
                                self)
        self.msg_box = MsgBox(540, 0, 260, 520, self.main_font)

        self.promotion_sel = PromotionSelector(0, 540, 256, 64, self)

        self.block_input = False
        self.connected = False
        self.waiting = False
        self.in_game = False
        self.handling_promotion = False

        self.conn = None


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
                self.msg_box.handle_event(event)
                self.msg_input.handle_event(event)
                self.send_msg.handle_event(event)

                if self.msg_input.active:
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_RETURN:
                            self.send_msg.confirm_send()

                if self.handling_promotion:
                    self.promotion_sel.handle_event(event)

            if event.type == pygame.QUIT: 
                self.running = False

            elif event.type == pygame.KEYDOWN:

                if not self.name_input.active and not self.msg_input.active:
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
        self.msg_input.update(delta)

    
    def draw(self, delta):
        self.surface.fill((30, 30, 30))

        if self.in_game:
            self.gameboard.draw(self.surface)
            self.msg_input.draw(self.surface)
            self.send_msg.draw(self.surface)
            self.msg_box.draw(self.surface)
            if self.handling_promotion:
                self.promotion_sel.draw(self.surface)

        if not self.connected:
            self.name_input.draw(self.surface)
            self.submit_name.draw(self.surface)
        
        if self.show_debug:
            t_str = ' turn=' + str(self.gameboard.turn)
            s_str = ' side=' + str(self.gameboard.side)
            h_pr = ' hp=' + str(self.handling_promotion)

            db_text = str(delta) + t_str + s_str + h_pr
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


    def handle_message(self, message):
        if not self.in_game:
            return

        self.msg_box.add_message(message)
        
