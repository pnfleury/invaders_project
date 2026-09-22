import pygame
from pygame.sprite import Sprite
from settings import Settings


class Player (Sprite):
    """ Player ship class """

    def __init__(self, invaders_game):
        super().__init__()
        self.settings = Settings()
        self.screen = invaders_game.screen
        self.screen_rect = invaders_game.screen_rect
        self.image = pygame.image.load('graphics/player.png')
        self.x_pos = self.image.get_width()
        self.y_pos = self.settings.screen_heigth - self.image.get_height()
        self.rect = self.image.get_rect(midleft = (self.x_pos , self.y_pos))
            
    def get_input(self):
        
        keys = pygame.key.get_pressed() 
        if keys[pygame.K_RIGHT] and self.rect.right < self.screen_rect.right:
            self.rect.x += self.settings.player_speed
        elif keys[pygame.K_LEFT] and self.rect.left > self.screen_rect.left:
            self.rect.x -= self.settings.player_speed
            
    def restart_player_location (self):
        self.rect = self.image.get_rect(midleft = (self.x_pos , self.y_pos))
    
    def update (self):
        self.get_input()
           


