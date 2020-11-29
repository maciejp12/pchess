import pygame


class PromotionSelector:


    def __init__(self, x, y, wid, hei, cli):
        self.client = cli
        self.rect = pygame.Rect(x, y, wid, hei)

    
    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                if event.button == 1:
                    print(event.pos)
                    x = event.pos[0] - self.rect.x
                    
                    selected = (x / self.rect.width) * 4

                    if selected < 0:
                        x = 0
                    elif x > 3:
                        x = 3
                    
                    selected = int(selected)

                    pieces = ('rook', 'kngiht', 'bishop', 'queen')
                    self.client.gameboard.finish_promotion(pieces[selected])


    def draw(self, surface):
        images = self.client.gameboard.piece_images
        side = self.client.gameboard.side
        color = 'w_'
        if side == 1:
            color = 'b_'
        
        dx = self.rect.width / 4
        dy = self.rect.height

        scale = (int(dx), int(dy))
    
        img_list = list()
    
        img_list.append(pygame.transform.scale(images[color + 'rook'], scale))
        img_list.append(pygame.transform.scale(images[color + 'knight'], scale))
        img_list.append(pygame.transform.scale(images[color + 'bishop'], scale))
        img_list.append(pygame.transform.scale(images[color + 'queen'], scale))

        for i in range(0, len(img_list)):
            y = self.rect.y
            x = self.rect.x + (dx * i)
            surface.blit(img_list[i], (x, y))



    

