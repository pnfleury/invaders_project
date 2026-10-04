import pygame, sys
from settings import Settings


class Menu():

    def __init__(self, game):
        
        self.game = game
        self.earth_view = pygame.image.load(self.game.resource_path('assets/graphics/planets/earth_view.png')).convert_alpha()
        self.left_arrow = pygame.image.load(self.game.resource_path('assets/graphics/keys/left_arrow.png')).convert_alpha()
        self.right_arrow = pygame.image.load(self.game.resource_path('assets/graphics/keys/right_arrow.png')).convert_alpha()
        self.ctrl_key = pygame.image.load(self.game.resource_path('assets/graphics/keys/ctrl_key.png')).convert_alpha()
        self.esc_key = pygame.image.load(self.game.resource_path('assets/graphics/keys/esc_key.png')).convert_alpha()
        self.exit_image = pygame.image.load(self.game.resource_path('assets/graphics/exit.png')).convert_alpha()
        self.pause_image = pygame.image.load(self.game.resource_path('assets/graphics/pause.png')).convert_alpha()
        self.player_image = pygame.image.load(self.game.resource_path('assets/graphics/player_image.png')).convert_alpha()   
       
        # variable for blinking text used on blink function
        self.blink_time = 0
        self.hiscore_list = []
        self.title_active = True
        self.hiscore_active = True
        self.speed = 1
        self.hi_color = 'white'
        self.first_color = '#fff01f'
        self.second_color = '#c4c4c4'
        self.third_color = '#FF7A00'
        self.hi_space = 0
      
    def draw_text(self, text, font, text_col, x, y):
        img = font.render (text, False, text_col)
        img_rect = img.get_rect()
        img_rect.center = (x,y)
        self.game.screen.blit(img, img_rect)


    def blink_text (self):
        self.blink_time += 0.1 
        if self.blink_time >= 3:
            self.blink_time = 0

    def show_hiscore_list(self):
        self.hiscore_list = list(self.game.s.current_hiscore.values())
        hiscore_list_size = len (self.hiscore_list)
        if hiscore_list_size > 0:
            try:    
                self.draw_text (f"1. {self.hiscore_list[0][0]} {self.hiscore_list[0][1]:06}", self.game.font_y22436, self.first_color, self.game.s.screen_width /2, self.game.s.screen_heigth / 5)
                self.draw_text (f"2. {self.hiscore_list[1][0]} {self.hiscore_list[1][1]:06}", self.game.font_y22436, self.second_color, self.game.s.screen_width /2, self.game.s.screen_heigth / 5 + 60)
                self.draw_text (f"3. {self.hiscore_list[2][0]} {self.hiscore_list[2][1]:06}", self.game.font_y22436, self.third_color, self.game.s.screen_width /2, self.game.s.screen_heigth / 5 + 120)
                self.draw_text (f"4. {self.hiscore_list[3][0]} {self.hiscore_list[3][1]:06}", self.game.font_y22436, self.hi_color, self.game.s.screen_width /2, self.game.s.screen_heigth / 5 + 180)
                self.draw_text (f"5. {self.hiscore_list[4][0]} {self.hiscore_list[4][1]:06}", self.game.font_y22436, self.hi_color, self.game.s.screen_width /2, self.game.s.screen_heigth / 5 + 240)
                self.draw_text (f"6. {self.hiscore_list[5][0]} {self.hiscore_list[5][1]:06}", self.game.font_y22436, self.hi_color, self.game.s.screen_width /2, self.game.s.screen_heigth / 5 + 300)
                self.draw_text (f"7. {self.hiscore_list[6][0]} {self.hiscore_list[6][1]:06}", self.game.font_y22436, self.hi_color, self.game.s.screen_width /2, self.game.s.screen_heigth / 5 + 360)
                self.draw_text (f"8. {self.hiscore_list[7][0]} {self.hiscore_list[7][1]:06}", self.game.font_y22436, self.hi_color, self.game.s.screen_width /2, self.game.s.screen_heigth / 5 + 420)
                self.draw_text (f"9. {self.hiscore_list[8][0]} {self.hiscore_list[8][1]:06}", self.game.font_y22436, self.hi_color, self.game.s.screen_width /2, self.game.s.screen_heigth / 5 + 480)
                self.draw_text (f"10.{self.hiscore_list[9][0]} {self.hiscore_list[9][1]:06}", self.game.font_y22436, self.hi_color, self.game.s.screen_width /2, self.game.s.screen_heigth / 5 + 540)
            except:
                pass
        else: pass

        
    def title_menu(self):
        ''' function to show the game title screen '''
        #self.game.load_hiscore()
        if self.title_active:
           
            self.game.screen.blit(self.earth_view,(0, 500))
            
            self.blink_text()
                            
            self.draw_text (f'HI-SCORE: {self.game.s.hi_score:06}',  self.game.font_pixeled15, 'white', self.game.s.screen_width / 2, 20)
            self.draw_text("INVADERS", self.game.font_pixeled80, "#074B07", self.game.s.screen_width / 2 + 10, self.game.s.screen_heigth / 4 + 10)
            self.draw_text("INVADERS", self.game.font_pixeled80, '#00ff00', self.game.s.screen_width / 2, self.game.s.screen_heigth / 4)
            
            self.game.screen.blit(self.esc_key, (140, 490))  
            self.game.screen.blit(self.exit_image, (220, 500)) 
            self.game.screen.blit(self.pause_image, (290, 500)) 
            
            self.game.screen.blit( self.ctrl_key, (140, 560)) 
            self.game.screen.blit(self.left_arrow, (200, 560)) 
            self.game.screen.blit(self.right_arrow, (260, 560))
            self.game.screen.blit(self.player_image, (340, 570))
           
            
            if self.blink_time > 1:
                self.draw_text("Press [ENTER] to play",  self.game.font_pixeled15, 'white', self.game.s.screen_width /2, self.game.s.screen_heigth - 50)

            if self.game.pause_time(50, True): #50
                self.title_active = False

        else:

            self.draw_text("HIGH SCORES", self.game.font_y22436, '#45ea1d', self.game.s.screen_width /2, self.game.s.screen_heigth / 9)
            
            self.show_hiscore_list()
            
            # give a pause before changing to title game screen
            if self.game.pause_time(35, True):
                self.title_active = True


    def check_input(self):
        """Check player input events"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()              

            if event.type == pygame.KEYDOWN:
                if self.title_active:
                    if event.key == pygame.K_RETURN:
                        self.game.s.menu_stars = False
                        self.game.s.moving_stars = True
                        self.run_display = False
                        self.game.playing = True
                        self.game.ship_thruster_sound.play()
                        self.game.s.ship_thruster_on = True
                       

                if event.key == pygame.K_ESCAPE:
                    sys.exit()

    def display_menu(self):
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
            self.game.crt.draw()   
            pygame.display.flip()
            self.game.clock.tick(60)


class GameOver (Menu):
    def __init__(self, game):
        Menu.__init__(self, game)

        self.count = 1

    def game_over_menu(self):
        """Show the game over text on screen and stop the game"""
        self.count += 0.1
        self.game.display_score()
        self.game.display_hiscore()
        self.game.display_level()
        self.game.stars.draw(self.game.screen)
        self.game.planets.draw(self.game.screen) 
        self.game.blocks.draw(self.game.screen)
        self.game.aliens.draw(self.game.screen)
        if self.count < 2:
            self.game.screen.blit(self.game.explosion_player, (self.game.player_sprite.rect.x, self.game.player_sprite.rect.y))
        self.draw_text("GAME OVER", self.game.font_pixeled80, "#3F0422", self.game.screen_rect.centerx + 10, self.game.screen_rect.centery + 10)
        self.draw_text("GAME OVER", self.game.font_pixeled80, '#FF007F', self.game.screen_rect.centerx, self.game.screen_rect.centery)

        if self.game.pause_time(28, True):
            self.run_display = False
            if self.game.s.score > 0:
                self.game.verify_score()  
            else:  
                self.game.curr_menu = self.game.main_menu
                self.game.reset_game()
            

    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.game.screen.fill('black')
            self.game_over_menu()
            self.game.crt.draw()
            pygame.display.flip()
            self.game.clock.tick(60)


class Hiscore (Menu):
    def __init__(self, game):
        Menu.__init__(self, game)

        
        self.alphabet = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O',
             'P','Q','R','S','T','U','V','W','X','Y','Z','<', '+']
        self.alphabet_copy = self.alphabet[:]
     
        self.hiscore_initialize()
    
    def hiscore_initialize (self):
        # player name list.
        self.player_name = []
        # index variable of alphabet list.
        self.i = 0
        # space between letters on input hiscore screen.
        self.space = 0
        self.score_name = '#ff0000'
       
        
    def check_input(self):
        ''' get player input for hiscore '''
        # press left or right arrow to choose the letter on alphabet list.
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
                    if len(self.player_name) < 3 and self.i not in {26, 27}:    # i=24 is 'DEL'.
                        self.player_name.append(self.alphabet[self.i])     # save on player name list.
                        self.space += 80 # add a horizontal space after selecting the letter.
                        self.i = 0   # the alphabet list index jumps to the first letter.
                    # choose "ok" to save hiscore.
                    # select 'del' to delete the character and move to the previous character.
                    else:
                        if self.alphabet[self.i] == '<' and self.player_name:
                            self.player_name.pop()
                            self.space -= 80
                            self.i = 0

                        if self.alphabet[self.i] == '+':
                            self.game.s.name = "".join(self.player_name).ljust(3, ".")
                            self.game.save_hiscore()
                            pygame.mixer.stop()
                            self.run_display = False
                            self.game.curr_menu = self.game.main_menu
                            self.game.reset_game()

    def display_letters(self):
        # If the first letter is chosen, display it on the screen.
        if len(self.player_name) > 0:
            first_letter = self.game.font_y22472.render(self.player_name[0], True, self.score_name)
            self.game.screen.blit(first_letter, (500, self.game.s.screen_heigth / 3))
        # If the second letter is chosen, display it on the screen.
        if len(self.player_name) > 1:
            second_letter = self.game.font_y22472.render(self.player_name[1], True, self.score_name)
            self.game.screen.blit(second_letter, (580, self.game.s.screen_heigth / 3))
        # If the third letter is chosen, display it on the screen.
        if len(self.player_name) > 2:
            last_letter = self.game.font_y22472.render(self.player_name[2], True, self.score_name)
            self.game.screen.blit(last_letter, (660, self.game.s.screen_heigth / 3))
        # if three letters are choosen shrink the alphabet list to two options, 'end' or 'del'.
            self.alphabet = ['<', '+']
        else:
            # if choosen letters are minor than three, the alphabet list remains full.
            self.alphabet = self.alphabet_copy

        # displays the letter on the screen for the player to choose using the arrow keys.
        choose_letters = self.game.font_y22472.render(self.alphabet[self.i], True, self.score_name)
        self.game.screen.blit(choose_letters, (500 + self.space, self.game.s.screen_heigth / 3))
        traces = self.game.font_y22472.render("___", True, self.score_name)  
        self.game.screen.blit(traces, (500, self.game.s.screen_heigth / 3 + 15))
        self.game.screen.blit(self.left_arrow, (520, self.game.s.screen_heigth / 3 + 120)) 
        self.game.screen.blit(self.right_arrow, (590, self.game.s.screen_heigth / 3 + 120)) 
        self.game.screen.blit( self.ctrl_key, (660, self.game.s.screen_heigth / 3 + 120)) 
       

    def display_menu(self):
        self.run_display = True
        while self.run_display:                         
            self.game.screen.fill("black")
            self.blink_text()
            self.game.stars.draw(self.game.screen)
            self.game.stars.update()
            if self.blink_time >= 1.5:
                self.draw_text("HIGH SCORES", self.game.font_y22436, 'green', self.game.s.screen_width /2, 40)
            self.hi_color = self.first_color = self.second_color = self.third_color = '#404040'
            self.show_hiscore_list()
            
            self.check_input()
            self.display_letters()             
            pygame.display.flip()
            self.game.clock.tick(60)

class BeatGame (Menu):
    def __init__(self, game):
        Menu.__init__(self, game)

        self.unlock_input = False
        self.bonus = 0

    def end_game_bonus (self):
        if self.game.s.activate_bonus:
            if not self.game.s.executed_bonus:
                self.game.bonus_sound.play()
                self.game.s.lives += 1
                self.bonus = self.game.s.lives * self.game.s.bonus
                self.game.s.score += self.bonus
                self.game.s.executed_bonus = True
            self.draw_text(f"BONUS  {self.game.s.bonus} X {self.game.s.lives} LIVES = {self.bonus}" , self.game.font_y22424, '#00ff00', self.game.s.screen_width / 2, self.game.s.screen_heigth / 5)
            
    
    def end_game(self):
        self.blink_text()
        self.draw_text("CONGRATULATIONS", self.game.font_y22424, '#fff01f', self.game.s.screen_width /2, self.game.s.screen_heigth / 3)
        self.draw_text("You defended our entire solar system", self.game.font_y22424, 'white', self.game.s.screen_width /2, self.game.s.screen_heigth / 3 + 60)
        self.draw_text("and drove the alien armada back", self.game.font_y22424, 'white', self.game.s.screen_width /2, self.game.s.screen_heigth / 3 + 120)
        self.draw_text("to the far reaches of the universe", self.game.font_y22424, 'white', self.game.s.screen_width /2, self.game.s.screen_heigth / 3 + 180)
        self.draw_text("Your job is done", self.game.font_y22424, 'white', self.game.s.screen_width /2, self.game.s.screen_heigth / 3 + 240)
        self.draw_text("you can now return to Earth", self.game.font_y22424, 'white', self.game.s.screen_width /2, self.game.s.screen_heigth / 3 + 300)
        if self.game.pause_time(50, True):
            self.game.s.activate_bonus = True
            self.unlock_input = True
            
            

    def check_input(self):
        """Check player input events"""
        if self.unlock_input:
            if self.blink_time > 1:
                self.draw_text("Press [ENTER] to continue",  self.game.font_pixeled15, 'white', self.game.s.screen_width /2, self.game.s.screen_heigth - 50)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()              

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        pygame.mixer.stop()
                        self.run_display = False
                        self.game.verify_score()  


    def display_menu(self):
        self.game.beat_game_sound.play()
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
            self.game.crt.draw()
            self.check_input()
            pygame.display.flip()
            self.game.clock.tick(60)