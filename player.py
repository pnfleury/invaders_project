import pygame
from pygame.sprite import Sprite

class Player (Sprite):
    """ Player ship class """

    def __init__(self, game):
        super().__init__()
        self.game = game
        self.player_sprites =  []
        self.player_sprites.append (pygame.image.load(self.game.resource_path('assets/graphics/player.png')).convert_alpha())
        self.player_sprites.append (pygame.image.load(self.game.resource_path('assets/graphics/ship_ciano/sprite_0.png')).convert_alpha())
        self.player_sprites.append (pygame.image.load(self.game.resource_path('assets/graphics/ship_ciano/sprite_1.png')).convert_alpha())
        self.player_sprites.append (pygame.image.load(self.game.resource_path('assets/graphics/ship_ciano/sprite_2.png')).convert_alpha())
        self.current_sprite = 0
        self.image = self.player_sprites[self.current_sprite]
        
        self.x_pos = self.image.get_width()
        self.y_pos = self.game.s.screen_heigth - self.image.get_height() - 15
        self.rect = self.image.get_rect(midleft = (self.x_pos , self.y_pos))
        self.speed_up = 1
        self.block_input = False
        #self.executed_thruster_on = False
       
            
    def get_input(self):
        if not self.block_input:
            keys = pygame.key.get_pressed() 
            if keys[pygame.K_RIGHT] and self.rect.right < self.game.screen_rect.right:
                self.rect.x += self.game.s.player_speed
            elif keys[pygame.K_LEFT] and self.rect.left > self.game.screen_rect.left:
                self.rect.x -= self.game.s.player_speed
            
    def restart_player_location (self):
        self.rect = self.image.get_rect(midleft = (self.x_pos , self.y_pos))
    
    def last_thrust (self):
        self.current_sprite += 0.5
        if self.current_sprite >= len (self.player_sprites):
            self.current_sprite = 0
        self.image = self.player_sprites[int(self.current_sprite)]
        self.rect.y -= 1 * self.speed_up
        self.speed_up += 0.1
        if self.rect.y < 0:
            self.game.player.empty()
            self.game.s.ship_last_thrust = False
                     
         
    def thruster_on(self): 
        if self.game.i == 0:
            time = 8
        else: time = 15
        self.current_sprite += 0.5
        if self.current_sprite >= len (self.player_sprites):
            self.current_sprite = 0
        self.image = self.player_sprites[int(self.current_sprite)]
        if self.game.ship_boost_time (time, True):
            self.game.s.ship_thruster_on = False
            self.game.ship_thruster_sound.stop()
            self.image = self.player_sprites[0]

    def update (self):
        self.get_input()
            
        if self.game.s.ship_thruster_on:
            self.thruster_on()
        
        if self.game.s.ship_last_thrust:
            self.block_input = True
            self.last_thrust()
      
           
       
            
        
            
           

            