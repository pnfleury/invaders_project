import pygame
from random import randint


class Settings:
    """ Global game settings class"""

    
    # Screen resolution
    flags = pygame.SCALED | pygame.FULLSCREEN
    screen_width = 1200
    screen_heigth = 800

    game_paused = False
    
    # Font settings
    font_pixeled = 'font/Pixeled.ttf'
    font_wonder = 'font/8-BIT WONDER.ttf'
    text_col = ('white') # font color
    
   
    # Initialize score and hiscore variables
    hiscore_file = "hiscore.pkl"
    current_hiscore = {}
    new_hiscore = {}
    name = 'INV'
    score = 0
    hi_score = 0

    # Initialize level and lives variables
    level = 0 
    lives = 2
    
    # Flags for the new_life function on the main program
    executed = False
    executed_2 = False
    executed_3 = False
    executed_4 = False

    # Initialize stars variables
    x = y = 0
    num_stars = 200 # numbers of stars on screen
    moving_stars = True # flag for moving start or not

    menu_stars = False

    ship_up = False

    # Obstacle setup
    block_size = 6
    obstacle_amount = 4
    obstacle_color = ('#FF5F1F') 
    obstacle_x_start = int(screen_width / 12)
    obstacle_y_start = screen_heigth - 140
    # Calculate obstacles positions on screen and put in a list
    obstacle_x_positions = []
    for num in range(obstacle_amount):
        obstacle_x_positions.append(num * (screen_width / obstacle_amount))
        

    # Player settings
    player_speed = 5
    shoots_allowed = 1
    laser_speed = 15
   
    
    # Aliens settings
    alien_speed = 1.3
    alien_bullets_allowed = 1
    alien_direction = 1
    alien_distance = 16 # distance that a line of aliens descends 
    alien_speedup_scale = 1.04
    alien_time_between_bullets = 900
    alien_rows = 5 #5
    alien_cols = 11 #11
    alien_x_distance = 70 #60
    alien_y_distance = 48 
    aliens_x_offset = 70 
    aliens_y_offset = 100
    
    # Aliens lasers settings
    alien_laser_speed = 5
    alien_laser_y = 15
   
    # Extra alien settings
    range_a = 800
    range_b = 1600
    extra_spawn_time = randint (range_a, range_b)
    extra_speed = 3
    extra_list_points = [100, 200, 500, 800, 1000]
    extra_point = 0

   # create a list for explosions time
    active_explosions = []   

   
    

    