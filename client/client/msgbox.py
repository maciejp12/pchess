import pygame
from .msgview import MsgView


class MsgBox:


    bg_color = (16, 16, 16)
    msg_gap = 2


    def __init__(self, x, y, wid, hei, f):
        self.font = f
        self.rect = pygame.Rect(x, y, wid, hei)
        self.messages = list()
        self.scroll_y = 0
        self.scrollable = False


    def draw(self, surface):
        pygame.draw.rect(surface, self.bg_color, self.rect)

        dy = 18 + self.msg_gap
        cy = self.rect.y + self.rect.height

        for i in range(self.scroll_y, len(self.messages)):
            msg = self.messages[len(self.messages) - i - 1]
            
            point = (self.rect.x, cy)
            msg.draw(surface, point, self.rect.width, dy)

            cy -= msg.rect.height + self.msg_gap
            if msg.rect.y < 0:
                self.scrollable = True


    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos) and self.scrollable:
                if event.button == 4:
                    if self.scroll_y < len(self.messages) - 1:
                        self.scroll_y += 1
                elif event.button == 5:
                    if self.scroll_y > 0:
                        self.scroll_y -= 1


    def add_message(self, message):
        self.messages.append(MsgView(message, self.font))
    

