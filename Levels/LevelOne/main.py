from colorsys import rgb_to_hls
import pygame, time, random, math
from pytmx.util_pygame import load_pygame


from tile import Tile
from player import Player
from boss import Boss
from constants import *


display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

sprite_group = pygame.sprite.Group()

clock = pygame.time.Clock()

#Initiailize pygame
pygame.init()

# video tmx code
tmx_data = load_pygame('./Levels/levelOne/maps/levelOne.tmx')


land_sprite_group = pygame.sprite.Group()

# cycle through all layers
for layer in tmx_data.visible_layers:
    if hasattr(layer,'data'):
        for x, y, surf in layer.tiles():
            # for tile in layer.tiles():
                # NOTE: here i need to check if the tile is an edge tile , use the ID of the edge tile to check this, just am not sure 
                # how to do that because the documentation is so shit and basic 
            pos = (x * 31, y * 32)
            temp = Tile(pos = pos, surf = surf, groups = sprite_group)
            if layer.name in ('Collisions'):
                land_sprite_group.add(temp)





my_player_group = pygame.sprite.Group()
boss_group = pygame.sprite.Group()

my_player = Player(164, 164, land_sprite_group)
my_player_group.add(my_player)

boss_chomper = Boss(600, 385)
boss_group.add(boss_chomper)





class Game():
    def __init__(self):
        self.player_lives = 3

        self.custom_font = pygame.font.Font('./Levels/LevelOne/fonts/ARCADECLASSIC.ttf', 32)

        self.player_lives_text = self.custom_font.render("Lives", True, BEIGE)
        self.player_lives_text_rect = self.player_lives_text.get_rect()
        self.player_lives_text_rect.center = (65, 35)

        self.boss_health_text = self.custom_font.render("Health", True, BEIGE)
        self.boss_health_text_rect = self.boss_health_text.get_rect()
        self.boss_health_text_rect.center = (WINDOW_WIDTH - 300, 35)

        self.heart = pygame.transform.scale(pygame.image.load("./Levels/LevelOne/images/heart.png").convert_alpha(), (48, 48))
        self.boss_health = 1


    def update(self):
        self.check_collisions(my_player, boss_chomper)
        self.check_game_over()
        self.draw_hearts()
        self.draw_health_bar()


    def draw_health_bar(self):
        # outline for the health bar: 
        pygame.draw.line(display_surface, (255, 20, 20), (WINDOW_WIDTH - 225, 22), (WINDOW_WIDTH - 25, 22), 4)
        pygame.draw.line(display_surface, (255, 20, 20), (WINDOW_WIDTH - 225, 42), (WINDOW_WIDTH - 25, 42), 4)
        pygame.draw.line(display_surface, (255, 20, 20), (WINDOW_WIDTH - 225, 22), (WINDOW_WIDTH - 225, 42), 4)
        pygame.draw.line(display_surface, (255, 20, 20), (WINDOW_WIDTH - 25, 22), (WINDOW_WIDTH - 25, 42), 4)

        # fill for the health bar: 
        pygame.draw.rect(display_surface, (0, 255, 0), pygame.Rect(WINDOW_WIDTH - 223, 24, 195 * self.boss_health, 18))

        display_surface.blit(self.boss_health_text, self.boss_health_text_rect)
        

    def boss_hurt(self):
        self.boss_health -= 0.1


    def draw_hearts(self):
        # can't do a "if change needed" because the hearts need to be drawn every frame since the back
        
        for i in range(math.ceil(self.player_lives)):
            if self.player_lives % 1 != 0 and i is math.floor(self.player_lives):
                self.heart = pygame.transform.scale(pygame.image.load("./Levels/LevelOne/images/half-heart.png").convert_alpha(), (48, 48))
            else:
                self.heart = pygame.transform.scale(pygame.image.load("./Levels/LevelOne/images/heart.png").convert_alpha(), (48, 48))
            self.heart_rect = self.heart.get_rect(  ) # sets a rectangle that surrounds the surface, use this to position
            self.heart_rect.topleft = (130 + (i * 52), 10) # can position multiple ways
            display_surface.blit(self.heart, self.heart_rect)
        
        display_surface.blit(self.player_lives_text, self.player_lives_text_rect)

    def check_collisions(self, player, boss):
        # Check for collisions between player and boss
        collision_list = pygame.sprite.spritecollide(player, [boss], False, pygame.sprite.collide_mask)
        for collided in collision_list:
            if not collided.collision_occurred and player.is_attacking and not boss.attacking:
                boss.is_hurting = True
                self.boss_hurt()
                collided.collision_occurred = True
            elif not collided.collision_occurred and not player.is_attacking and boss.attacking:
                player.is_hurting = True
                self.player_lives_update(0.5)
                collided.collision_occurred = True
            elif player.is_attacking and boss.attacking and not collided.collision_occurred:
                self.player_lives_update(0.5)
                self.boss_hurt()
                boss.is_hurting = True
                player.is_hurting = True
        if len(collision_list) == 0:
            boss.collision_occurred = False

    def check_game_over(self):
        if self.player_lives <= 0:
            # player lost 
            my_player.is_dying = True
            my_player.able_to_move = False
            self.player_death_animation()
            self.show_player_loss_screen()
        elif self.boss_health <= 0.09:
            boss_chomper.is_dying = True
            boss_chomper.able_to_move = False
            self.boss_death_animation()
            self.show_player_win_screen()


    def player_death_animation(self):
        # here i just want the player to go through a whole cycle of animations, and 
        # then i want the game to show the death screen 
        if my_player.right:
            death_frames = my_player.death_right_frames # a list of death frames
        else:
            death_frames = my_player.death_left_frames # a list of death frames
        delay = 200 # the delay between each frame in milliseconds

        for frame in death_frames:
            # currently have it so that everything goes away except the player 
            my_player.image = frame
            # redraw the screen
            my_player_group.draw(display_surface)
            pygame.display.flip()
            pygame.time.delay(delay)
            display_surface.fill('black')
            sprite_group.draw(display_surface)

    
    def boss_death_animation(self):
        # here i just want the player to go through a whole cycle of animations, and 
        # then i want the game to show the death screen 
        if boss_chomper.right:
            death_frames = boss_chomper.death_right_frames # a list of death frames
        else:
            death_frames = boss_chomper.death_left_frames # a list of death frames

        delay = 400 # the delay between each frame in milliseconds

        for frame in death_frames:
            # currently have it so that everything goes away except the player 
            boss_chomper.image = frame
            # redraw the screen
            boss_group.draw(display_surface)
            my_player_group.draw(display_surface)

            pygame.display.flip()
            pygame.time.delay(delay)
            display_surface.fill('black')
            sprite_group.draw(display_surface)

        # pause the animation for a few seconds
        pygame.time.wait(3000)


    def show_player_loss_screen(self):
        game_over = True

        WHITE = (255, 255, 255)
        BLACK = (0, 0, 0)

        main_text = self.custom_font.render("GAME OVER", True, WHITE)
        main_rect = main_text.get_rect()
        main_rect.center = (WINDOW_WIDTH//2, WINDOW_HEIGHT//2)

        retry_text = self.custom_font.render("Press Y to retry", True, WHITE)
        exit_text = self.custom_font.render("Press N to exit", True, WHITE)

        retry_rect = retry_text.get_rect()
        retry_rect.center = (WINDOW_WIDTH//2, WINDOW_HEIGHT//2 + 50)

        exit_rect = exit_text.get_rect()
        exit_rect.center = (WINDOW_WIDTH//2, WINDOW_HEIGHT//2 + 100)

        #Display the pause text
        display_surface.fill(BLACK)
        display_surface.blit(main_text, main_rect)
        display_surface.blit(retry_text, retry_rect)
        display_surface.blit(exit_text, exit_rect)

        pygame.display.update()
        while game_over:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_y:
                        self.reset()
                        game_over = False
                    if event.key == pygame.K_n:
                        # here we need to go back to the level selector
                        pass

    def show_player_win_screen(self):
        WHITE = (255, 255, 255)
        BLACK = (0, 0, 0)

        game_over = True

        #Create main pause text
        main_text = self.custom_font.render("YOU WON", True, WHITE)
        main_rect = main_text.get_rect()
        main_rect.center = (WINDOW_WIDTH//2, WINDOW_HEIGHT//2)

        continue_text = self.custom_font.render("PRESS ENTER TO CONTINUE", True, WHITE)
        continue_rect = main_text.get_rect()
        continue_rect.center = (WINDOW_WIDTH//2 - 150, WINDOW_HEIGHT//2 + 50)
        
        #Display the pause text
        display_surface.fill(BLACK)
        display_surface.blit(main_text, main_rect)
        display_surface.blit(continue_text, continue_rect)
        
        pygame.display.update()
        while game_over:
            for event in pygame.event.get():    
                #User wants to quit
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        game_over = False
                        self.reset()
                        # go to the level selector
                        pass


    def reset(self):
        self.player_lives = 3
        self.boss_health = 1
        boss_chomper.rect.bottomleft = (600, 385)
        my_player.position = (164, 164)
        my_player.able_to_move = True
        my_player.is_hurting = False
        my_player.is_attacking = False
        boss_chomper.is_dying = False
        boss_chomper.able_to_move = True
        boss_chomper.is_hurting = False
        boss_chomper.attacking = False

    
    def player_lives_update(self, lives):
        self.player_lives -= lives
        self.update_needed = True

    def pause_game(self, main_text, sub_text):
        """Pause the game"""
        global running

        pygame.mixer.music.pause()

        #Set colors
        WHITE = (255, 255, 255)
        BLACK = (0, 0, 0, 0)
        GREEN = (25, 200, 25)
        BLUE = (240, 248, 255)

        #Create main pause text
        main_text = self.custom_font.render(main_text, True, GREEN)
        main_rect = main_text.get_rect()
        main_rect.center = (WINDOW_WIDTH//2, WINDOW_HEIGHT//2)

        #Create sub pause text
        sub_text = self.custom_font.render(sub_text, True, BLACK)
        sub_rect = sub_text.get_rect()
        sub_rect.center = (WINDOW_WIDTH//2, WINDOW_HEIGHT//2 + 64)

        #Display the pause text
        # display_surface.fill(BLACK)
        pygame.draw.rect(display_surface, BLUE, pygame.Rect(150, 110, 475, 300))
        display_surface.blit(main_text, main_rect)
        display_surface.blit(sub_text, sub_rect)
        pygame.display.update()

        #Pause the game until user hits enter or quits
        is_paused = True
        while is_paused:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    #User wants to continue
                    if event.key == pygame.K_RETURN:
                        is_paused = False
                        pygame.mixer.music.unpause()
                #User wants to quit
                if event.type == pygame.QUIT:
                    is_paused = False
                    running = False
                    pygame.mixer.music.stop()


my_game = Game()



running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False 
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE or event.key == pygame.K_UP or event.key == pygame.K_w:
                my_player.is_jumping = True
                my_player.jump()
            if event.key == pygame.K_ESCAPE:
                my_game.pause_game("Paused", "Press    enter     to     play")
            if event.key == pygame.K_1:
                my_player.attack(1)
            if event.key == pygame.K_2:
                my_player.attack(2)


    # high level loop progression: screen goes black, tiles get loaded, player and boss update position and get redrawn, 
    # game updates, screen updates, repeat 

    display_surface.fill('black')
    sprite_group.draw(display_surface)


    my_player_group.update()
    my_player_group.draw(display_surface)
    # pygame.draw.rect(display_surface, (255, 255, 255), my_player.rect)

    boss_group.update()
    boss_group.draw(display_surface)
    # pygame.draw.rect(display_surface, (255, 255, 255), boss_chomper.rect)

    my_game.update()
    # display_surface.blit(heart, heart_rect)

    pygame.display.flip()

    clock.tick(FPS)


pygame.quit()