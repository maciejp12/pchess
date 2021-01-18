import pygame


class MsgView:


    bg_color = (236, 236, 236)

    bg_color_white = (236, 200, 144)
    bg_color_black = (164, 160, 96)

    fg_color = (4, 4, 4)


    def __init__(self, message, f):
        self.font = f

        time = message['datetime'].split(' ')[1][:-7]
        username = message['source']['name']
        content = message['content']
        self.user_side = message['source']['side']

        self.text = time + ' ' + username + ': ' + content

        if self.user_side == -1:
            self.text = time + '||' + content

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
        
        bg = self.bg_color
        if self.user_side == 0:
            bg = self.bg_color_white
        elif self.user_side == 1:
            bg = self.bg_color_black

        pygame.draw.rect(surface, bg, self.rect) 
        
        for i in range(0, len(lines)):
            line = lines[i]
            if self.rect.y + hei > 0:
                surface.blit(line, (self.rect.x, self.rect.y + (i * hei)))
