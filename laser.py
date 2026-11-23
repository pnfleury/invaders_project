import pygame
from pygame.sprite import Sprite

class Laser(Sprite):
    """ Ship laser class """

    def __init__(self, pos, game):
        super().__init__()
        self.game = game
        self.image = pygame.Surface((1,9))
        self.image.fill('white')
        self.rect = self.image.get_rect(center = pos)
        self.y = float(self.rect.y)
    
    def update(self):
        self.y -= self.game.s.laser_speed
        self.rect.y = self.y
        if self.rect.y <= (80 * 0.6):
            self.game.s.active_explosions.append({"pos" : (self.rect.x, self.rect.y), "time" : 100, "hit" : "laser_miss"})
            self.kill()
           
            
    
    