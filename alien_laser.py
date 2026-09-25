import pygame
from pygame.sprite import Sprite
from settings import Settings

class AlienLaser (Sprite):
    """ Alien laser class """

    def __init__(self, pos):
        super().__init__()
        self.settings = Settings()
        self.sprites = []
        self.sprites.append (pygame.image.load('assets/graphics/alien_laser_0.png'))
        self.sprites.append (pygame.image.load('assets/graphics/alien_laser_1.png'))
        self.current_sprite = 0
        self.image = self.sprites[self.current_sprite]
        self.rect = self.image.get_rect(center = pos)
    
    def update(self):
       
        self.current_sprite += 0.2
        if self.current_sprite >= len (self.sprites):
            self.current_sprite = 0
                       
        self.image = self.sprites[int(self.current_sprite)]
        self.rect.y += self.settings.alien_laser_speed
        if self.rect.y > self.settings.screen_heigth: 
            self.kill()