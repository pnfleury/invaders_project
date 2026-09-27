import pygame
from random import randint

class CRT():
    """ Emulate CRT monitor class """
    
    def __init__(self, game):
        
        self.game = game
        self.tv = pygame.image.load(self.game.resource_path('assets/graphics/tv.png')).convert_alpha()
        self.tv = pygame.transform.scale(self.tv, (self.game.s.screen_width, self.game.s.screen_heigth))

    def create_crt_lines(self):
        line_height = 3
        line_amount = int(self.game.s.screen_heigth / line_height)
        for line in range (line_amount):
            y_pos = line * line_height
            pygame.draw.line(self.tv, 'black', (0, y_pos), (self.game.s.screen_width, y_pos), 1)
    
    def draw (self):
        self.tv.set_alpha(randint(75,90))
        self.create_crt_lines()
        self.game.screen.blit(self.tv,(0,0))