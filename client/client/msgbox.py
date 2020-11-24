import pygame
from .msgview import MsgView


class MsgBox:


    bg_color = (16, 16, 16)
    msg_gap = 2

    def __init__(self, x, y, wid, hei, f):
        self.font = f
        self.rect = pygame.Rect(x, y, wid, hei)
        self.messages = list()


    def draw(self, surface):
        pygame.draw.rect(surface, self.bg_color, self.rect)

        dy = 18 + self.msg_gap
        cy = self.rect.y + self.rect.height

        for i in range(0, len(self.messages)):
            msg = self.messages[len(self.messages) - i - 1]
            
            point = (self.rect.x, cy)
            msg.draw(surface, point, self.rect.width, dy)

            cy -= msg.rect.height + self.msg_gap

    def add_message(self, message):
        self.messages.append(MsgView(message, self.font))
    
        
