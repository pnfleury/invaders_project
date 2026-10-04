import pygame,sys, os, pickle
from random import choice, randint
from player import Player
from crt import CRT
from settings import Settings
from alien import Alien, Extra
from alien_laser import AlienLaser, ExtraLaser
from laser import Laser
from menu import *
import scenary
from scenary import Planet

class Game:
    """ Principal class of Invader-X game"""
    def __init__(self):

        self.s = Settings()
        self.clock = pygame.time.Clock()
        
        # initialize screen
        self.screen =  pygame.display.set_mode((self.s.screen_width, self.s.screen_heigth), self.s.flags)
        self.screen_rect = self.screen.get_rect()

        # Lifes indicator on top right screen
        self.life_surf_original = pygame.image.load(self.resource_path('assets/graphics/player.png')).convert_alpha()
        self.life_surf = pygame.transform.scale_by(self.life_surf_original, 0.6)
        self.live_x_start_pos = self.s.screen_width - (self.life_surf.get_size()[0] * 2.3 + 65)
        self.life_x = self.live_x_start_pos + ((self.life_surf.get_size()[0]))  

        # Load explosions images
        self.explosion_alien = pygame.image.load(self.resource_path('assets/graphics/alien_explosion.png')).convert_alpha() 
        self.explosion_extra = pygame.image.load(self.resource_path('assets/graphics/extra_explosion.png')).convert_alpha()
        self.laser_hit = pygame.image.load(self.resource_path('assets/graphics/laser_hit.png')).convert_alpha()
        self.explosion_player = pygame.image.load(self.resource_path('assets/graphics/player_explosion.png')).convert_alpha()
        self.block_hit = pygame.image.load(self.resource_path('assets/graphics/block_hit.png')).convert_alpha()
        self.laser_miss = pygame.image.load(self.resource_path('assets/graphics/laser_miss.png')).convert_alpha()

        # Load pause buttons images
        self.play_image = pygame.image.load(self.resource_path('assets/graphics/play.png')).convert_alpha()
        self.big_pause_image = pygame.image.load(self.resource_path('assets/graphics/pause_big.png')).convert_alpha()
        self.big_pause_image_rect = self.big_pause_image.get_rect(midtop = (self.s.screen_width /2, self.s.screen_heigth /3))
       
        # Create Font objects from files
        self.font_pixeled15 = pygame.font.Font(self.resource_path('assets/font/Pixeled.ttf'), 15)
        self.font_pixeled80 = pygame.font.Font(self.resource_path('assets/font/Pixeled.ttf'), 80)
        self.font_y22424 = pygame.font.Font(self.resource_path('assets/font/Y224-2vdae.ttf'), 24)
        self.font_y22436 = pygame.font.Font(self.resource_path('assets/font/Y224-2vdae.ttf'), 36) 
        self.font_y22472 = pygame.font.Font(self.resource_path('assets/font/Y224-2vdae.ttf'), 72)

        # Load sounds files
        #self.music = pygame.mixer.Sound(self.resource_path('assets/audio/01 BGM.mp3'))
        self.laser_sound = pygame.mixer.Sound(self.resource_path('assets/audio/shoot.wav'))
        self.alien_laser_sound = pygame.mixer.Sound(self.resource_path('assets/audio/alien_laser.wav'))
        self.extra_alien_sound = pygame.mixer.Sound(self.resource_path('assets/audio/extra_sound.wav'))
        self.extra_laser_sound = pygame.mixer.Sound(self.resource_path('assets/audio/extra_laser.wav'))
        self.new_life_sound = pygame.mixer.Sound(self.resource_path('assets/audio/life.mp3'))
        self.explosion_sound = pygame.mixer.Sound(self.resource_path('assets/audio/explosion.wav'))
        self.player_explosion_sound = pygame.mixer.Sound(self.resource_path('assets/audio/player_explosion.wav'))
        self.extra_explosion_sound = pygame.mixer.Sound(self.resource_path('assets/audio/extra_explosion.mp3'))
        self.block_rebuild_sound = pygame.mixer.Sound(self.resource_path('assets/audio/block_rebuild.wav'))
        self.shot_collision = pygame.mixer.Sound(self.resource_path('assets/audio/shot_collision.wav'))
        self.obstacle_explosion = pygame.mixer.Sound(self.resource_path('assets/audio/obstacle_explosion.mp3'))
        self.alien_fleet_sound = pygame.mixer.Sound(self.resource_path('assets/audio/alien_fleet.wav'))
        self.ship_thruster_sound = pygame.mixer.Sound(self.resource_path('assets/audio/ship_thruster.wav'))
        self.name_entry_sound = pygame.mixer.Sound(self.resource_path('assets/audio/name_entry.mp3'))
        self.beat_game_sound = pygame.mixer.Sound(self.resource_path('assets/audio/end_game.mp3'))
        self.bonus_sound = pygame.mixer.Sound(self.resource_path('assets/audio/bonus.mp3'))
        self.game_over_sound = pygame.mixer.Sound(self.resource_path('assets/audio/game_over.mp3'))

        # Set volume
        #self.music.set_volume(0.1)
        self.game_over_sound.set_volume(0.4)
        self.bonus_sound.set_volume(0.3)
        self.beat_game_sound.set_volume(0.8)
        self.name_entry_sound.set_volume(0.3)
        self.ship_thruster_sound.set_volume(0.3)
        self.alien_fleet_sound.set_volume(0.8)
        self.laser_sound.set_volume(0.2)
        self.alien_laser_sound.set_volume(0.2)
        self.extra_alien_sound.set_volume(0.1)
        self.extra_laser_sound.set_volume(0.2)
        self.new_life_sound.set_volume(0.3)
        self.explosion_sound.set_volume(0.2)
        self.player_explosion_sound.set_volume(0.2)
        self.extra_explosion_sound.set_volume(0.3)
        self.block_rebuild_sound.set_volume(0.2)
        self.obstacle_explosion.set_volume(0.2)
        self.shot_collision.set_volume(0.2)
        #self.warp_exit_sound.set_volume(0.2)

        ## Create instances
        self.crt = CRT(self)
        self.main_menu = Menu(self)
        self.game_over_menu = GameOver(self)
        self.hiscore_menu = Hiscore(self)
        self.beatgame_menu = BeatGame(self)
        self.shape = scenary.shape
       
        # sprites
        self.planet = Planet(self)
        self.alien = Alien('red',0,0, self)
        self.extra_sprite = Extra('left', self)
        self.player_sprite = Player(self)
       
        # sprite groups
        self.planets = pygame.sprite.Group(self.planet)
        self.player = pygame.sprite.GroupSingle(self.player_sprite)
        self.extra = pygame.sprite.GroupSingle()
        self.aliens = pygame.sprite.Group()
        self.blocks = pygame.sprite.Group()
        self.alien_lasers = pygame.sprite.Group()
        self.extra_lasers = pygame.sprite.Group()
        self.lasers = pygame.sprite.Group()
        self.stars = pygame.sprite.Group()
        

        """ initialize variables """
        # Menu inicial
        self.curr_menu = self.main_menu

        # flag for level up fucntion
        self.level_up_active = False  

        ## PAUSE FUNCTION
        # time variable for pause function 
        self.time =  0
        # initial time variable for pause function 
        self.initial_time = 0
        # flag variable for pause function
        self.start = False

        ## SHIP BOOST TIME FUNCTION
        # time variable for ship boost function 
        self.ship_time =  0
        # initial time variable for boost ship 
        self.ship_initial_time = 0
        self.start_boost = False
        
        ## OBSTACLE 
        # flag variable for create obstacles blocks
        self.create_obstacle_flag = True
        # flag variable for rebuild obstacles blocks
        self.block_rebuild = False
        # increment variable used on redraw blocks function
        self.block_count = 0
        
        ## Planets animation
        # Flag for start/stop initial planet animation
        self.finish_initial_planet_animation = False
        # Flag for start/stop planet animation
        self.finish_planet_animation = False
        # variable used on leave_planet_animation function
        self.i = 0
        
        ## Start game flags
        # Flag for start the game
        self.running = True
        # Flag for start/ stop the game_loop function
        self.playing = False
        
        # explosion time function variable
        self.dt = 0   

        # Call functions for create stars
        self.create_stars(self.s.x, self.s.y)

     
        
    """ GAME FUNCTIONS """

    def resource_path(self,relative_path):
        """ Retorna o caminho correto para o arquivo, funcionando no script ou no .exe """
        if hasattr(sys, '_MEIPASS'):
            return os.path.join(sys._MEIPASS, relative_path)
        return os.path.join(os.path.abspath("."), relative_path)


    def create_stars(self, x, y):

        for value in range(self.s.num_stars):
            rand_x = randint(0, self.s.screen_width)
            rand_y =  randint (0, self.s.screen_heigth)
            if x == rand_x:
                rand_x = randint(0, self.s.screen_width)
            if y == rand_y:
                rand_y = randint(0, self.s.screen_heigth)
            x = rand_x
            y = rand_y
            self.star_sprite = scenary.Stars('white', x, y, self)
            self.stars.add(self.star_sprite)



    def create_obstacle(self, offset_x):
        """Create obstacles sprites (player shields) 
        Parameters: 
        offset_x (int): space between obstacles 
        """
        for row_index, row in enumerate(self.shape):
            for col_index, col in enumerate(row):
                if col == 'x':
                    x = self.s.obstacle_x_start + col_index * self.s.block_size + offset_x
                    y = self.s.obstacle_y_start + row_index * self.s.block_size        
                    self.block = scenary.Block(self.s.block_size, self.s.obstacle_color, x, y)
                    self.blocks.add(self.block)
                         
   
    def create_multiple_obstacles(self):
        """Create multiples obstacles defined on obstacle_x_positions list"""
        for offset_x in self.s.obstacle_x_positions:
            self.create_obstacle(offset_x)
                        
    
    def alien_setup(self):
        """Create the aliens fleet"""
        for row_index, row in enumerate(range(self.s.alien_rows)):
            for col_index, col in enumerate(range(self.s.alien_cols)):
                x = col_index * self.s.alien_x_distance + self.s.aliens_x_offset
                y = row_index * self.s.alien_y_distance + self.s.aliens_y_offset
                
                if row_index == 0: alien_sprite = Alien('yellow', x, y, self)
                elif 1 <= row_index <=2: alien_sprite = Alien('green', x, y, self)
                else: alien_sprite = Alien('red', x, y, self)
                self.aliens.add(alien_sprite)    
           
    def alien_position_checker(self):
        """Check if the alien fleet had reach the side edge of the screen"""
        for alien in self.aliens:
            if alien.rect.right >= self.s.screen_width or alien.rect.left <= 0:
                self.alien_move_down()
                break

    def alien_move_down(self):
        """Move down the alien fleet when they reach the side edge of screen
        and force to the oposite direction"""
        if self.aliens:
            for alien in self.aliens:
                alien.rect.y += self.s.alien_distance
            lowest_alien_sprite = max (self.aliens, key=lambda a: a.rect.bottom)
            pos_y = lowest_alien_sprite.rect.bottom
            
            if pos_y >= self.s.screen_heigth:
                self.player_explosion_sound.play()
                self.s.lives = 0
                self.playing = False
                self.curr_menu = self.game_over_menu
            else: self.s.alien_direction *= -1 
               
    
    def alien_shoot(self):
        """ Create the aliens shoot"""
        if self.aliens:
            random_alien = choice(self.aliens.sprites())
            if len (self.alien_lasers) < self.s.alien_bullets_allowed:
                laser_sprite = AlienLaser (random_alien.rect.midbottom, self)
                self.alien_lasers.add(laser_sprite)
                self.alien_laser_sound.play()

    def extra_shoot(self):
        """ Create the aliens shoot"""
        if self.s.activate_extra_shot:
            if self.extra:
                current_sprite = self.extra.sprites()[0]
                if len (self.extra_lasers) < self.s.extra_bullets_allowed:
                    extra_laser_sprite = ExtraLaser (current_sprite.rect.midbottom, self)
                    self.extra_lasers.add(extra_laser_sprite)
                    self.extra_laser_sound.play()
          

    def extra_alien_timer (self):
        """Spawns an extra alien as soon as the cooldown ends"""
        if self.extra_sprite.execute == True:
            self.s.extra_spawn_time -= 1
            if self.s.extra_spawn_time <= 0:
                self.extra.add(Extra(choice(['right','left']), self))
                self.extra_alien_sound.play()
                self.s.extra_spawn_time = randint (self.s.range_a, self.s.range_b)


    def explosion_time(self):   
        """Duration of the explosions shown on the screen"""     
        for exp in self.s.active_explosions[:]:  
            exp["time"] -= self.dt
            if exp["time"] <= 0:
                self.s.active_explosions.remove(exp)


    def draw_explosion(self):
        """Draws images of the explosions on the screen if there are any in the list"""
        for exp in self.s.active_explosions:
            match exp['hit']:
                case 'extra_explosion':
                    self.screen.blit(self.explosion_extra,  exp["pos"])
                case 'extra':
                    self.draw_text(f"{exp['points']}",  self.font_pixeled15, 'red', exp['pos'][0] + 25, exp['pos'][1] + 25)
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
                    self.s.active_explosions.append({"time" : 8000, "hit" : "game_over"})            

                case 'earth':
                    self.draw_text(f'DEFEND EARTH',  self.font_y22472, '#E1E6E7', exp['pos'][0], exp['pos'][1])
                case 'moon':
                    self.draw_text(f'DEFEND MOON',  self.font_y22472, '#E1E6E7', exp['pos'][0], exp['pos'][1])
                case 'mars':
                    self.draw_text(f'DEFEND MARS',  self.font_y22472, '#E1E6E7', exp['pos'][0], exp['pos'][1])
                case 'jupiter':
                    self.draw_text(f'DEFEND JUPITER',  self.font_y22472, '#E1E6E7', exp['pos'][0], exp['pos'][1])
                case 'saturn':
                    self.draw_text(f'DEFEND SATURN',  self.font_y22472, '#E1E6E7', exp['pos'][0], exp['pos'][1])
                case 'uranus':
                    self.draw_text(f'DEFEND URANUS',  self.font_y22472, '#E1E6E7', exp['pos'][0], exp['pos'][1])
                case 'netuno':
                    self.draw_text(f'DEFEND NEPTUNE',  self.font_y22472, '#E1E6E7', exp['pos'][0], exp['pos'][1])
                
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
                        self.s.active_explosions.append({"pos" : (alien.rect.x, alien.rect.y), "time" : 100, "hit" : "alien"})                       
                        self.s.score += alien.value 
                    laser.kill()
                    self.explosion_sound.play()
                    self.s.alien_speed *= self.s.alien_speedup_scale                
                
                # Extra alien
                extra_hit = pygame.sprite.spritecollide(laser, self.extra, True)
                if extra_hit:
                    for extra in extra_hit:
                        self.s.extra_point = choice (self.s.extra_list_points)
                        self.s.active_explosions.append({"pos" : (extra.rect.x, extra.rect.y), "time" : 300, "hit" : "extra_explosion"})
                        self.s.active_explosions.append({"pos" : (extra.rect.x, extra.rect.y), "time" : 1300, "hit" : "extra", "points" : self.s.extra_point})
                        self.extra_explosion_sound.play()
                        self.extra_alien_sound.stop()
                        self.s.score += self.s.extra_point
                    laser.kill()
                     
                # Alien laser 
                laser_hit = pygame.sprite.spritecollide(laser, self.alien_lasers, True)
                if laser_hit:
                    self.s.active_explosions.append({"pos" : (laser.rect.x, laser.rect.y), "time" : 100, "hit" : "laser"})
                    self.shot_collision.play()
                    laser.kill()
                
                # Extra laser
                extra_laser_hit = pygame.sprite.spritecollide(laser, self.extra_lasers, True)
                if extra_laser_hit:
                    self.s.active_explosions.append({"pos" : (laser.rect.x, laser.rect.y), "time" : 100, "hit" : "laser"})
                    self.shot_collision.play()
                    self.extra_laser_sound.stop()
                    laser.kill()

        """ Alien lasers collisions """
        if self.alien_lasers:
            for laser in self.alien_lasers:
                # Player 
                if pygame.sprite.spritecollide(laser, self.player, True):
                    self.player_explosion_sound.play()
                    self.s.lives -= 1
                    self.alien_lasers.empty()
                    self.s.active_explosions.append({"pos" : (self.player_sprite.rect.x, self.player_sprite.rect.y), "time" : 500, "hit" : "player"})
                                                     
                # Blocks 
                if pygame.sprite.spritecollide (laser, self.blocks, True):
                    self.s.active_explosions.append({"pos" : (laser.rect.x, laser.rect.y), "time" : 500, "hit" : "block"})
                    self.obstacle_explosion.play()
                    laser.kill()

        """ Extra alien lasers collisions """
        if self.extra_lasers:
            for laser in self.extra_lasers:
                # Player 
                if pygame.sprite.spritecollide(laser, self.player, True):
                    self.player_explosion_sound.play()
                    self.s.lives -= 1
                    self.extra_lasers.empty()
                    self.s.active_explosions.append({"pos" : (self.player_sprite.rect.x, self.player_sprite.rect.y), "time" : 500, "hit" : "player"})
                                                                            
                # Blocks 
                if pygame.sprite.spritecollide (laser, self.blocks, True):
                    self.s.active_explosions.append({"pos" : (laser.rect.x, laser.rect.y), "time" : 500, "hit" : "block"})
                    self.obstacle_explosion.play()
                    laser.kill()
                    

        """ Alien collisions """
        if self.aliens:
            for block in self.blocks:
                # Blocks
                block_hit = pygame.sprite.spritecollide(block, self.aliens, False)
                if block_hit:
                    self.s.active_explosions.append({"pos" : (block.rect.x, block.rect.y), "time" : 500, "hit" : "block"})
                    block.kill()

            # Player
            if pygame.sprite.groupcollide(self.player, self.aliens, True, True):
                self.player_explosion_sound.play()
                self.s.active_explosions.append({"pos" : (self.player_sprite.rect.x, self.player_sprite.rect.y), "time" : 800, "hit" : "fleet_bottom"})
                self.s.lives < 0
                

    def zero_lives_check(self):
        if self.s.lives < 0:
            pygame.mixer.stop()
            self.player_explosion_sound.play()
            self.playing = False
            self.game_over_sound.play()
            self.curr_menu = self.game_over_menu        

    def display_lives(self):
        """Display the player life on screen"""
        self.draw_text(f'x {self.s.lives}',  self.font_pixeled15, self.s.text_col, self.s.screen_width - 40, 20)
        self.screen.blit(self.life_surf, (self.life_x,15))

    def display_score(self):
        """Display the score on screen"""
        self.draw_text(f'SCORE: {self.s.score:06}',  self.font_pixeled15, self.s.text_col, 20, 0, 'topleft')
      
    def display_hiscore(self): 
        """Display the hiscore on screen"""
        self.draw_text(f'HI-SCORE: {self.s.hi_score:06}',  self.font_pixeled15, self.s.text_col, self.screen_rect.centerx, self.screen_rect.top + 20)
        if self.s.score > self.s.hi_score:
            self.s.hi_score = self.s.score
    
    def display_level(self):
        """Display the current level on screen"""
        if self.s.level > 0:
            self.draw_text(f'LEVEL: {self.s.level}',  self.font_pixeled15, self.s.text_col, self.s.screen_width - 200, 20)

    def new_life(self):
        """Gives the player an extra life when they reach a certain score."""
        match self.s.score:

            case s if s >= 50000 and not self.s.executed_2:
                self.s.lives += 1
                self.new_life_sound.play()
                self.s.executed_2 = True

            case s if s >= 100000 and not self.s.executed_3:
                self.s.lives += 1
                self.new_life_sound.play()
                self.s.executed_3 = True

            case s if s >= 150000 and not self.s.executed_4:
                self.s.lives += 1
                self.new_life_sound.play()
                self.s.executed_4 = True

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
    
    def ship_boost_time(self, time, start):
        """ Take a pause before continuing
        Parameters:
        time (int) = pause time 
        start (boolean)= starts pause """
        if start:
            self.ship_initial_time += 0.03
            if self.ship_initial_time >= time:
                self.ship_initial_time = 0
                return True

    def level_up (self):
        if self.level_up_active:
            if not self.aliens:
                self.alien_fleet_sound.stop()
                if self.pause_time(8, True):
                    self.s.level +=1 
                    self.alien_setup()
                    self.alien_fleet_sound.play(loops=-1)
                    self.restart_speed()
                    self.raise_difficulty()
                    self.s.alien_direction = 1

    def initial_planet_animation(self):
        if not self.finish_initial_planet_animation:
            if self.planet.execute_show_planet == False:
                self.s.moving_stars = False
                self.describe_planet()
                if self.create_obstacle_flag:
                    self.create_multiple_obstacles()
                    self.block_rebuild = True
                    self.create_obstacle_flag = False
                    self.level_up_active = True
                    self.finish_initial_planet_animation = True


    def planet_animation(self):
        if not self.finish_planet_animation:
            if self.s.level in (3, 6, 9, 12, 15, 18, 21) and not (self.aliens):
                self.level_up_active = False
                self.alien_lasers.empty()
                self.blocks.empty()
                if self.extra:
                    for extra in self.extra:
                        self.s.active_explosions.append({"pos" : (extra.rect.x, extra.rect.y), "time" : 300, "hit" : "extra_explosion"})
                        self.extra_explosion_sound.play()
                        self.extra.empty()
                        self.extra_alien_sound.stop()
                if not self.s.ship_thruster_sound_played:
                    self.ship_thruster_sound.play()
                    self.s.ship_thruster_sound_played = True
                self.s.moving_stars = True
                self.s.ship_thruster_on = True 
                self.planet.execute_hide_planet = True
                if self.pause_time(10, True):
                    if self.s.level == 21:
                        self.finish_planet_animation = True
                        self.s.moving_stars = False
                        self.playing = False
                        self.curr_menu = self.beatgame_menu
                    else:
                        self.i += 1
                        self.planet.image = self.planet.list[self.i] 
                        self.finish_planet_animation = True
                        self.planet.execute_show_planet = True
                        self.create_obstacle_flag = True
                        self.finish_initial_planet_animation = False
                        self.s.ship_thruster_sound_played = False
                                        

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
        self.create_obstacle_flag = True
        self.player_sprite.restart_player_location()
        self.s.initialize_dynamic_settings()
      

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
        self.s.alien_speed = 1.3

    def describe_planet(self):
        if self.planet.image == self.planet.list[0]:
            self.s.active_explosions.append({"pos" : (self.screen_rect.centerx, self.screen_rect.centery), "time" : 4000, "hit" : "earth"})
        elif self.planet.image == self.planet.list[1]:
            self.s.active_explosions.append({"pos" : (self.screen_rect.centerx, self.screen_rect.centery), "time" : 4000, "hit" : "moon"})
        elif self.planet.image == self.planet.list[2]:
                self.s.active_explosions.append({"pos" : (self.screen_rect.centerx, self.screen_rect.centery), "time" : 4000, "hit" : "mars"})
        elif self.planet.image == self.planet.list[3]:
            self.s.active_explosions.append({"pos" : (self.screen_rect.centerx, self.screen_rect.centery), "time" : 4000, "hit" : "jupiter"})
        elif self.planet.image == self.planet.list[4]:
            self.s.active_explosions.append({"pos" : (self.screen_rect.centerx, self.screen_rect.centery), "time" : 4000, "hit" : "saturn"})
        elif self.planet.image == self.planet.list[5]:
            self.s.active_explosions.append({"pos" : (self.screen_rect.centerx, self.screen_rect.centery), "time" : 4000, "hit" : "uranus"})
        elif self.planet.image == self.planet.list[6]:
            self.s.active_explosions.append({"pos" : (self.screen_rect.centerx, self.screen_rect.centery), "time" : 4000, "hit" : "netuno"})

     
    def raise_difficulty(self):
        """Increase the game's difficulty by raising the number of shots fired by the alien fleet
          as the level rises. Raise the number of player's shots starting on level 4 """
        if self.s.level in (1, 2):
            self.s.alien_bullets_allowed = 1
            
        elif self.s.level == 3:
            self.s.activate_extra_shot = True
            self.s.extra_bullets_allowed = 1
            self.finish_planet_animation = False
            
        elif self.s.level in (4, 5):
            self.s.alien_bullets_allowed = 2
           
        elif self.s.level == 6:
            self.s.extra_bullets_allowed = 2
            self.finish_planet_animation = False

        elif self.s.level in (7, 8):
            self.s.alien_bullets_allowed = 3
            self.s.shoots_allowed = 2
        
        elif self.s.level == 9:
            self.s.extra_bullets_allowed = 3
            self.finish_planet_animation = False
           
        elif self.s.level in (10, 11):
            self.s.alien_bullets_allowed = 4
            
        elif self.s.level == 12:
            self.s.extra_bullets_allowed = 4
            self.finish_planet_animation = False

        elif self.s.level in (13, 14):
            self.s.alien_bullets_allowed = 5
            self.s.alien_speed = 1.5    
        
        elif self.s.level == 15:
            self.s.extra_bullets_allowed = 5
            self.finish_planet_animation = False

        elif self.s.level in (16, 17):
            self.s.alien_bullets_allowed = 6
            self.s.alien_speed = 1.7
           
        elif self.s.level == 18:
            pygame.time.set_timer(self.s.EXTRALASER, 500)
            self.finish_planet_animation = False
            
        elif self.s.level in (19, 20):
            self.s.alien_bullets_allowed = 6
            self.s.alien_speed = 1.9 
           
        elif self.s.level == 21: 
            self.finish_planet_animation = False
            
   
    def save_hiscore(self):
         # define a random key for the dictionary
        code = randint(1, 1000000)
        # if the dictionary key exists in loaded hiscore file get other random key 
        if str(code) in self.s.current_hiscore.keys():
            code = randint(1, 1000000)
        # create a dictionary with a random key with name and sccore of the player as values
        self.s.new_hiscore[code] = [self.s.name, self.s.score]   
        # save score on dictionary
        self.s.current_hiscore.update(self.s.new_hiscore)
        # save the hiscore file but sort first from the greater to lowest
        sorted_hiscore = dict(sorted(self.s.current_hiscore.items(), key=lambda item: item[1][1], reverse=True))
        try:
            with open (self.s.hiscore_file, "wb") as file:
                pickle.dump (sorted_hiscore, file)
        except Exception:
            pass


    def verify_score(self):
        lowest_hiscore = min(self.s.current_hiscore.items(), key=lambda item: item[1][1])
        key, values = lowest_hiscore
        if self.s.score > values[1]:
            self.s.current_hiscore.pop(key)
            self.name_entry_sound.play()
            self.curr_menu = self.hiscore_menu
        else:
            self.curr_menu = self.main_menu
            self.reset_game()
            

    def shoot_laser(self):
        """Create player laser sprite and add to the sprite group"""
        if len(self.lasers) < self.s.shoots_allowed:
            self.laser_sound.play()
            self.lasers.add(Laser(self.player_sprite.rect.center, self))

    def blink_text (self):
        self.blink_time += 0.05 
        if self.blink_time >= 3:
            self.blink_time = 0


    def check_events(self):
        """Check player input events"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()              
            if event.type == self.s.EXTRALASER: #and self.extra:
                self.extra_shoot()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LCTRL or event.key == pygame.K_RCTRL:
                    self.shoot_laser()
                if event.key == pygame.K_ESCAPE:
                    if self.s.game_paused == False: 
                        self.s.game_paused = True
                        pygame.mixer.pause()
                        
                                  
    
    def check_events_paused(self):
         for event in pygame.event.get():
            if event.type == pygame.QUIT:
                 sys.exit()
            if event.type == pygame.KEYDOWN:              
                if event.key == pygame.K_ESCAPE:
                    self.playing = False
                    self.s.game_paused = False
                    self.reset_game()
                  
                if event.key == pygame.K_LCTRL or event.key == pygame.K_RCTRL:
                    self.s.game_paused = False
                    pygame.mixer.unpause()

    def pause_menu(self):
        self.check_events_paused()
        self.screen.blit(self.big_pause_image, self.big_pause_image_rect)
        self.screen.blit(self.main_menu.esc_key, (self.s.screen_width / 2 - 60, self.s.screen_heigth / 2 + 10))
        self.screen.blit(self.main_menu.exit_image, (self.s.screen_width /2 + 20, self.s.screen_heigth /2 + 20))
        self.screen.blit(self.main_menu.ctrl_key, (self.s.screen_width / 2 - 60, self.s.screen_heigth / 2 + 80))
        self.screen.blit(self.play_image, (self.s.screen_width /2 + 20, self.s.screen_heigth /2 + 90))        
        pygame.display.flip()


    def game_loop(self):
        """Run all the critical functions for the game """
        while self.playing:
    
            if not self.s.game_paused:
                
                self.check_events()
                self.screen.fill('black')
                self.stars.update()
                self.player.update()
                self.lasers.update()
                self.aliens.update(self.s.alien_direction, self.s.alien_speed)
                self.alien_lasers.update()
                self.extra_lasers.update()
                self.blocks.update()
                self.extra.update()
                self.planets.update()
                
                self.initial_planet_animation()
                self.planet_animation()
                self.explosion_time()
                self.alien_shoot()
                self.extra_alien_timer()     
                self.alien_position_checker()
                self.collision_checks()
                self.level_up()
                self.new_life()
                self.pause_time(self.time, self.start)
                self.ship_boost_time(self.ship_time, self.start_boost)
                self.zero_lives_check()
                self.display_score()
                self.display_hiscore()
                self.display_level()
                self.display_lives()
                self.stars.draw(self.screen)
                self.planets.draw(self.screen)
                self.player.draw (self.screen)
                self.lasers.draw(self.screen)
                self.aliens.draw(self.screen)
                self.alien_lasers.draw(self.screen)
                self.extra_lasers.draw(self.screen)
                self.blocks.draw(self.screen)
                self.extra.draw(self.screen)
               
                self.draw_explosion()           
                self.redraw_blocks()
                self.crt.draw()
                pygame.display.flip()
                self.dt = self.clock.tick(60)
            else:
                self.pause_menu()
               

if __name__ == '__main__':
    
    pygame.init()
    pygame.font.init()
    pygame.mixer.init()
    invaders = Game()
   

    while invaders.running:
        pygame.mouse.set_visible(False)
        invaders.curr_menu.display_menu()
        invaders.game_loop()
       
        
        
    