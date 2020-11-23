import pygame


class MsgView:


    bg_color = (200, 180, 120)
    fg_color = (4, 4, 4)


    def __init__(self, message, f):
        self.font = f

        time = message['datetime'].split(' ')[1][:-7]
        username = message['source']['name']
        content = message['content']
        
        self.text = time + ' ' + username + ': ' + content


    def draw(self, surface, rect):
        pygame.draw.rect(surface, self.bg_color, rect)
        point = (rect.x, rect.y)
        text_surface = self.font.render(self.text, True, self.fg_color)
        surface.blit(text_surface, point)

