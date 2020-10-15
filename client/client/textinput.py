import pygame


class TextInput:


    active_color = (234, 234, 234)
    inactive_color = (122, 122, 122)
    font_color = (4, 4, 4)

    def __init__(self, x, y, wid, hei, f):
        self.font = f
        self.rect = pygame.Rect(x, y, wid, hei)
        self.text = ''
        self.color = self.inactive_color
        self.text_surface = self.font.render(self.text, True, self.font_color)
        self.active = False
        self.backspace_max_delay = 500
        self.backspace_delay = 0
        self.backspace_hold = False

    
    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.active = not self.active
            else:
                self.active = False
            
            if self.active:
                self.color = self.active_color
            else:
                self.color = self.inactive_color


        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                    self.backspace_hold = True
                elif event.key == pygame.K_ESCAPE and self.active:
                    self.active = False
                    self.color = self.inactive_color
                else:
                    self.text += event.unicode

            f = self.font_color
            self.text_surface = self.font.render(self.text, True, f)

        keys = pygame.key.get_pressed()

        if self.active:
            if not keys[pygame.K_BACKSPACE]:
                self.backspace_hold = False
                self.backspace_delay = 0   


    def update(self, dt):
        if self.active:
            if self.backspace_hold:
                if self.backspace_delay < self.backspace_max_delay:
                    self.backspace_delay += dt
                else:
                    self.text = self.text[:-1]
                    f = self.font_color
                    self.text_surface = self.font.render(self.text, True, f)


    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)
        surface.blit(self.text_surface, (self.rect.x + 5, self.rect.y + 5))
        
