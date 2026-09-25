import pygame
from pygame.sprite import Sprite
from random import randint
from settings import Settings

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
    def __init__(self, color, x, y):
        super().__init__()
        
        self.settings = Settings
        self.x = randint (1,4)
        self.image = pygame.surface.Surface((self.x, self.x))
        self.image.fill(color)
        self.rect = self.image.get_rect(center = (x,y))

    def update(self):
        if self.settings.menu_stars:
            self.red = randint(0, 255)
            self.green = randint(0, 255)
            self.blue = randint(0, 255)
            self.image.fill((self.red, self.green, self.blue))
            self.rect.y -=  1
            if self.rect.y < 0:
                self.rect.y = self.settings.screen_heigth

        else:
            self.color = randint(0 ,255)
            self.image.fill((self.color, self.color, self.color))   
            if self.settings.moving_stars:
                self.rect.y +=  6
                if self.rect.y > self.settings.screen_heigth:
                    self.rect.y = 0
        

class Planet(Sprite):
    def __init__(self, game):
        super().__init__()
        self.settings = Settings()
        self.game = game
        self.list = []
        self.list.append(pygame.image.load('assets/graphics/planets/earth.png').convert_alpha())
        self.list.append(pygame.image.load('assets/graphics/planets/moon.png').convert_alpha())
        self.list.append(pygame.image.load('assets/graphics/planets/mars.png').convert_alpha())
        self.list.append(pygame.image.load('assets/graphics/planets/jupiter.png').convert_alpha())
        self.list.append(pygame.image.load('assets/graphics/planets/saturn.png').convert_alpha())
        self.list.append(pygame.image.load('assets/graphics/planets/uranus.png').convert_alpha())
        self.list.append(pygame.image.load('assets/graphics/planets/netuno.png').convert_alpha())
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
            if self.rect.y <= self.settings.screen_heigth / self.divisor: 
                
                self.execute_show_planet = False
            
               
    def hide_planet(self):
        self.rect.y +=  3
        if self.rect.y > self.settings.screen_heigth:
            self.rect.y == self.settings.screen_heigth
            self.execute_hide_planet = False


    def update(self): 
        # Show planet
        if self.execute_show_planet:
            self.show_planet()
        
        # Hide planet
        if self.execute_hide_planet:
            self.hide_planet()
           
                
                                                 
        





                
             
                

    