import pygame, sys, asyncio



class Menu():

    def __init__(self, game):
        
        self.game = game
        self.earth_view = pygame.image.load(self.game.resource_path('assets/graphics/planets/earth_view.png')).convert_alpha()
        self.keys_image = pygame.image.load(self.game.resource_path('assets/graphics/keys.png')).convert_alpha()
        self.hiscore_keys_image = pygame.image.load(self.game.resource_path('assets/graphics/hiscore_keys.png')).convert_alpha()
        self.copyright_image = pygame.image.load(self.game.resource_path('assets/graphics/copyright.png')).convert_alpha()

       # Title points animation settings
        self.current_sprite = 0
        self.image = self.game.title_points[self.current_sprite]
        self.rect = self.image.get_rect(midtop = (self.game.s.screen_width / 2, self.game.s.screen_heigth / 2))

        # variable for blinking text used on blink function
        self.blink_time = 0
        self.hiscore_active = True
        self.speed = 1
        self.hi_color = 'white'
        self.first_color = '#fff01f'
        self.second_color = '#c4c4c4'
        self.third_color = '#FF7A00'
        self.hi_space = 0
        self.wait = 0

      
    def draw_text(self, text, font, text_col, x, y):
        img = font.render (text, False, text_col)
        img_rect = img.get_rect()
        img_rect.center = (x,y)
        self.game.screen.blit(img, img_rect)

    def draw_text_topleft(self, text, font, text_col, x, y):
        img = font.render (text, False, text_col)
        img_rect = img.get_rect()
        img_rect.topleft = (x,y)
        self.game.screen.blit(img, img_rect)

    def blink_text (self):
        self.blink_time += 0.1 
        if self.blink_time >= 3:
            self.blink_time = 0

    def show_hiscore_list(self):
        if len(self.game.s.hiscore_list) > 0:
            try:    
                self.draw_text (f"1. {self.game.s.hiscore_list[0][0]} {self.game.s.hiscore_list[0][1]:06}", self.game.font_hiscore, self.first_color, self.game.s.screen_width /2, self.game.s.screen_heigth / 5)
                self.draw_text (f"2. {self.game.s.hiscore_list[1][0]} {self.game.s.hiscore_list[1][1]:06}", self.game.font_hiscore, self.second_color, self.game.s.screen_width /2, self.game.s.screen_heigth / 5 + 36)
                self.draw_text (f"3. {self.game.s.hiscore_list[2][0]} {self.game.s.hiscore_list[2][1]:06}", self.game.font_hiscore, self.third_color, self.game.s.screen_width /2, self.game.s.screen_heigth / 5 + 72)
                self.draw_text (f"4. {self.game.s.hiscore_list[3][0]} {self.game.s.hiscore_list[3][1]:06}", self.game.font_hiscore, self.hi_color, self.game.s.screen_width /2, self.game.s.screen_heigth / 5 + 108)
                self.draw_text (f"5. {self.game.s.hiscore_list[4][0]} {self.game.s.hiscore_list[4][1]:06}", self.game.font_hiscore, self.hi_color, self.game.s.screen_width /2, self.game.s.screen_heigth / 5 + 144)
                self.draw_text (f"6. {self.game.s.hiscore_list[5][0]} {self.game.s.hiscore_list[5][1]:06}", self.game.font_hiscore, self.hi_color, self.game.s.screen_width /2, self.game.s.screen_heigth / 5 + 180)
                self.draw_text (f"7. {self.game.s.hiscore_list[6][0]} {self.game.s.hiscore_list[6][1]:06}", self.game.font_hiscore, self.hi_color, self.game.s.screen_width /2, self.game.s.screen_heigth / 5 + 216)
                self.draw_text (f"8. {self.game.s.hiscore_list[7][0]} {self.game.s.hiscore_list[7][1]:06}", self.game.font_hiscore, self.hi_color, self.game.s.screen_width /2, self.game.s.screen_heigth / 5 + 252)
                self.draw_text (f"9. {self.game.s.hiscore_list[8][0]} {self.game.s.hiscore_list[8][1]:06}", self.game.font_hiscore, self.hi_color, self.game.s.screen_width /2, self.game.s.screen_heigth / 5 + 288)
                self.draw_text (f"10.{self.game.s.hiscore_list[9][0]} {self.game.s.hiscore_list[9][1]:06}", self.game.font_hiscore, self.hi_color, self.game.s.screen_width /2, self.game.s.screen_heigth / 5 + 324)
            except:
                pass
        else: pass

        
    def title_menu(self):
        ''' function to show the game title screen '''
        if self.game.s.title_active:
           
            self.game.screen.blit(self.earth_view,(0, 300))
            self.draw_text_topleft("ATTACK on", self.game.font_title, '#ff0000', self.game.s.screen_width / 6, 50)
            self.draw_text_topleft("SOLAR SYSTEM", self.game.font_title, '#ffef1f', self.game.s.screen_width / 6, 110)
            self.blink_text()

            
            self.wait += 0.05 
            match self.wait:     
                case w if w > 25 and w < 50:
                    self.current_sprite += 0.08
                    if self.current_sprite >= len (self.game.title_points):
                        self.current_sprite = 0
                    self.image = self.game.title_points[int(self.current_sprite)]
                    self.game.screen.blit(self.image, self.rect)
    
                case w if w > 50:
                    self.draw_text_topleft("DEVELOPMENT, PROGRAMMING, ART AND AUDIO", self.game.font_credits, 'white', self.game.s.screen_width / 6, 180)
                    self.draw_text_topleft("PAULO FLEURY", self.game.font_credits, self.first_color, self.game.s.screen_width / 6, 195)
                    self.draw_text_topleft("PLANET IMAGES", self.game.font_credits, 'white', self.game.s.screen_width / 6, 220)
                    self.draw_text_topleft("FROM NASA IMAGE AND VIDEO LIBRARY", self.game.font_credits, self.first_color, self.game.s.screen_width / 6, 235)
                    
                    if self.wait > 85: self.wait = 0
            
            self.draw_text_topleft("2026 PAULO FLEURY", self.game.font_copyright, '#c4c4c4', 65, self.game.s.screen_heigth - 50)
            self.draw_text_topleft("V.0.4.0-BETA", self.game.font_copyright, '#c4c4c4', 65, self.game.s.screen_heigth - 35)
            self.game.screen.blit(self.copyright_image, (45, self.game.s.screen_heigth - 48)) 

            self.game.screen.blit(self.keys_image, (65, 300)) 
            
            if self.blink_time > 1:
                self.draw_text("PRESS [ENTER] TO PLAY",  self.game.font_credits, '#fff01f', self.game.s.screen_width /2, self.game.s.screen_heigth - 38)

            if self.game.pause_time(90, True): 
                self.game.s.title_active = False

        else:

            self.draw_text("HIGH SCORES", self.game.font_hiscore, '#45ea1d', self.game.s.screen_width /2, self.game.s.screen_heigth / 9)
            self.show_hiscore_list()
            # give a pause before changing to title game screen
            if self.game.pause_time(30, True):
                self.game.s.title_active = True

    def start_game (self):
        self.game.extra.empty()
        self.game.extra_sprite.execute = False
        self.game.extra_alien_sound.stop()
        self.game.player_sprite.play_thruster_sound = False
        self.game.s.menu_stars = False
        self.game.s.moving_stars = True
        self.run_display = False
        self.game.playing = True
        self.game.s.ship_thruster_on = True
        self.exit_hiscore_time = 40

    
    def check_input(self):
        """Check player input events"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                raise SystemExit()               
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    self.start_game()
                if event.key == pygame.K_ESCAPE:
                    raise SystemExit()
                    

    async def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.check_input()
            self.game.screen.fill('black')
            self.game.extra.update()
            self.game.stars.update()
            self.game.extra_alien_timer()  
            self.game.stars.draw(self.game.screen)
            self.title_menu()
            self.game.extra.draw(self.game.screen)
            #self.game.crt.draw()   
            pygame.display.flip()
            self.game.clock.tick(60)
            await asyncio.sleep(0)


class GameOver (Menu):
    def __init__(self, game):
        Menu.__init__(self, game)

        self.count = 1

    def game_over_menu(self):
        """Show the game over text on screen and stop the game"""
        self.count += 0.1
        self.game.display_scoreboard()
        self.game.stars.draw(self.game.screen)
        self.game.planets.draw(self.game.screen) 
        self.game.blocks.draw(self.game.screen)
        self.game.aliens.draw(self.game.screen)
        if self.count < 2:
            self.game.screen.blit(self.game.explosion_player, (self.game.player_sprite.rect.x, self.game.player_sprite.rect.y))
        self.draw_text("GAME OVER", self.game.font_game_over, "#3F0422", self.game.screen_rect.centerx + 6, self.game.screen_rect.centery + 6)
        self.draw_text("GAME OVER", self.game.font_game_over, '#FF007F', self.game.screen_rect.centerx, self.game.screen_rect.centery)

        if self.game.pause_time(28, True):
            self.run_display = False
            if self.game.s.score > 0:
                self.game.verify_score()  
            else:
                self.game.reset_game()  
                self.game.curr_menu = self.game.main_menu
                
            

    async def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.game.screen.fill('black')
            self.game_over_menu()
            #self.game.crt.draw()
            pygame.display.flip()
            self.game.clock.tick(60)
            await asyncio.sleep(0)


class Hiscore (Menu):
    def __init__(self, game):
        Menu.__init__(self, game)

        
        self.alphabet = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O',
             'P','Q','R','S','T','U','V','W','X','Y','Z','<', '+']
        self.alphabet_copy = self.alphabet[:]
        
        # gray letters for first to third place 
        self.hi_color = self.first_color = self.second_color = self.third_color = '#404040'     
    
        self.hiscore_initialize()    

    def hiscore_initialize (self):
        # Timer for exiting hiscore menu
        self.exit_hiscore_time = 40
        self.last_second = pygame.time.get_ticks()
                
        # player name list.
        self.player_name = []
        # index variable of alphabet list.
        self.i = 0
        # space between letters on input hiscore screen.
        self.space = 0
        self.score_color = '#ff0000'
            
        
    def check_input(self):
        ''' get player input for hiscore '''
        # press left or right arrow to choose the letter on alphabet list.
        if self.actual_time - self.last_second >= 1000: 
            self.exit_hiscore_time -= 1
            self.last_second = self.actual_time        

        for event in pygame.event.get():          
            
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    self.i += 1
                    if self.i >= len (self.alphabet): self.i = 0
                if event.key == pygame.K_LEFT:
                    self.i -= 1
                    if self.i < 0: self.i = len (self.alphabet) - 1
                # press control key to get a letter.
                if event.key == pygame.K_LCTRL or event.key == pygame.K_RCTRL:
                    # If the player's name is 3 letters or fewer and the index is not 'del', 
                    # save it to the list.
                    if len(self.player_name) < 3 and self.i not in {26, 27}:    # i=26 is 'DEL'.
                        self.player_name.append(self.alphabet[self.i])     # save on player name list.
                        self.space += 48 # add a horizontal space after selecting the letter.
                        self.i = 0   # the alphabet list index jumps to the first letter.
                    # choose "+" to save hiscore.
                    # select '<' to delete the character and move to the previous character.
                    else:
                        if self.alphabet[self.i] == '<' and self.player_name:
                            self.player_name.pop()
                            self.space -= 48
                            self.i = 0

                        if self.alphabet[self.i] == '+':
                            self.save_hiscore()
                      

    def display_letters(self):
        # If time runs out, save and exit to the main menu
        if self.exit_hiscore_time < 0:
            pygame.time.wait(1000) 
            self.save_hiscore()
        # display blinking hiscore
        if self.blink_time >= 1.5:
            self.draw_text("HIGH SCORES", self.game.font_hiscore, '#45ea1d', self.game.s.screen_width /2, self.game.s.screen_heigth / 9)
        # If the first letter is chosen, display it on the screen.
        if len(self.player_name) > 0:
            first_letter = self.game.font_initials.render(self.player_name[0], True, self.score_color)
            self.game.screen.blit(first_letter, (300, self.game.s.screen_heigth / 2 - self.hiscore_keys_image.get_height()))
        # If the second letter is chosen, display it on the screen.
        if len(self.player_name) > 1:
            second_letter = self.game.font_initials.render(self.player_name[1], True, self.score_color)
            self.game.screen.blit(second_letter, (348, self.game.s.screen_heigth / 2 - self.hiscore_keys_image.get_height()))
        # If the third letter is chosen, display it on the screen.
        if len(self.player_name) > 2:
            last_letter = self.game.font_initials.render(self.player_name[2], True, self.score_color)
            self.game.screen.blit(last_letter, (396, self.game.s.screen_heigth / 2 - self.hiscore_keys_image.get_height()))
        # if three letters are choosen shrink the alphabet list to two options, 'end' or 'del'.
            self.alphabet = ['<', '+']
        else:
            # if choosen letters are minor than three, the alphabet list remains full.
            self.alphabet = self.alphabet_copy

        # displays the letter on the screen for the player to choose using the arrow keys.
        choose_letters = self.game.font_initials.render(self.alphabet[self.i], True, self.score_color)
        self.game.screen.blit(choose_letters, (300 + self.space, self.game.s.screen_heigth / 2 - self.hiscore_keys_image.get_height()))
        
        self.game.screen.blit(self.hiscore_keys_image, (300, self.game.s.screen_heigth / 2))
        # display timer for enter name
        if self.exit_hiscore_time <= 0:
            self.draw_text(f"0", self.game.font_game_over, "#c4c4c4" , 552, 210)
        else:
            self.draw_text(f"{self.exit_hiscore_time}", self.game.font_game_over, "#c4c4c4" , 552, 210)
        
    def save_hiscore (self):
        self.game.s.name = "".join(self.player_name).ljust(3, ".")
        self.game.save_hiscore()
        pygame.mixer.stop()
        self.game.reset_game()
        self.run_display = False
        self.game.curr_menu = self.game.main_menu
        
    async def display_menu(self):
        self.run_display = True
        while self.run_display:                         
            self.game.screen.fill("black")
            self.blink_text()
            self.game.stars.draw(self.game.screen)
            self.game.stars.update()
            self.show_hiscore_list()
            self.actual_time = pygame.time.get_ticks()
            self.display_letters() 
            self.check_input()           
            pygame.display.flip()
            self.game.clock.tick(60)
            await asyncio.sleep(0)


class BeatGame (Menu):
    def __init__(self, game):
        Menu.__init__(self, game)

        self.bonus = 0

    def end_game_bonus (self):
        if self.game.s.activate_bonus:
            if not self.game.s.executed_bonus:
                self.game.bonus_sound.play()
                self.game.s.lives += 1
                self.bonus = self.game.s.lives * self.game.s.bonus
                self.game.s.score += self.bonus
                self.game.s.executed_bonus = True
            self.draw_text(f"BONUS  {self.game.s.bonus} X {self.game.s.lives} LIVES = {self.bonus}" , self.game.font_end_game, '#00ff00', self.game.s.screen_width / 2, self.game.s.screen_heigth / 5)
            
    
    def end_game(self):
        self.blink_text()
        self.draw_text("CONGRATULATIONS", self.game.font_end_game, '#fff01f', self.game.s.screen_width /2, self.game.s.screen_heigth / 3)
        self.draw_text("You defended our entire solar system", self.game.font_end_game, 'white', self.game.s.screen_width /2, self.game.s.screen_heigth / 3 + 36)
        self.draw_text("and drove the alien armada back", self.game.font_end_game, 'white', self.game.s.screen_width /2, self.game.s.screen_heigth / 3 + 72)
        self.draw_text("to the far reaches of the universe", self.game.font_end_game, 'white', self.game.s.screen_width /2, self.game.s.screen_heigth / 3 + 108)
        self.draw_text("Your job is done", self.game.font_end_game, 'white', self.game.s.screen_width /2, self.game.s.screen_heigth / 3 + 144)
        self.draw_text("you can now return to Earth", self.game.font_end_game, 'white', self.game.s.screen_width /2, self.game.s.screen_heigth / 3 + 180)
        if self.game.pause_time(50, True):
            self.game.s.activate_bonus = True
            self.game.s.unlock_input = True
            
    def exit_congrats (self):
        self.game.end_game_music.stop()
        self.run_display = False
        self.game.verify_score()          

    
    def check_input(self):
        """Check player input events"""
        if pygame.mixer.get_busy() == False:
            self.exit_congrats()

        if self.game.s.unlock_input:
            if self.blink_time > 1:
                self.draw_text("Press [ENTER] to continue",  self.game.font_credits, 'white', self.game.s.screen_width /2, self.game.s.screen_heigth - 30)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()              
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        self.exit_congrats()
                        
        
    async def display_menu(self):
        self.game.end_game_music.play()
        self.run_display = True
        self.game.s.ship_last_thrust = True
        while self.run_display:
            self.game.screen.fill('black')
            self.game.stars.update()
            self.game.player.update()
            self.game.stars.draw(self.game.screen)
            self.game.player.draw(self.game.screen)
            self.end_game()
            self.end_game_bonus()
            #self.game.crt.draw()
            self.check_input()
            pygame.display.flip()
            self.game.clock.tick(60)
            await asyncio.sleep(0)