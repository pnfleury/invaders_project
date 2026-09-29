import pygame
from random import randint


class Settings:
    """ Global game settings class"""
    
    def __init__(self):
   
        # Screen resolution
        self.flags = pygame.SCALED | pygame.FULLSCREEN
        self.screen_width = 1200
        self.screen_heigth = 800

        self.game_paused = False
        
        # end_game bonus
        self.bonus = 100000
        
        # Font coloer
        self.text_col = ('white') 
        
        # Initialize score and hiscore variables
        self.hiscore_file = "hiscore.pkl"
        self.current_hiscore = {}
        self.new_hiscore = {}
        self.name = 'INV'
        self.hi_score = 0
            
        # Initialize stars variables
        self.x = self.y = 0
        self.num_stars = 200 # numbers of stars on screen

        # flag for move ship up if beat game       
        self.ship_up = False

        # Obstacle setup
        self.block_size = 6
        self.obstacle_amount = 4
        self.obstacle_color = ('#FF5F1F') 
        self.obstacle_x_start = int(self.screen_width / 12)
        self.obstacle_y_start = self.screen_heigth - 140
        # Calculate obstacles positions on screen and put in a list
        self.obstacle_x_positions = []
        for num in range(self.obstacle_amount):
           self.obstacle_x_positions.append(num * (self.screen_width / self.obstacle_amount))
        

        # Player settings
        self.player_speed = 5
        self.laser_speed = 15
    
        # Aliens settings
        self.alien_laser_y = 15
        self.alien_direction = 1
        self.alien_distance = 16 # distance that a line of aliens descends 
        #self.alien_time_between_bullets = 900
        self.alien_rows = 5 #5
        self.alien_cols = 11 #11
        self.alien_x_distance = 70 #60
        self.alien_y_distance = 48 
        self.aliens_x_offset = 70 
        self.aliens_y_offset = 100
    
   
        # Extra alien settings
        self.EXTRALASER = pygame.USEREVENT + 1
        self.range_a = 800
        self.range_b = 1600
        self.extra_spawn_time = randint (self.range_a, self.range_b)
        self.extra_speed = 3
        self.extra_list_points = [100, 200, 500, 800, 1000]
        self.extra_point = 0

        
        self.initialize_dynamic_settings()
        
   
    def initialize_dynamic_settings(self):
        
        # Initialize level and lives variables
        self.level = 0 
        self.lives = 2
        self.score = 0
        # player ship
        self.shoots_allowed = 1
        # alien fleet
        self.alien_speed = 1.3
        self.alien_bullets_allowed = 1
        self.alien_speedup_scale = 1.04
        self.alien_laser_speed = 5
        # extra alien settings
        pygame.time.set_timer(self.EXTRALASER, 800)
        self.activate_extra_shot = False
        self.extra_bullets_allowed = 1
        self.extra_laser_speed = 4

        # flag for moving start or not
        self.moving_stars = False
        # flag for colors stars on title menu
        self.menu_stars = True
        # create a list for explosions time
        self.active_explosions = []   
        # Flags for the new_life function on the main program
        self.executed = False
        self.executed_2 = False
        self.executed_3 = False
        self.executed_4 = False
        self.activate_bonus = False
        self.executed_bonus = False
   