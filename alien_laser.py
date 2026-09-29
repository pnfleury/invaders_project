import pygame
from random import randint
from pygame.sprite import Sprite

class AlienLaser (Sprite):
    """ Alien laser class """

    def __init__(self, pos, game):
        super().__init__()
        self.game = game
        self.sprites = []
        self.sprites.append (pygame.image.load(self.game.resource_path('assets/graphics/alien_laser_0.png')).convert_alpha())
        self.sprites.append (pygame.image.load(self.game.resource_path('assets/graphics/alien_laser_1.png')).convert_alpha())
        self.current_sprite = 0
        self.image = self.sprites[self.current_sprite]
        self.rect = self.image.get_rect(center = pos)
    
    def update(self):
       
        self.current_sprite += 0.2
        if self.current_sprite >= len (self.sprites):
            self.current_sprite = 0
                       
        self.image = self.sprites[int(self.current_sprite)]
        self.rect.y += self.game.s.alien_laser_speed
        if self.rect.y > self.game.s.screen_heigth: 
            self.kill()

class ExtraLaser (Sprite):
    """ Extra laser class """

    def __init__(self, pos, game):
        super().__init__()
        self.game = game
        self.sprites = []
        self.sprites.append (pygame.image.load(self.game.resource_path('assets/graphics/extra_shoot/sprite_0.png')).convert_alpha())
        self.sprites.append (pygame.image.load(self.game.resource_path('assets/graphics/extra_shoot/sprite_1.png')).convert_alpha())
        self.sprites.append (pygame.image.load(self.game.resource_path('assets/graphics/extra_shoot/sprite_2.png')).convert_alpha())
        self.sprites.append (pygame.image.load(self.game.resource_path('assets/graphics/extra_shoot/sprite_3.png')).convert_alpha())
        self.current_sprite = 0
        self.image = self.sprites[self.current_sprite]
        self.rect = self.image.get_rect(center = pos)
        self.push = 0
        
    def update(self):
        
        self.current_sprite += 0.8
        if self.current_sprite >= len (self.sprites):
            self.current_sprite = 0
        
        self.image = self.sprites[int(self.current_sprite)]
        
        self.rect.y += self.game.s.extra_laser_speed + self.push
        self.push += 0.1
        if self.rect.y > self.game.s.screen_heigth:
            self.push = 0 
            self.kill()