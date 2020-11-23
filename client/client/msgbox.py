import pygame
from .msgview import MsgView


class MsgBox:


    bg_color = (16, 16, 16)


    def __init__(self, x, y, wid, hei, f):
        self.font = f
        self.rect = pygame.Rect(x, y, wid, hei)
        self.messages = list()


    def draw(self, surface):
        pygame.draw.rect(surface, self.bg_color, self.rect)

        dy = 40
        cy = self.rect.y + self.rect.height - dy

        for i in range(0, len(self.messages)):
            msg = self.messages[i]
            rect = pygame.Rect(self.rect.x, cy, self.rect.width - 2, dy - 2)
            msg.draw(surface, rect)
            cy -= 40

    def add_message(self, message):
        self.messages.append(MsgView(message, self.font))
    
        
