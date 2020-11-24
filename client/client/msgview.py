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
        self.rect = None


    def draw(self, surface, point, wid, hei): 
        text_surface = self.font.render(self.text, True, self.fg_color)
        lines = []
        cur_text = ''
        last_surface = self.font.render('', True, self.fg_color)

        for c in self.text:
            cur_text += c
            cur_surface = self.font.render(cur_text, True, self.fg_color)
            if cur_surface.get_width() > wid:
                lines.append(last_surface)
                cur_text = '' 
                continue
            last_surface = cur_surface
       
        lines.append(last_surface)

        self.rect = pygame.Rect(point[0], point[1] - (len(lines) * hei), 
                                wid, len(lines) * hei)
        
        pygame.draw.rect(surface, self.bg_color, self.rect) 
        
        for i in range(0, len(lines)):
            line = lines[i]
            if self.rect.y + hei > 0:
                surface.blit(line, (self.rect.x, self.rect.y + (i * hei)))
