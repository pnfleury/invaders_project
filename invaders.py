import pygame,sys, os, pickle
from random import choice, randint
from player import Player
from crt import CRT
from settings import Settings
from alien import Alien, Extra
from alien_laser import AlienLaser
from laser import Laser
from menu import *
import scenary
from scenary import Planet

class Game (Settings):
    """ Principal class of Invader-X game"""
    def __init__(self):
        
        # initialize screen
        self.screen =  pygame.display.set_mode((self.screen_width, self.screen_heigth), self.flags)
        self.screen_rect = self.screen.get_rect()

        # Lifes indicator on top right screen
        self.life_surf_original = pygame.image.load('graphics/player.png').convert_alpha()
        self.life_surf = pygame.transform.scale_by(self.life_surf_original, 0.6)
        self.live_x_start_pos = self.screen_width - (self.life_surf.get_size()[0] * 2.3 + 65)
        self.life_x = self.live_x_start_pos + ((self.life_surf.get_size()[0]))  

        # Load explosions images
        self.explosion_alien = pygame.image.load('graphics/alien_explosion.png').convert_alpha() 
        self.explosion_extra = pygame.image.load('graphics/extra_explosion.png').convert_alpha()
        self.laser_hit = pygame.image.load('graphics/laser_hit.png').convert_alpha()
        self.explosion_player = pygame.image.load('graphics/player_explosion.png').convert_alpha()
        self.block_hit = pygame.image.load('graphics/block_hit.png').convert_alpha()
        self.laser_miss = pygame.image.load('graphics/laser_miss.png').convert_alpha()
        self.pause_menu = pygame.image.load('graphics/pause_menu.png').convert_alpha()
        self.pause_menu_rect = self.pause_menu.get_rect(center = (self.screen_width /2, self.screen_heigth / 2))

        
       
        # Create Font objects from files
        self.font_text = pygame.font.Font(self.font_pixeled, 15)
        self.font_title_2 = pygame.font.Font('font/Pixeled.ttf', 40)
        self.font_scoreboard = pygame.font.Font('font/Pixeled.ttf', 15)
        self.font_extra_points = pygame.font.Font('font/8-BIT WONDER.ttf', 20)
        self.font_finish = pygame.font.Font('font/Pixeled.ttf', 25) 
        self.font_planets = pygame.font.Font('font/8-BIT WONDER.ttf', 40)
        self.font_title = pygame.font.Font(self.font_pixeled, 80)
        self.font_score = pygame.font.Font('font/Pixeled.ttf', 25) 
        self.font_wonder = pygame.font.Font('font/8-BIT WONDER.ttf', 35)
        
    
        # Load sounds files
        self.music = pygame.mixer.Sound('audio/music.wav')
        self.laser_sound = pygame.mixer.Sound('audio/shoot.wav')
        self.alien_laser_sound = pygame.mixer.Sound('audio/laser.wav')
        self.extra_alien_sound = pygame.mixer.Sound('audio/ufo_lowpitch.wav')
        self.new_life_sound = pygame.mixer.Sound('audio/life.mp3')
        self.explosion_sound = pygame.mixer.Sound('audio/explosion.wav')
        self.player_explosion_sound = pygame.mixer.Sound('audio/player_explosion.wav')
        self.extra_explosion_sound = pygame.mixer.Sound('audio/ufo_highpitch.wav')
        self.block_rebuild_sound = pygame.mixer.Sound('audio/block_rebuild.wav')
        self.warp_sound = pygame.mixer.Sound('audio/warp.mp3')
        self.warp_exit_sound = pygame.mixer.Sound('audio/warp_exit.mp3')

        # Set volume
        self.music.set_volume(0.1)
        self.laser_sound.set_volume(0.2)
        self.alien_laser_sound.set_volume(0.2)
        self.extra_alien_sound.set_volume(0.2)
        self.new_life_sound.set_volume(0.3)
        self.explosion_sound.set_volume(0.2)
        self.player_explosion_sound.set_volume(0.2)
        self.extra_explosion_sound.set_volume(0.2)
        self.block_rebuild_sound.set_volume(0.2)
        self.warp_sound.set_volume(0.2)
        self.warp_exit_sound.set_volume(0.2)
        #self.music.play(loops= -1)


        # Create sprite instances and sprite groups
        self.crt = CRT(self)

        self.main_menu = Menu(self)
        self.game_over_menu = GameOver(self)
        self.hiscore_menu = Hiscore(self)
        self.beatgame_menu = BeatGame(self)
        self.planet = Planet(self)
        self.alien = Alien('red',0,0)
        self.extra_sprite = Extra('left')
        self.shape = scenary.shape
        self.player_sprite = Player(self)
        
        self.planets = pygame.sprite.Group(self.planet)
        self.player = pygame.sprite.GroupSingle(self.player_sprite)
        self.extra = pygame.sprite.GroupSingle()
        self.aliens = pygame.sprite.Group()
        self.blocks = pygame.sprite.Group()
        self.alien_lasers = pygame.sprite.Group()
        self.lasers = pygame.sprite.Group()
        self.stars = pygame.sprite.Group()

        

        """ initialize variables """
        # Menu inicial
        self.curr_menu = self.main_menu

        # flag for level up fucntion
        self.level_up_active = False  

        ## PAUSE FUNCTION
        # time variable for pause function 
        self.time =  10
        # initial time variable for pause function 
        self.initial_time = 0
        # flag variable for pause function
        self.start = False

        # OBSTACLE 
        # flag variable for create obstacles blocks
        self.create_obstacle_flag = True
        # flag variable for rebuild obstacles blocks
        self.block_rebuild = False
        # increment variable used on redraw blocks function
        self.block_count = 0

        # Flag for start/stop initial planet animation
        self.finish_initial_planet_animation = False

        # Flag for start/stop planet animation
        self.finish_planet_animation = False
        
        # variable used on leave_planet_animation function
        self.i = 0
        # Flag for start the game
        self.running = True
        # Flag for start/ stop the game_loop function
        self.playing = False
        # explosion time function variable
        self.dt = 0   

        # Call functions for create stars
        self.create_stars(self.x, self.y)

        
     
    """ GAME FUNCTIONS """

    def create_stars(self, x, y):

        for value in range(self.num_stars):
            rand_x = randint(0, self.screen_width)
            rand_y =  randint (0, self.screen_heigth)
            if x == rand_x:
                rand_x = randint(0, self.screen_width)
            if y == rand_y:
                rand_y = randint(0, self.screen_heigth)
            x = rand_x
            y = rand_y
            self.star_sprite = scenary.Stars('white', x, y)
            self.stars.add(self.star_sprite)



    def create_obstacle(self, offset_x):
        """Create obstacles sprites (player shields) 
        Parameters: 
        offset_x (int): space between obstacles 
        """
        for row_index, row in enumerate(self.shape):
            for col_index, col in enumerate(row):
                if col == 'x':
                    x = self.obstacle_x_start + col_index * self.block_size + offset_x
                    y = self.obstacle_y_start + row_index * self.block_size        
                    self.block = scenary.Block(self.block_size, self.obstacle_color, x, y)

                    self.blocks.add(self.block)
        

   
    def create_multiple_obstacles(self):
        """Create multiples obstacles defined on obstacle_x_positions list"""
        for offset_x in self.obstacle_x_positions:
            self.create_obstacle(offset_x)
                        
    
    def alien_setup(self):
        """Create the aliens fleet"""
        for row_index, row in enumerate(range(self.alien_rows)):
            for col_index, col in enumerate(range(self.alien_cols)):
                x = col_index * self.alien_x_distance + self.aliens_x_offset
                y = row_index * self.alien_y_distance + self.aliens_y_offset
                
                if row_index == 0: alien_sprite = Alien('yellow', x, y)
                elif 1 <= row_index <=2: alien_sprite = Alien('green', x, y)
                else: alien_sprite = Alien('red', x, y)
                self.aliens.add(alien_sprite)    
           
    def alien_position_checker(self):
        """Check if the alien fleet had reach the side edge of the screen"""
        for alien in self.aliens:
            if alien.rect.right >= self.screen_width or alien.rect.left <= 0:
                self.alien_move_down()
                break

    def alien_move_down(self):
        """Move down the alien fleet when they reach the side edge of screen
        and force to the oposite direction"""
        if self.aliens:
            for alien in self.aliens:
                alien.rect.y += self.alien_distance
            lowest_alien_sprite = max (self.aliens, key=lambda a: a.rect.bottom)
            pos_y = lowest_alien_sprite.rect.bottom
            
            if pos_y >= self.screen_heigth :
                self.player_explosion_sound.play()
                self.lives = 0
                self.active_explosions.append({"pos" : (self.player_sprite.rect.x, self.player_sprite.rect.y), "time" : 800, "hit" : "fleet_bottom"})
                
            else: self.alien_direction *= -1 
               
    
    def alien_shoot(self):
        """ Create the aliens shoot"""
        if self.aliens:
            random_alien = choice(self.aliens.sprites())
            if len (self.alien_lasers) < self.alien_bullets_allowed:
                laser_sprite = AlienLaser (random_alien.rect.midbottom)
                self.alien_lasers.add(laser_sprite)

    def extra_alien_timer (self):
        """Spawns an extra alien as soon as the cooldown ends"""
        if self.extra_sprite.execute == True:
            self.extra_spawn_time -= 1
            if self.extra_spawn_time <= 0:
                self.extra.add(Extra(choice(['right','left'])))
                self.extra_alien_sound.play()
                self.extra_spawn_time = randint (self.range_a, self.range_b)  


    def explosion_time(self):   
        """Duration of the explosions shown on the screen"""     
        for exp in self.active_explosions[:]:  
            exp["time"] -= self.dt
            if exp["time"] <= 0:
                self.active_explosions.remove(exp)


    def draw_explosion(self):
        """Draws images of the explosions on the screen if there are any in the list"""
        for exp in self.active_explosions:
            match exp['hit']:
                case 'extra_explosion':
                    self.screen.blit(self.explosion_extra,  exp["pos"])
                case 'extra':
                    self.draw_text(f"{exp['points']}", self.font_scoreboard, 'red', exp['pos'][0] + 25, exp['pos'][1] + 25)
                case 'laser':
                    self.screen.blit(self.laser_hit, exp["pos"])
                case 'alien':
                    self.screen.blit(self.explosion_alien, exp["pos"])
                case 'player':
                    self.screen.blit(self.explosion_player, exp["pos"])
                    self.lasers.empty()
                    if exp["time"] <= 90:
                        self.player.add(self.player_sprite)
                        self.player_sprite.restart_player_location()
                case 'block':
                    self.screen.blit(self.block_hit, exp["pos"])
                case 'laser_miss':
                    self.screen.blit(self.laser_miss, exp["pos"])
                case 'fleet_bottom':
                    self.screen.blit(self.explosion_player, exp["pos"])
                    self.active_explosions.append({"time" : 8000, "hit" : "game_over"})            

                case 'earth':
                    self.draw_text(f'DEFEND EARTH', self.font_planets, '#E1E6E7', exp['pos'][0], exp['pos'][1])
                case 'moon':
                    self.draw_text(f'DEFEND MOON', self.font_planets, '#E1E6E7', exp['pos'][0], exp['pos'][1])
                case 'mars':
                    self.draw_text(f'DEFEND MARS', self.font_planets, '#E1E6E7', exp['pos'][0], exp['pos'][1])
                case 'jupiter':
                    self.draw_text(f'DEFEND JUPITER', self.font_planets, '#E1E6E7', exp['pos'][0], exp['pos'][1])
                case 'saturn':
                    self.draw_text(f'DEFEND SATURN', self.font_planets, '#E1E6E7', exp['pos'][0], exp['pos'][1])
                case 'uranus':
                    self.draw_text(f'DEFEND URANUS', self.font_planets, '#E1E6E7', exp['pos'][0], exp['pos'][1])
                case 'netuno':
                    self.draw_text(f'DEFEND NEPTUNE', self.font_planets, '#E1E6E7', exp['pos'][0], exp['pos'][1])
                #case 'finished':
                    #self.curr_menu = self.beatgame_menu
                    #self.playing = False           
                       
    def collision_checks(self):
        """Check all the sprites collisons"""
        if self.player:
            for laser in self.lasers:
                # Obstacle 
                if pygame.sprite.spritecollide(laser, self.blocks, True):
                    laser.kill()
                                   
                # Alien 
                aliens_hit = pygame.sprite.spritecollide(laser, self.aliens, True)
                if aliens_hit:
                    for alien in aliens_hit:  
                        self.active_explosions.append({"pos" : (alien.rect.x, alien.rect.y), "time" : 100, "hit" : "alien"})                       
                        self.score += alien.value 
                    laser.kill()
                    self.alien_speed *= self.alien_speedup_scale
                    self.explosion_sound.play()
                
                # Extra alien
                extra_hit = pygame.sprite.spritecollide(laser, self.extra, True)
                if extra_hit:
                    for extra in extra_hit:
                        self.extra_point = choice (self.extra_list_points)
                        self.active_explosions.append({"pos" : (extra.rect.x, extra.rect.y), "time" : 300, "hit" : "extra_explosion"})
                        self.active_explosions.append({"pos" : (extra.rect.x, extra.rect.y), "time" : 1300, "hit" : "extra", "points" : self.extra_point})
                        self.extra_explosion_sound.play()
                        self.score += self.extra_point
                    laser.kill()
                     
                # Alien laser 
                laser_hit = pygame.sprite.spritecollide(laser, self.alien_lasers, True)
                if laser_hit:
                    self.active_explosions.append({"pos" : (laser.rect.x, laser.rect.y), "time" : 100, "hit" : "laser"})
                    laser.kill()

            
        """ Alien lasers collisions """
        if self.alien_lasers:
            for laser in self.alien_lasers:
                # Player 
                if pygame.sprite.spritecollide(laser, self.player, True):
                    self.player_explosion_sound.play()
                    self.lives -= 1
                    self.alien_lasers.empty()
                    self.active_explosions.append({"pos" : (self.player_sprite.rect.x, self.player_sprite.rect.y), "time" : 500, "hit" : "player"})
                    if self.lives < 0:
                        self.playing = False
                        self.curr_menu = self.game_over_menu
                        
                                                     
                # Blocks 
                if pygame.sprite.spritecollide (laser, self.blocks, True):

                    self.active_explosions.append({"pos" : (laser.rect.x, laser.rect.y), "time" : 500, "hit" : "block"})
                    laser.kill()
           

        """ Alien collisions """
        if self.aliens:
            for block in self.blocks:
                # Blocks
                block_hit = pygame.sprite.spritecollide(block, self.aliens, False)
                if block_hit:
                    self.active_explosions.append({"pos" : (block.rect.x, block.rect.y), "time" : 500, "hit" : "block"})
                    block.kill()

            # Player
            if pygame.sprite.groupcollide(self.player, self.aliens, True, True):
                self.player_explosion_sound.play()
                self.active_explosions.append({"pos" : (self.player_sprite.rect.x, self.player_sprite.rect.y), "time" : 800, "hit" : "fleet_bottom"})
            

    def display_lives(self):
        """Display the player life on screen"""
        self.draw_text(f'x {self.lives}', self.font_scoreboard, self.text_col, self.screen_width - 40, 20)
        self.screen.blit(self.life_surf, (self.life_x,15))

    def display_score(self):
        """Display the score on screen"""
        self.draw_text(f'SCORE: {self.score}', self.font_scoreboard, self.text_col, 20, 0, 'topleft')
      
    def display_hiscore(self): 
        """Display the hiscore on screen"""
        self.draw_text(f'HI-SCORE: {self.hi_score}', self.font_scoreboard, self.text_col, self.screen_rect.centerx, self.screen_rect.top + 20)
        if self.score > self.hi_score:
            self.hi_score = self.score
    
    def display_level(self):
        """Display the current level on screen"""
        if self.level > 0:
            self.draw_text(f'LEVEL: {self.level}', self.font_scoreboard, self.text_col, self.screen_width - 200, 20)

    def new_life(self):
        """Gives the player an extra life when they reach a certain score."""
        match self.score:
            case s if s >= 20000 and not self.executed:
                self.lives += 1
                self.new_life_sound.play()
                self.executed = True

            case s if s >= 50000 and not self.executed_2:
                self.lives += 1
                self.new_life_sound.play()
                self.executed_2 = True

            case s if s >= 80000 and not self.executed_3:
                self.lives += 1
                self.new_life_sound.play()
                self.executed_3 = True

            case s if s >= 100000 and not self.executed_4:
                self.lives += 1
                self.new_life_sound.play()
                self.executed_4 = True

    def pause_time(self, time, start):
        """ Take a pause before continuing
        Parameters:
        time (int) = pause time 
        start (boolean)= starts pause """
        if start:
            self.initial_time += 0.05
            if self.initial_time >= time:
                self.initial_time = 0
                return True


    def level_up (self):
        if self.level_up_active:
            if not self.aliens:
                if self.pause_time(8, True):
                    self.level +=1 
                    self.alien_setup()
                    self.restart_speed()
                    self.raise_difficulty()
                    self.alien_direction = 1

    def initial_planet_animation(self):
        if not self.finish_initial_planet_animation:
            if self.planet.execute_show_planet == False:
                Settings.moving_stars = False
                self.describe_planet()
                if self.create_obstacle_flag:
                    self.create_multiple_obstacles()
                    self.block_rebuild = True
                    self.create_obstacle_flag = False
                    self.level_up_active = True
                    self.finish_initial_planet_animation = True

          
    def planet_animation(self):
        if not self.finish_planet_animation:
            if self.level in (3, 6, 9, 12, 15, 18, 21) and not (self.aliens):
                self.level_up_active = False
                self.alien_lasers.empty()
                self.blocks.empty()
                #self.warp_sound.play()
                Settings.moving_stars = True
                self.planet.execute_hide_planet = True
                if self.pause_time(10, True):
                    if self.level == 21:
                        self.finish_planet_animation = True
                        self.extra.empty()
                        Settings.moving_stars = False
                        self.playing = False
                        self.curr_menu = self.beatgame_menu
                        
                        #self.finish_initial_planet_animation = False
                    else:
                        self.i += 1
                        self.planet.image = self.planet.list[self.i] 
                        self.finish_planet_animation = True
                        self.planet.execute_show_planet = True
                        self.create_obstacle_flag = True
                        self.finish_initial_planet_animation = False
                                        

    def redraw_blocks (self):
        if self.block_rebuild:
            self.block_rebuild_sound.play()   
            self.block_count += 0.1
            if self.block_count <= 4: 
                for dots in self.blocks:
                    self.color_red = randint(0 ,255)
                    self.color_green = randint(0 ,255)
                    self.color_blue = randint(0 ,255)
                    dots.image.fill ((self.color_red, self.color_green, self.color_blue)) 
            else:
                
                self.create_multiple_obstacles()
                self.block_count = 0
                self.block_rebuild = False            

    def reset_game(self):
        """Reset the game settings"""
        #self.active_explosions = []
        self.hiscore_menu.hiscore_initialize()
        self.aliens.empty()
        self.alien_lasers.empty()
        self.lasers.empty()
        self.blocks.empty()
        self.extra.empty()
        self.planets.empty()
        self.player.empty()
        self.planets.add(self.planet)
        self.player.add(self.player_sprite)
        self.planet.rect = self.planet.image.get_rect(topleft = (0, 800))
        self.i = 0 
        self.planet.image = self.planet.list[self.i]
        self.level_up_active = False
        self.planet.execute_show_planet = True
        self.finish_initial_planet_animation = False
        Settings.moving_stars = True
        self.create_obstacle_flag = True
        self.alien_bullets_allowed = 1
        self.shoots_allowed = 1
        self.alien_speedup_scale = 1.04
        self.lives = 2
        self.score = 0
        self.level = 0
        self.player_sprite.restart_player_location()
        # Default flags for the new_life function on the main program
        self.executed = False
        self.executed_2 = False
        self.executed_3 = False
        self.executed_4 = False
     

    def draw_text(self, text, font, text_col, x, y, pos = 'center'):
            """Draw text on screen
            Parameters:
            text (string) = text 
            font = font type
            text_col = font color
            x,y = width and heigh positon on screen"""
            img = font.render (text, False, text_col)
            img_rect = img.get_rect()
            if pos == 'topleft':
                img_rect.topleft = (x,y)
                self.screen.blit(img, img_rect)
            else:
                img_rect.center = (x,y)
                self.screen.blit(img, img_rect)
    
    def restart_speed(self):
        """ Restart speed of player and alien fleet speed"""
        self.alien_speed = 1.3

    def describe_planet(self):
        if self.planet.image == self.planet.list[0]:
            self.active_explosions.append({"pos" : (self.screen_rect.centerx, self.screen_rect.centery), "time" : 4000, "hit" : "earth"})
        elif self.planet.image == self.planet.list[1]:
            self.active_explosions.append({"pos" : (self.screen_rect.centerx, self.screen_rect.centery), "time" : 4000, "hit" : "moon"})
        elif self.planet.image == self.planet.list[2]:
                self.active_explosions.append({"pos" : (self.screen_rect.centerx, self.screen_rect.centery), "time" : 4000, "hit" : "mars"})
        elif self.planet.image == self.planet.list[3]:
            self.active_explosions.append({"pos" : (self.screen_rect.centerx, self.screen_rect.centery), "time" : 4000, "hit" : "jupiter"})
        elif self.planet.image == self.planet.list[4]:
            self.active_explosions.append({"pos" : (self.screen_rect.centerx, self.screen_rect.centery), "time" : 4000, "hit" : "saturn"})
        elif self.planet.image == self.planet.list[5]:
            self.active_explosions.append({"pos" : (self.screen_rect.centerx, self.screen_rect.centery), "time" : 4000, "hit" : "uranus"})
        elif self.planet.image == self.planet.list[6]:
            self.active_explosions.append({"pos" : (self.screen_rect.centerx, self.screen_rect.centery), "time" : 4000, "hit" : "netuno"})

     
    def raise_difficulty(self):
        """Increase the game's difficulty by raising the number of shots fired by the alien fleet
          as the level rises. Raise the number of player's shots starting on level 4 """
        if self.level in (1, 2):
            self.alien_bullets_allowed = 1
        elif self.level == 3:
            self.finish_planet_animation = False
            
        elif self.level in (4, 5):
            self.alien_bullets_allowed = 2
            self.shoots_allowed = 2
        elif self.level == 6:
            self.finish_planet_animation = False

        elif self.level in (7, 8):
            self.alien_bullets_allowed = 3
            self.shoots_allowed = 2
        elif self.level == 9:
            self.finish_planet_animation = False
           
        elif self.level in (10, 11):
            self.alien_bullets_allowed = 4
            self.shoots_allowed = 2
        elif self.level == 12:
            self.finish_planet_animation = False

        elif self.level in (13, 14):
            self.alien_bullets_allowed = 5
            self.shoots_allowed = 2
            self.alien_speed = 1.5    
        elif self.level == 15:
            self.finish_planet_animation = False

        elif self.level in (16, 17):
            self.alien_bullets_allowed = 6
            self.alien_speed = 1.7
            self.shoots_allowed = 3
        elif self.level == 18:
            self.finish_planet_animation = False
            
        elif self.level in (19, 20, 21):
            self.finish_planet_hide_animation = False
            self.alien_bullets_allowed = 6
            self.alien_speed = 1.9
            self.shoots_allowed = 3

        elif self.level == 22:
            self.finish_planet_hide_animation = False
            #self.save_hiscore()
            #self.extra.empty()
            #self.playing = False
            #self.curr_menu = self.beatgame_menu
              
          

    def choose_level(self):
        self.aliens.empty()
        self.alien_lasers.empty()
        self.extra.empty()
        self.alien_setup()
        self.restart_speed()
        self.level += 1
        self.raise_difficulty()

    def save_hiscore(self):
         # define a random key for the dictionary
        code = randint(1, 1000000)
        # if the dictionary key exists in loaded hiscore file get other random key 
        if str(code) in self.current_hiscore.keys():
            code = randint(1, 1000000)
        # create a dictionary with a random key with name and sccore of the player as values
        self.new_hiscore[code] = [self.name, self.score]   
        # save score on dictionary
        self.current_hiscore.update(self.new_hiscore)
        # save the hiscore file but sort first from the greater to lowest
        sorted_hiscore = dict(sorted(self.current_hiscore.items(), key=lambda item: item[1][1], reverse=True))
        try:
            with open (self.hiscore_file, "wb") as file:
                pickle.dump (sorted_hiscore, file)
        except Exception:
            pass


    def verify_score(self):
        
        # if the hiscore file has less than 10 scores update with the new score
        if len(self.current_hiscore) < 10:
            self.curr_menu = self.hiscore_menu
        
        # if the file has 10 scores update only if the new score is greater than the lowest
        if len(self.current_hiscore) == 10:
            lowest_hiscore = min(self.current_hiscore.items(), key=lambda item: item[1][1])
            key, values = lowest_hiscore
            if self.score > values[1]:
                self.current_hiscore.pop(key)
                self.curr_menu = self.hiscore_menu
            else:
                self.curr_menu = self.main_menu
                self.reset_game()
               



    def load_hiscore(self):
        if os.path.exists(self.hiscore_file):
            with open (self.hiscore_file, "rb") as file:
                try:
                    self.current_hiscore = pickle.load(file)
                except Exception:
                    self.current_hiscore={}
            if self.current_hiscore:
                if len(self.current_hiscore) > 10:
                    self.current_hiscore.popitem()
                self.hi_score = list(self.current_hiscore.values())[0][1]
            else:
                self.hi_score = 0
    

    def shoot_laser(self):
        """Create player laser sprite and add to the sprite group"""
        if len(self.lasers) < self.shoots_allowed:
            self.laser_sound.play()
            self.lasers.add(Laser((self.player_sprite.rect.center)))

    def blink_text (self):
        self.blink_time += 0.05 
        if self.blink_time >= 3:
            self.blink_time = 0


    def check_events(self):
        """Check player input events"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()              

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LCTRL or event.key == pygame.K_RCTRL:
                    self.shoot_laser()
                if event.key == pygame.K_ESCAPE:
                    if self.game_paused == False: 
                        self.game_paused = True
                   
                                   
    
    def check_events_paused(self):
         for event in pygame.event.get():
            if event.type == pygame.QUIT:
                 sys.exit()
            if event.type == pygame.KEYDOWN:              
                if event.key == pygame.K_ESCAPE:
                    self.playing = False
                    self.game_paused = False
                    self.reset_game()
                  
                if event.key == pygame.K_LCTRL or event.key == pygame.K_RCTRL:
                    self.game_paused = False
   

    def game_loop(self):
        """Run all the critical functions for the game """
        while self.playing:
    
            if not self.game_paused:
                
                self.check_events()
                self.screen.fill('black')
                self.initial_planet_animation()
                self.planet_animation()

                self.explosion_time()
                self.planets.update()
                self.stars.update()
               
                self.player.update()
                self.lasers.update()
                self.aliens.update(self.alien_direction, self.alien_speed)
                invaders.alien_shoot()
                self.alien_lasers.update()
                self.extra.update()
                self.blocks.update()
                self.extra_alien_timer()     

                self.alien_position_checker()
                self.collision_checks()
                
                self.display_score()
                self.display_hiscore()
                self.display_level()
                self.display_lives()

                self.stars.draw(self.screen)
                self.planets.draw(self.screen)
                self.player.draw (self.screen)
                self.draw_explosion()           
                self.blocks.draw(self.screen)
                self.redraw_blocks()
                self.lasers.draw(self.screen)
                self.aliens.draw(self.screen)
                self.alien_lasers.draw(self.screen)
                self.extra.draw(self.screen)
                self.crt.draw()
                self.level_up()
                self.new_life()
                self.pause_time(self.time, self.start)

                pygame.display.flip()
                self.dt = clock.tick(60)
            else:
                self.check_events_paused()
                self.screen.blit(self.pause_menu, self.pause_menu_rect)  
                pygame.display.flip()
                
           

if __name__ == '__main__':
    
    pygame.init()
    pygame.font.init()
    pygame.mixer.init()
    clock = pygame.time.Clock()
    # create a instance for game class
    invaders = Game()
   

    while invaders.running:
        invaders.curr_menu.display_menu()
        invaders.game_loop()
        
        
    