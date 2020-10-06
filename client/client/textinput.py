import pygame


class TextInput:


    color = (234, 234, 234)


    def __init__(self, x, y, wid, hei, f):
        self.font = f
        self.rect = pygame.Rect(x, y, wid, hei)
        self.text = ''
        self.text_surface = self.font.render(self.text, True, self.color)
        self.active = False

    
    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.active = not self.active
            else:
                self.active = False

        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode

            self.text_surface = self.font.render(self.text, True, self.color)

    
    def draw(self, surface):
        surface.blit(self.text_surface, (self.rect.x + 5, self.rect.y + 5))
        pygame.draw.rect(surface, self.color, self.rect, 2)

