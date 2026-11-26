import pygame
from pygame.sprite import Sprite

class Alien(Sprite):
    """ Alien class """
    
    def __init__(self, color, x, y, game):
        super().__init__()
        
        self.game = game
        file_path = 'assets/graphics/' + color +'/sprite_0.png'
        self.sprites = []
        self.value = 0
        self.sprites.append(pygame.image.load(self.game.resource_path(file_path)).convert_alpha())

        if color == 'red': 
            self.sprites.append(pygame.image.load(self.game.resource_path('assets/graphics/red/sprite_1.png')).convert_alpha())
            self.sprites.append(pygame.image.load(self.game.resource_path('assets/graphics/red/sprite_2.png')).convert_alpha())
            self.sprites.append(pygame.image.load(self.game.resource_path('assets/graphics/red/sprite_3.png')).convert_alpha())
            self.sprites.append(pygame.image.load(self.game.resource_path('assets/graphics/red/sprite_4.png')).convert_alpha())
            self.value = 100
        elif color == "green": 
            self.sprites.append(pygame.image.load(self.game.resource_path('assets/graphics/green/sprite_1.png')).convert_alpha())
            self.sprites.append(pygame.image.load(self.game.resource_path('assets/graphics/green/sprite_2.png')).convert_alpha())
            self.value = 200
        elif color == "silver": 
            self.sprites.append(pygame.image.load(self.game.resource_path('assets/graphics/silver/sprite_1.png')).convert_alpha())
            self.sprites.append(pygame.image.load(self.game.resource_path('assets/graphics/silver/sprite_2.png')).convert_alpha())
            self.sprites.append(pygame.image.load(self.game.resource_path('assets/graphics/silver/sprite_3.png')).convert_alpha())
            self.sprites.append(pygame.image.load(self.game.resource_path('assets/graphics/silver/sprite_4.png')).convert_alpha())
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
        self.sprites.append(pygame.image.load(self.game.resource_path('assets/graphics/alien_extra/sprite_0.png')).convert_alpha())
        self.sprites.append(pygame.image.load(self.game.resource_path('assets/graphics/alien_extra/sprite_1.png')).convert_alpha())
        self.sprites.append(pygame.image.load(self.game.resource_path('assets/graphics/alien_extra/sprite_2.png')).convert_alpha())
        self.sprites.append(pygame.image.load(self.game.resource_path('assets/graphics/alien_extra/sprite_3.png')).convert_alpha())
        self.sprites.append(pygame.image.load(self.game.resource_path('assets/graphics/alien_extra/sprite_4.png')).convert_alpha())
       
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
        
        self.rect = self.image.get_rect(topleft = (x, 36))
        self.x = float(self.rect.x)

        self.execute = True
                    
    def update(self):
        if self.execute:
           
            self.current_sprite += 0.2
            if self.current_sprite >= len (self.sprites):
                 self.current_sprite = 0
                                                          
            self.image = self.sprites[int(self.current_sprite)]
            self.x += self.speed
            self.rect.x = self.x
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
        self.sprites.append(pygame.transform.scale_by(self.game.extra_sprite.sprites[0], 3.0))
        self.sprites.append(pygame.transform.scale_by(self.game.extra_sprite.sprites[1], 3.0))
        self.sprites.append(pygame.transform.scale_by(self.game.extra_sprite.sprites[2], 3.0))
        self.sprites.append(pygame.transform.scale_by(self.game.extra_sprite.sprites[3], 3.0))
        self.sprites.append(pygame.transform.scale_by(self.game.extra_sprite.sprites[4], 3.0))
       
        self.current_sprite = 0
        self.image = self.sprites[self.current_sprite]
              
        self.x_pos = self.image.get_width()
        self.y_pos = self.image.get_height()   
        
        self.rect = self.image.get_rect(center = (self.game.s.screen_width / 2, - 60))
        
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)
        

    def initial_animation(self):
        if not self.game.s.executed_boss_animation:
            self.y += 3
            self.rect.y = self.y
            if self.rect.y >= 60:
                self.game.s.executed_boss_animation = True
                self.game.boss_music.play()
                self.game.s.start_boss_update = True

    
    def move_down(self):
        self.y += 12
        self.rect.y = self.y
        self.game.s.boss_direction *= -1
        self.game.s.boss_speed += self.game.s.boss_speedup_scale
    
    def update(self):
        self.initial_animation()
        if self.game.s.start_boss_update: 
            
            self.current_sprite += 0.2
            if self.current_sprite >= len (self.sprites):
                    self.current_sprite = 0
                                                            
            self.image = self.sprites[int(self.current_sprite)]
            self.x += self.game.s.boss_speed * self.game.s.boss_direction
            self.rect.x = self.x
            if self.rect.x > self.game.s.screen_width - self.x_pos or self.rect.x <= 0:
                self.move_down()
            
        
        
    
        
