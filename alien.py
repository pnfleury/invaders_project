import pygame
from pygame.sprite import Sprite
from settings import Settings

class Alien(Sprite):
    """ Alien class """
    
    def __init__(self, color, x, y):
        super().__init__()
       
        file_path = 'assets/graphics/' + color + '.png'
        self.sprites = []
        self.value = 0
        self.sprites.append(pygame.image.load(file_path).convert_alpha())

        if color == 'red': 
            self.sprites.append(pygame.image.load('assets/graphics/alien_red/sprite_1.png').convert_alpha())
            self.sprites.append(pygame.image.load('assets/graphics/alien_red/sprite_2.png').convert_alpha())
            self.sprites.append(pygame.image.load('assets/graphics/alien_red/sprite_3.png').convert_alpha())
            self.sprites.append(pygame.image.load('assets/graphics/alien_red/sprite_4.png').convert_alpha())
            self.value = 100
        elif color == "green": 
            self.sprites.append(pygame.image.load('assets/graphics/alien_green/sprite_1.png').convert_alpha())
            self.sprites.append(pygame.image.load('assets/graphics/alien_green/sprite_2.png').convert_alpha())
            self.value = 200
        else: 
            self.sprites.append(pygame.image.load('assets/graphics/alien_prata/sprite_1.png').convert_alpha())
            self.sprites.append(pygame.image.load('assets/graphics/alien_prata/sprite_2.png').convert_alpha())
            
            
            self.value = 300
        
        self.current_sprite = 0
        self.image = self.sprites[self.current_sprite]
       
        self.rect = self.image.get_rect(topleft = (x,y))
        self.x = float(self.rect.x)
     
    
    def update(self, direction, alien_speed):
       
        self.current_sprite += 0.02 * alien_speed
        if self.current_sprite >= len (self.sprites):
                self.current_sprite = 0
                                              
        self.image = self.sprites[int(self.current_sprite)]
        self.x += alien_speed * direction
        self.rect.x = self.x
       
        
class Extra(Sprite):
    """ Extra alien ship class"""
    
    def __init__(self, side):
        super().__init__()
        self.settings = Settings()
        self.sprites = []
        self.sprites.append(pygame.image.load('assets/graphics/alien_extra/extra.png').convert_alpha())
        self.sprites.append(pygame.image.load('assets/graphics/alien_extra/extra1.png').convert_alpha())
        self.sprites.append(pygame.image.load('assets/graphics/alien_extra/extra2.png').convert_alpha())
        self.sprites.append(pygame.image.load('assets/graphics/alien_extra/extra3.png').convert_alpha())
        self.sprites.append(pygame.image.load('assets/graphics/alien_extra/extra4.png').convert_alpha())
        self.sprites.append(pygame.image.load('assets/graphics/alien_extra/extra5.png').convert_alpha())
       
        self.current_sprite = 0
        self.image = self.sprites[self.current_sprite]
    
        if side == 'right':
            x = self.settings.screen_width + 50
            self.speed = - self.settings.extra_speed 
        else:
            x = -50
            self.speed = self.settings.extra_speed
        
        self.rect = self.image.get_rect(topleft = (x, 60))

        self.execute = True
                    
    def update(self):
        if self.execute:
           
            self.current_sprite += 0.2
            if self.current_sprite >= len (self.sprites):
                 self.current_sprite = 0
                                                          
            self.image = self.sprites[int(self.current_sprite)]
            self.rect.x += self.speed
            


        
        
    
        
