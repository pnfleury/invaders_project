import pygame
from pygame.sprite import Sprite
from settings import Settings


class Player (Sprite):
    """ Player ship class """

    def __init__(self, game):
        super().__init__()
        self.settings = Settings()
        self.game = game
        #self.screen = invaders_game.screen
        self.screen_rect = game.screen_rect
        self.image = pygame.image.load('assets/graphics/player.png')
        self.x_pos = self.image.get_width()
        self.y_pos = self.settings.screen_heigth - self.image.get_height()
        self.rect = self.image.get_rect(midleft = (self.x_pos , self.y_pos))
        self.speed_up = 1
            
    def get_input(self):
        
        keys = pygame.key.get_pressed() 
        if keys[pygame.K_RIGHT] and self.rect.right < self.screen_rect.right:
            self.rect.x += self.settings.player_speed
        elif keys[pygame.K_LEFT] and self.rect.left > self.screen_rect.left:
            self.rect.x -= self.settings.player_speed
            
    def restart_player_location (self):
        self.rect = self.image.get_rect(midleft = (self.x_pos , self.y_pos))

    def move_up (self):
        self.rect.y -= 1 * self.speed_up
        self.speed_up += 0.1
        if self.rect.y < 0:
            self.game.player.empty()
            Settings.ship_up = False
             
    def update (self):
        if self.settings.ship_up:
            self.move_up()
        else:
            self.get_input()
        
        
           


