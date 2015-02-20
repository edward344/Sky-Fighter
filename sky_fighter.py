#!/usr/bin/env python

import pygame, random

class Explosion(object):
    def __init__(self):
        #-----load images-----------------------------------------------
        self.images = []
        img = pygame.image.load("explosion01.png").convert()
        img.set_colorkey((0,0,0))
        self.images.append(img)
        img = pygame.image.load("explosion02.png").convert()
        img.set_colorkey((0,0,0))
        self.images.append(img)
        img = pygame.image.load("explosion03.png").convert()
        img.set_colorkey((0,0,0))
        self.images.append(img)
        img = pygame.image.load("explosion04.png").convert()
        img.set_colorkey((0,0,0))
        self.images.append(img)
        img = pygame.image.load("explosion05.png").convert()
        img.set_colorkey((0,0,0))
        self.images.append(img)
        img = pygame.image.load("explosion06.png").convert()
        img.set_colorkey((0,0,0))
        self.images.append(img)
        img = pygame.image.load("explosion07.png").convert()
        img.set_colorkey((0,0,0))
        self.images.append(img)
        img = pygame.image.load("explosion08.png").convert()
        img.set_colorkey((0,0,0))
        self.images.append(img)
        img = pygame.image.load("explosion09.png").convert()
        img.set_colorkey((0,0,0))
        self.images.append(img)
        img = pygame.image.load("explosion10.png").convert()
        img.set_colorkey((0,0,0))
        self.images.append(img)
        img = pygame.image.load("explosion11.png").convert()
        img.set_colorkey((0,0,0))
        self.images.append(img)
        img = pygame.image.load("explosion12.png").convert()
        img.set_colorkey((0,0,0))
        self.images.append(img)
        img = pygame.image.load("explosion13.png").convert()
        img.set_colorkey((0,0,0))
        self.images.append(img)
        img = pygame.image.load("explosion14.png").convert()
        img.set_colorkey((0,0,0))
        self.images.append(img)
        img = pygame.image.load("explosion15.png").convert()
        img.set_colorkey((0,0,0))
        self.images.append(img)
        
        self.explosion_list = []
        
        #---------load Sound Effects------------------------------------
        
        self.explosion_sound = pygame.mixer.Sound("explosion.ogg")

    def add(self,pos):
        self.explosion_list.append([pos,0]) # the second argument is for the frame number;
        self.explosion_sound.play()
            
    def draw(self,screen):
        if len(self.explosion_list) > 0:
            for item in self.explosion_list:
                screen.blit(self.images[item[1]],item[0])
                if len(self.images) > item[1] +1:
                    item[1] += 1
                else:
                    self.explosion_list.remove(item)

class Enemy(pygame.sprite.Sprite):
    tick = 15
    projectile_image = None
    def __init__(self,img,projectile_list,tick_delay):
        pygame.sprite.Sprite.__init__(self)
        self.image = img
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.topleft = (random.randint(0,525),-50)
        if self.rect.x < 105:
            self.speed_x = random.randint(0,5)
        elif self.rect.x < 210:
            self.speed_x = random.randint(-1,5)
        elif self.rect.x < 315:
            self.speed_x = random.randint(-3,3)
        elif self.rect.x < 420:
            self.speed_x = random.randint(-5,-1)
        else:
            self.speed_x = random.randint(-5,0)
        self.projectile_list = projectile_list
        self.speed_y = random.randint(3,7)
        self.tick_delay = tick_delay
        
    def update(self):
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y
        
        if self.tick == 0:
            projectile = Projectile(self.rect.center,self.projectile_image)
            projectile.speed_x = self.speed_x
            projectile.speed_y = 10
            self.projectile_list.add(projectile)
            self.tick = self.tick_delay
        else:
            self.tick -= 1

class Missile(pygame.sprite.Sprite):
    speed_x = 0
    speed_y = 0
    def __init__(self,pos,img):
        pygame.sprite.Sprite.__init__(self)
        self.image = img
        self.rect = self.image.get_rect()
        self.rect.center = pos
        
    def update(self):
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y
        
class Projectile(Missile):
    def __init__(self,pos,img):
        Missile.__init__(self,pos,img)
        self.mask = pygame.mask.from_surface(self.image)
        

class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("fighter.png").convert()
        self.image.set_colorkey((0,0,0))
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)

    def update(self):
        self.rect.center = pygame.mouse.get_pos()
        
        
class Game(object):
    display_help_screen = False
    display_credits_screen = False
    texture_increment = -480
    tick = 30 # 30 fps = 1 second
    tick_delay = 35
    level = 1
    running = False
    menu_choice = 0
    score_text = None
    level_text = None
    def __init__(self):
        self.player = Player()
        self.player_list = pygame.sprite.Group()
        self.enemy_list = pygame.sprite.Group()
        self.missile_list = pygame.sprite.Group()
        self.projectile_list = pygame.sprite.Group()
        self.player_list.add(self.player)
        #---------------------------------------------------------------
        self.font = pygame.font.Font(None,25) # text font...
        self.menu_font = pygame.font.Font(None,40) # Menu font...
        self.menu_text = []
        #-----------Menu Texts------------------------------------------
        txt = self.menu_font.render("START",True,(255,0,0))
        self.menu_text.append(txt)
        txt = self.menu_font.render("HELP",True,(255,0,0))
        self.menu_text.append(txt)
        txt = self.menu_font.render("CREDITS",True,(255,0,0))
        self.menu_text.append(txt)
        txt = self.menu_font.render("EXIT",True,(255,0,0))
        self.menu_text.append(txt)
        #-----------load images-----------------------------------------
        self.ocean_texture = pygame.image.load("ocean_texture.png").convert()
        self.enemy_images = []
        img = pygame.image.load("enemy_1.png").convert()
        img.set_colorkey((0,0,0))
        self.enemy_images.append(img)
        img = pygame.image.load("enemy_2.png").convert()
        img.set_colorkey((0,0,0))
        self.enemy_images.append(img)
        img = pygame.image.load("enemy_3.png").convert()
        img.set_colorkey((0,0,0))
        self.enemy_images.append(img)
        self.missile_image = pygame.image.load("missile.png").convert()
        self.missile_image.set_colorkey((0,0,0))
        self.projectile_image = pygame.image.load("projectile.png").convert()
        self.projectile_image.set_colorkey((0,0,0))
        self.explosion_image = pygame.image.load("explosion01.png").convert()
        self.explosion_image.set_colorkey((0,0,0))
        self.game_over_image = pygame.image.load("game_over.png").convert()
        self.game_over_image.set_colorkey((0,0,0))
        self.help_image = pygame.image.load("help_image.png").convert()
        self.help_image.set_colorkey((255,255,255))
        self.credits_image = pygame.image.load("credits_image.png").convert()
        self.credits_image.set_colorkey((255,255,255))
        self.intro_image = pygame.image.load("intro_image.png").convert()
        #--------------load Sounds--------------------------------------
        self.plane_sound = pygame.mixer.Sound("plane.ogg")
        #---------------------------------------------------------------
        self.explosion = Explosion()

    def scroll_menu_up(self):
        if self.menu_choice > 0:
            self.menu_choice -= 1
            
    def scroll_menu_down(self):
        if self.menu_choice +1 < len(self.menu_text):
            self.menu_choice += 1
            

    def start_game(self):
        self.running = True
        self.plane_sound.play(-1) # Start the plane sound; 
        self.terminate_count_down = 150
        self.terminate = False
        self.score = 0
        if len(self.enemy_list) > 0:
            self.enemy_list.empty()
        if len(self.missile_list) > 0:
            self.missile_list.empty()
        if len(self.projectile_list) > 0:
            self.projectile_list.empty()
        self.tick_delay = 35
        self.level = 1
        self.score_text = self.font.render("Score: 0",True,(255,255,255))
        self.level_text = self.font.render("Level: 1",True,(255,255,255))
        
    def run_game(self):
        if not self.terminate:
            self.player.update()
        self.enemy_list.update()
        self.missile_list.update()
        self.projectile_list.update()
        
        for missile in self.missile_list:
            if missile.rect.x < 0 or missile.rect.x > 640:
                self.missile_list.remove(missile)
            elif missile.rect.y < - 40 or missile.rect.y > 480:
                self.missile_list.remove(missile)
                
        for projectile in self.projectile_list:
            if projectile.rect.x < 0 or projectile.rect.x > 640:
                self.projectile_list.remove(projectile)
            elif projectile.rect.y < - 20 or projectile.rect.y > 480:
                self.projectile_list.remove(projectile)
                
        for enemy in self.enemy_list:
            if enemy.rect.x < -120 or enemy.rect.x > 640:
                self.enemy_list.remove(enemy)
            elif enemy.rect.y < -100 or enemy.rect.y > 480:
                self.enemy_list.remove(enemy)
                
        for enemy in self.enemy_list:
            hit_list = pygame.sprite.spritecollide(enemy,self.missile_list,True)
            if len(hit_list) > 0:
                self.explosion.add((enemy.rect.x +20,enemy.rect.y +20))
                self.enemy_list.remove(enemy)
                self.score += 1
                if self.level == 1:
                    if self.score == 50:
                        self.level += 1
                        self.tick_delay = 25
                        self.level_text = self.font.render("Level: " + str(self.level),True,(255,255,255))
                elif self.level == 2:
                    if self.score == 100:
                        self.level += 1
                        self.tick_delay = 15
                        self.level_text = self.font.render("Level: " + str(self.level),True,(255,255,255))
                self.score_text = self.font.render("Score: " + str(self.score),True,(255,255,255))
                
                
        hit_list = pygame.sprite.spritecollide(self.player,self.enemy_list,False,pygame.sprite.collide_mask)
        if len(hit_list) > 0 and not self.terminate:
            self.terminate = True
            self.explosion.add(self.player.rect.topleft)
            self.plane_sound.stop()
            for enemy in hit_list:
                self.explosion.add(enemy.rect.topleft)
                self.enemy_list.remove(enemy)
            
        hit_list = pygame.sprite.spritecollide(self.player,self.projectile_list,False,pygame.sprite.collide_mask)
        if len(hit_list) > 0 and not self.terminate:
            self.terminate = True
            self.explosion.add(self.player.rect.topleft)
            self.plane_sound.stop()
            for projectile in hit_list:
                self.projectile_list.remove(projectile)
        
        if self.tick == 0:
            enemy = Enemy(random.choice(self.enemy_images),self.projectile_list,self.tick_delay)
            enemy.projectile_image = self.projectile_image
            self.enemy_list.add(enemy)
            self.tick = self.tick_delay
        else:
            self.tick -= 1
            
        if self.texture_increment == 0:
            self.texture_increment = -480
        else:
            self.texture_increment += 1
            
        if self.terminate:
            if self.terminate_count_down == 0:
                self.running = False
            else:
                self.terminate_count_down -= 1
        
    def display_frame(self,screen):
        if self.running:
            screen.blit(self.ocean_texture,(0,self.texture_increment))
            self.missile_list.draw(screen)
            self.projectile_list.draw(screen)
            self.enemy_list.draw(screen)
            if not self.terminate:
                self.player_list.draw(screen)
            screen.blit(self.score_text,(75,20))
            screen.blit(self.level_text,(285,20))
            self.explosion.draw(screen)
            if self.terminate_count_down <= 90:
                screen.blit(self.game_over_image,(100,145))
        elif self.display_credits_screen:
            screen.blit(self.intro_image,(0,0))
            screen.blit(self.credits_image,(80,100))
        elif self.display_help_screen:
            screen.blit(self.intro_image,(0,0))
            screen.blit(self.help_image,(70,50))
        else:
            screen.blit(self.intro_image,(0,0))
            increment = 100
            for text in self.menu_text:
                screen.blit(text,(135,increment))
                increment += 50
            pygame.draw.rect(screen,(0,0,255),[125,90 + self.menu_choice * 50,160,45],3)
        
    def shoot(self):
        missile = Missile(self.player.rect.center,self.missile_image)
        missile.speed_y = -10
        self.missile_list.add(missile)
        
def main():
    
    pygame.init()

    # Set the width and height of the screen [width, height]
    
    screen = pygame.display.set_mode((640,480))

    pygame.display.set_caption("Sky Fighter")
    
    #-------------make the mouse cursor invisible-------------------
    pygame.mouse.set_visible(False)
    
    #Loop until the user clicks the close button.
    done = False
    
    # Used to manage how fast the screen updates
    clock = pygame.time.Clock()
    #------------------------------------------------
    game = Game()
    # -------- Main Program Loop ---------------------------------------
    while not done:
        # --- Main event loop
        for event in pygame.event.get(): # User did something
            if event.type == pygame.QUIT: # If user clicked close
                done = True # Flag that we are done so we exit this loop
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                game.shoot()
                
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if not game.running:
                        #------The user's menu selection----------------
                        if game.menu_choice == 0:
                            game.start_game()
                        elif game.menu_choice == 1:
                            game.display_help_screen = True
                        elif game.menu_choice == 2:
                            game.display_credits_screen = True
                        elif game.menu_choice == 3:
                            done = True
                        
                elif event.key == pygame.K_UP:
                    game.scroll_menu_up()
                elif event.key == pygame.K_DOWN:
                    game.scroll_menu_down()
                    
                elif event.key == pygame.K_ESCAPE:
                    if game.running:
                        game.running = False
                        game.plane_sound.stop()
                    else:
                        game.display_help_screen = False
                        game.display_credits_screen = False

        # --- Game logic should go here
        if game.running:
            game.run_game()
        # First, clear the screen to white. Don't put other drawing commands
        # above this, or they will be erased with this command.
        screen.fill((255,255,255))

        # --- Drawing code should go here
        game.display_frame(screen)
        # --- Go ahead and update the screen with what we've drawn.
        pygame.display.flip()

        # --- Limit to 30 frames per second
        clock.tick(30)

    # Close the window and quit.
    # If you forget this line, the program will 'hang'
    # on exit if running from IDLE.
    pygame.quit()

if __name__ == '__main__':
    main()

