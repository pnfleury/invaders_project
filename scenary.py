import pygame
from pygame.sprite import Sprite
from random import randint

class Block(Sprite):
    """ Shields player class """

    def __init__(self, size, color, x, y):
        super().__init__()
        
        self.image = pygame.Surface((size, size))
        self.image.fill(color)
        self.rect = self.image.get_rect(topleft = (x,y))
        
             
            

shape = [
'   xxxxx',         #5
'  xxxxxxx',        #7
' xxxxxxxxx',       #9
'xxxxxxxxxxx',      #11
'xxxxxxxxxxx',      #11
'xxxxxxxxxxx',      #11
'xxx     xxx',      #6
'xx       xx']      #4


class Stars(Sprite):
    def __init__(self, color, x, y, game):
        super().__init__()
        self.game = game
        
        self.radius = randint(1, 3)
        self.diameter = self.radius * 2
        
        self.image = pygame.Surface((self.diameter, self.diameter), pygame.SRCALPHA)
        pygame.draw.circle(self.image, color, (self.radius, self.radius), self.radius)
        
        self.rect = self.image.get_rect(center = (x,y))
        self.speed = 1

        
    def update(self):
        
        if self.game.s.moving_stars:
            self.speed =  6
        else: self.speed =  1 

        self.rect.y +=  self.speed
        if self.rect.y > self.game.s.screen_heigth:
            self.rect.y = 0


class Planet(Sprite):
    def __init__(self, game):
        super().__init__()
        self.game = game
        self.list = []
        self.list.append(pygame.image.load(self.game.resource_path('assets/graphics/planets/earth.png')).convert_alpha())
        self.list.append(pygame.image.load(self.game.resource_path('assets/graphics/planets/moon.png')).convert_alpha())
        self.list.append(pygame.image.load(self.game.resource_path('assets/graphics/planets/mars.png')).convert_alpha())
        self.list.append(pygame.image.load(self.game.resource_path('assets/graphics/planets/jupiter.png')).convert_alpha())
        self.list.append(pygame.image.load(self.game.resource_path('assets/graphics/planets/saturn.png')).convert_alpha())
        self.list.append(pygame.image.load(self.game.resource_path('assets/graphics/planets/uranus.png')).convert_alpha())
        self.list.append(pygame.image.load(self.game.resource_path('assets/graphics/planets/netuno.png')).convert_alpha())
        self.current_planet = 0
        self.image = self.list[self.current_planet]
        self.image_height = self.image.get_height()
        self.rect = self.image.get_rect(topleft = (0, 800))

        self.execute_show_planet = True
        self.execute_hide_planet = False
        self.divisor = 3

    def show_planet(self):
            self.rect.y -= 2
            if self.image == self.list[5]: 
                self.divisor = 7 
            if self.image != self.list[5]:
                self.divisor = 3 
            if self.rect.y <= self.game.s.screen_heigth / self.divisor: 
                self.game.s.moving_stars = False
                self.game.level_up_active = True
                self.game.describe_planet()
                self.game.create_multiple_obstacles()
                self.game.block_rebuild = True   
                self.execute_show_planet = False
               
    def hide_planet(self):
        self.game.s.moving_stars = True
        self.rect.y +=  3
        if self.rect.y > self.game.s.screen_heigth:
            self.rect.y == self.game.s.screen_heigth
            self.execute_hide_planet = False


    def update(self): 
        # Show planet
        if self.execute_show_planet:
            self.show_planet()
        
        # Hide planet
        if self.execute_hide_planet:
            self.game.extra.empty()
            self.game.extra_alien_sound.stop()
            self.hide_planet()
           
                
                                                 
        





                
             
                

    