import pygame


class Button:


    bg_color = (0, 0, 198)
    fg_color = (4, 4, 4)


    dx = 5
    dy = 5


    def __init__(self, x, y, wid, hei, f, t):
        self.font = f
        self.rect = pygame.Rect(x, y, wid, hei)
        self.text = t
        self.text_surface = self.font.render(self.text, True, self.fg_color)


    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.action(event)


    def action(self, event):
        print('test')


    def set_text(self, t):
        self.text = t
        self.text_surface = self.font.render(self.text, True, self.fg_color)


    def draw(self, surface):
        pygame.draw.rect(surface, self.bg_color, self.rect)
        point = (self.rect.x + self.dx, self.rect.y + self.dy)
        surface.blit(self.text_surface, point)

