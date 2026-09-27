import pygame
from pygame.sprite import Sprite

class Laser(Sprite):
    """ Ship laser class """

    def __init__(self, pos, game):
        super().__init__()
        self.game = game
        self.image = pygame.Surface((2,15))
        self.image.fill('white')
        self.rect = self.image.get_rect(center = pos)
     
    def update(self):
        self.rect.y -= self.game.s.laser_speed
        if self.rect.y <= 75:
            self.game.s.active_explosions.append({"pos" : (self.rect.x, self.rect.y), "time" : 100, "hit" : "laser_miss"})
            self.kill()
           
            
    
    