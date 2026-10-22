import pygame
from pygame.sprite import Sprite

class Alien(Sprite):
    """ Alien class """
    
    def __init__(self, color, x, y, game):
        super().__init__()
        
        self.game = game
        file_path = 'assets/graphics/' + color + '.png'
        self.sprites = []
        self.value = 0
        self.sprites.append(pygame.image.load(self.game.resource_path(file_path)).convert_alpha())

        if color == 'red': 
            self.sprites.append(pygame.image.load(self.game.resource_path('assets/graphics/alien_red/sprite_1.png')).convert_alpha())
            self.sprites.append(pygame.image.load(self.game.resource_path('assets/graphics/alien_red/sprite_2.png')).convert_alpha())
            self.sprites.append(pygame.image.load(self.game.resource_path('assets/graphics/alien_red/sprite_3.png')).convert_alpha())
            self.sprites.append(pygame.image.load(self.game.resource_path('assets/graphics/alien_red/sprite_4.png')).convert_alpha())
            self.value = 100
        elif color == "green": 
            self.sprites.append(pygame.image.load(self.game.resource_path('assets/graphics/alien_green/sprite_1.png')).convert_alpha())
            self.sprites.append(pygame.image.load(self.game.resource_path('assets/graphics/alien_green/sprite_2.png')).convert_alpha())
            self.value = 200
        else: 
            self.sprites.append(pygame.image.load(self.game.resource_path('assets/graphics/alien_prata/sprite_1.png')).convert_alpha())
            self.sprites.append(pygame.image.load(self.game.resource_path('assets/graphics/alien_prata/sprite_2.png')).convert_alpha())
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
    
    def __init__(self, side, game):
        super().__init__()
        self.game = game
        self.sprites = []
        self.sprites.append(pygame.image.load(self.game.resource_path('assets/graphics/alien_extra/extra.png')).convert_alpha())
        self.sprites.append(pygame.image.load(self.game.resource_path('assets/graphics/alien_extra/extra1.png')).convert_alpha())
        self.sprites.append(pygame.image.load(self.game.resource_path('assets/graphics/alien_extra/extra2.png')).convert_alpha())
        self.sprites.append(pygame.image.load(self.game.resource_path('assets/graphics/alien_extra/extra3.png')).convert_alpha())
        self.sprites.append(pygame.image.load(self.game.resource_path('assets/graphics/alien_extra/extra4.png')).convert_alpha())
        self.sprites.append(pygame.image.load(self.game.resource_path('assets/graphics/alien_extra/extra5.png')).convert_alpha())

       
        self.current_sprite = 0
        self.image = self.sprites[self.current_sprite]
        self.x_pos = self.image.get_width()    
        self.side = ''

        if side == 'right':
            self.side = 'right'
            x = self.game.s.screen_width + 50
            self.value = -1
            self.speed = - self.game.s.extra_speed 
        else:
            x = -50
            self.speed = self.game.s.extra_speed
        
        self.rect = self.image.get_rect(topleft = (x, 60))

        self.execute = True
                    
    def update(self):
        if self.execute:
           
            self.current_sprite += 0.2
            if self.current_sprite >= len (self.sprites):
                 self.current_sprite = 0
                                                          
            self.image = self.sprites[int(self.current_sprite)]
            self.rect.x += self.speed
            if self.side == 'right':
                if self.rect.x < -(self.x_pos):
                    self.kill()
            else:
                if self.rect.x > self.game.s.screen_width + self.x_pos:
                    self.kill()
            

class Boss(Sprite):
    """ Boss alien ship class"""
    
    def __init__(self, game):
        super().__init__()
        self.game = game
        self.sprites = []
        self.sprites.append(pygame.image.load(self.game.resource_path('assets/graphics/boss_earth/sprite_0.png')).convert_alpha())
        self.sprites.append(pygame.image.load(self.game.resource_path('assets/graphics/boss_earth/sprite_1.png')).convert_alpha())
        self.sprites.append(pygame.image.load(self.game.resource_path('assets/graphics/boss_earth/sprite_2.png')).convert_alpha())
        self.sprites.append(pygame.image.load(self.game.resource_path('assets/graphics/boss_earth/sprite_3.png')).convert_alpha())
        self.sprites.append(pygame.image.load(self.game.resource_path('assets/graphics/boss_earth/sprite_4.png')).convert_alpha())
        self.sprites.append(pygame.image.load(self.game.resource_path('assets/graphics/boss_earth/sprite_5.png')).convert_alpha())

    
        self.current_sprite = 0
        self.image = self.sprites[self.current_sprite]
              
        self.x_pos = self.image.get_width()
        self.y_pos = self.image.get_height()   
        
        self.rect = self.image.get_rect(center = (self.game.s.screen_width / 2, -100))
        self.game.s.boss_speed = 5
        self.game.s.boss_direction = 1
        #self.execute = False
        
    def initial_animation(self):
        if not self.game.s.executed_boss_animation:
            self.rect.y += 3
            if self.rect.y >= 100:
                self.game.s.executed_boss_animation = True
                pygame.mixer_music.load(self.game.resource_path('assets/audio/battle_boss.mp3'))
                pygame.mixer_music.play()
                self.game.s.start_boss_update = True

    
    def move_down(self):
        self.rect.y += 20
        self.game.s.boss_direction *= -1
        self.game.s.boss_speed += 0.6
    
    def update(self):
        self.initial_animation()
        if self.game.s.start_boss_update: 
            
            self.current_sprite += 0.2
            if self.current_sprite >= len (self.sprites):
                    self.current_sprite = 0
                                                            
            self.image = self.sprites[int(self.current_sprite)]
            self.rect.x += self.game.s.boss_speed * self.game.s.boss_direction
            if self.rect.x > self.game.s.screen_width - self.x_pos or self.rect.x < 0:
                self.move_down()
            
        
        
    
        
