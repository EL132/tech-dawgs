from colorsys import rgb_to_hls
import pygame, time
from pytmx.util_pygame import load_pygame


#Use 2D vectors
vector = pygame.math.Vector2

#Initiailize pygame
pygame.init()

#Set display surface (tile size is 32x32 ; 25 tiles wide, 14 tiles high)
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 448
display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
sprite_group = pygame.sprite.Group()


#Set FPS and clock
FPS = 60
clock = pygame.time.Clock()



# classes
class Tile(pygame.sprite.Sprite):
	def __init__(self,pos,surf,groups):
		super().__init__(groups)
		self.image = surf
		self.rect = self.image.get_rect(topleft = pos)


class Player(pygame.sprite.Sprite):
    # parameters are TBD for grass and water tiles
    def __init__(self, x, y, land_tiles, water_tiles):
        super().__init__()

        # animation frames ::
        self.move_right_sprites = []
        self.move_left_sprites = []
        self.idle_right_sprites = []
        self.idle_left_sprites = []

        # adding the moving right frames
        self.move_right_sprites.append(pygame.transform.scale(pygame.image.load('./levelOne/images/player/boy/Run (1).png'), (64, 64)))
        self.move_right_sprites.append(pygame.transform.scale(pygame.image.load('./levelOne/images/player/boy/Run (2).png'), (64, 64)))
        self.move_right_sprites.append(pygame.transform.scale(pygame.image.load('./levelOne/images/player/boy/Run (3).png'), (64, 64)))
        self.move_right_sprites.append(pygame.transform.scale(pygame.image.load('./levelOne/images/player/boy/Run (4).png'), (64, 64)))
        self.move_right_sprites.append(pygame.transform.scale(pygame.image.load('./levelOne/images/player/boy/Run (5).png'), (64, 64)))
        self.move_right_sprites.append(pygame.transform.scale(pygame.image.load('./levelOne/images/player/boy/Run (6).png'), (64, 64)))
        self.move_right_sprites.append(pygame.transform.scale(pygame.image.load('./levelOne/images/player/boy/Run (7).png'), (64, 64)))
        self.move_right_sprites.append(pygame.transform.scale(pygame.image.load('./levelOne/images/player/boy/Run (8).png'), (64, 64)))

        # adding the moving left frames
        self.move_left_sprites.append(pygame.transform.flip(pygame.transform.scale(pygame.image.load('./levelOne/images/player/boy/Run (1).png'), (64, 64)), True, False))
        self.move_left_sprites.append(pygame.transform.flip(pygame.transform.scale(pygame.image.load('./levelOne/images/player/boy/Run (2).png'), (64, 64)), True, False))
        self.move_left_sprites.append(pygame.transform.flip(pygame.transform.scale(pygame.image.load('./levelOne/images/player/boy/Run (3).png'), (64, 64)), True, False))
        self.move_left_sprites.append(pygame.transform.flip(pygame.transform.scale(pygame.image.load('./levelOne/images/player/boy/Run (4).png'), (64, 64)), True, False))
        self.move_left_sprites.append(pygame.transform.flip(pygame.transform.scale(pygame.image.load('./levelOne/images/player/boy/Run (5).png'), (64, 64)), True, False))
        self.move_left_sprites.append(pygame.transform.flip(pygame.transform.scale(pygame.image.load('./levelOne/images/player/boy/Run (6).png'), (64, 64)), True, False))
        self.move_left_sprites.append(pygame.transform.flip(pygame.transform.scale(pygame.image.load('./levelOne/images/player/boy/Run (7).png'), (64, 64)), True, False))
        self.move_left_sprites.append(pygame.transform.flip(pygame.transform.scale(pygame.image.load('./levelOne/images/player/boy/Run (8).png'), (64, 64)), True, False))

        # idle left frames 
        self.idle_left_sprites.append(pygame.transform.flip(pygame.transform.scale(pygame.image.load('./levelOne/images/player/boy/Idle (1).png'), (64, 64)), True, False))
        self.idle_left_sprites.append(pygame.transform.flip(pygame.transform.scale(pygame.image.load('./levelOne/images/player/boy/Idle (2).png'), (64, 64)), True, False))
        self.idle_left_sprites.append(pygame.transform.flip(pygame.transform.scale(pygame.image.load('./levelOne/images/player/boy/Idle (3).png'), (64, 64)), True, False))
        self.idle_left_sprites.append(pygame.transform.flip(pygame.transform.scale(pygame.image.load('./levelOne/images/player/boy/Idle (4).png'), (64, 64)), True, False))
        self.idle_left_sprites.append(pygame.transform.flip(pygame.transform.scale(pygame.image.load('./levelOne/images/player/boy/Idle (5).png'), (64, 64)), True, False))
        self.idle_left_sprites.append(pygame.transform.flip(pygame.transform.scale(pygame.image.load('./levelOne/images/player/boy/Idle (6).png'), (64, 64)), True, False))
        self.idle_left_sprites.append(pygame.transform.flip(pygame.transform.scale(pygame.image.load('./levelOne/images/player/boy/Idle (7).png'), (64, 64)), True, False))
        self.idle_left_sprites.append(pygame.transform.flip(pygame.transform.scale(pygame.image.load('./levelOne/images/player/boy/Idle (8).png'), (64, 64)), True, False))
        self.idle_left_sprites.append(pygame.transform.flip(pygame.transform.scale(pygame.image.load('./levelOne/images/player/boy/Idle (9).png'), (64, 64)), True, False))

        # idle right frames 
        self.idle_right_sprites.append(pygame.transform.scale(pygame.image.load('./levelOne/images/player/boy/Idle (1).png'), (64, 64)))
        self.idle_right_sprites.append(pygame.transform.scale(pygame.image.load('./levelOne/images/player/boy/Idle (2).png'), (64, 64)))
        self.idle_right_sprites.append(pygame.transform.scale(pygame.image.load('./levelOne/images/player/boy/Idle (3).png'), (64, 64)))
        self.idle_right_sprites.append(pygame.transform.scale(pygame.image.load('./levelOne/images/player/boy/Idle (4).png'), (64, 64)))
        self.idle_right_sprites.append(pygame.transform.scale(pygame.image.load('./levelOne/images/player/boy/Idle (5).png'), (64, 64)))
        self.idle_right_sprites.append(pygame.transform.scale(pygame.image.load('./levelOne/images/player/boy/Idle (6).png'), (64, 64)))
        self.idle_right_sprites.append(pygame.transform.scale(pygame.image.load('./levelOne/images/player/boy/Idle (7).png'), (64, 64)))
        self.idle_right_sprites.append(pygame.transform.scale(pygame.image.load('./levelOne/images/player/boy/Idle (8).png'), (64, 64)))
        self.idle_right_sprites.append(pygame.transform.scale(pygame.image.load('./levelOne/images/player/boy/Idle (9).png'), (64, 64)))

        # index of the current sprite 
        self.current_sprite = 0

        self.image = self.move_right_sprites[self.current_sprite]
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.bottomleft = (x, y)

        self.land_tiles = land_tiles
        self.water_tiles = water_tiles

        # vector stuff with position, velocity, and accel
        self.position = vector(x, y)
        self.velocity = vector(0, 0)
        self.acceleration = vector(0, 0)

        # kinematic constants
        self.HORIZONTAL_ACCELERATION = 0.7
        self.HORIZONTAL_FRICTION = 0.10
        self.VERTICAL_ACCELERATION = 0.25 # gravity 
        self.VERTICAL_JUMP_SPEED = 10


        # NEW CODE FOR IMPROVED COLLISION HERE:
        self.leg_hitbox_rect = pygame.Rect(self.x, self.y, 10, 15)
        print(self.leg_hitbox_rect)

        # create a mask
        self.mask = pygame.mask.from_surface(self.image, 4)






    def update(self):
        self.move()
        self.check_collisions()
        mask_outline = self.mask.outline() # this gives a list of points that are on the mask 
        pygame.draw.lines(self.image, (255, 0, 0), True, mask_outline)


    def move(self):
        self.acceleration = vector(0, self.VERTICAL_ACCELERATION)

        # for collision improvements
        self.leg_hitbox_rect.centery = self.position.y - 16
        pygame.draw.rect(display_surface, (255, 0, 0), self.leg_hitbox_rect, 1)
        left = False
        if left:
            self.leg_hitbox_rect.centerx = self.position.x + 6
        else:
            self.leg_hitbox_rect.centerx = self.position.x + 36


        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT]:
            left = True
            if self.position.x < 0:
                self.position.x = WINDOW_WIDTH
            self.acceleration.x = -1 * self.HORIZONTAL_ACCELERATION
            self.animate(self.move_left_sprites, 0.1)
        elif keys[pygame.K_RIGHT]:
            left = False
            if self.position.x > WINDOW_WIDTH:
                self.position.x = 0
            self.acceleration.x = self.HORIZONTAL_ACCELERATION    
            self.animate(self.move_right_sprites, 0.1)    
        else:
            if self.velocity.x > 0:
                self.animate(self.idle_right_sprites, 0.1)
            else:
                self.animate(self.idle_left_sprites, 0.1)

        # # calc new kinematic values 
        self.acceleration.x -= self.HORIZONTAL_FRICTION * self.velocity.x # this is for friction of the acceleration
        self.velocity += self.acceleration
        self.position += self.velocity + 0.5 * self.acceleration
        
        self.rect.bottomleft = self.position

        if self.position.y > WINDOW_HEIGHT:
            self.position.y = self.y

    def check_collisions(self):

        for tile in self.land_tiles:  
            # if pygame.sprite.collide_mask(self.mask.scale((15, 15)), tile):
            if pygame.sprite.collide_mask(self, tile):
                tile.mask = pygame.mask.from_surface(tile.image)
                tile_mask_outline = tile.mask.outline() # this gives a list of points that are on
                pygame.draw.lines(self.image, (255, 0, 0), True, tile_mask_outline)
                if self.velocity.y > 0:
                    self.position.y = tile.rect.top + 10
                    self.velocity.y = 0
        for tile in self.water_tiles:  
            if pygame.sprite.collide_mask(self, tile):
                self.position.x = self.x
                self.position.y = self.y
    
    def jump(self):
        if pygame.sprite.spritecollide(self, self.land_tiles, False):
            self.velocity.y = -1 * self.VERTICAL_JUMP_SPEED

    def animate(self, sprite_list, speed):
        # speed parameter used to limit how fast the animation goes 

        # loop through sprite list and change current sprite 
        if self.current_sprite < len(sprite_list) - 1:
            self.current_sprite += speed
        else:
            self.current_sprite = 0
        
        self.image = sprite_list[int(self.current_sprite)]





class BossOne(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        # animation frames ::
        self.move_right_sprites = []
        self.move_left_sprites = []
        self.idle_sprites = []
        self.attack_left_sprites = []
        self.attack_right_sprites = []

        # adding the moving right frames
        # self.move_right_sprites.append(pygame.transform.scale(pygame.image.load('./images/BossOne/Move/Right/Right 1.png'), (55.5, 87)))
        # self.move_right_sprites.append(pygame.transform.scale(pygame.image.load('./images/BossOne/Move/Right/Right 2.png'), (55.5, 87)))
        # self.move_right_sprites.append(pygame.transform.scale(pygame.image.load('./images/BossOne/Move/Right/Right 3.png'), (55.5, 87)))
        # self.move_right_sprites.append(pygame.transform.scale(pygame.image.load('./images/BossOne/Move/Right/Right 4.png'), (55.5, 87)))
        # self.move_right_sprites.append(pygame.transform.scale(pygame.image.load('./images/BossOne/Move/Right/Right 5.png'), (55.5, 87)))
        # self.move_right_sprites.append(pygame.transform.scale(pygame.image.load('./images/BossOne/Move/Right/Right 6.png'), (55.5, 87)))

        # self.move_left_sprites.append(pygame.transform.scale(pygame.image.load('./images/BossOne/Move/Left/Left 1.png'), (55.5, 87)))
        # self.move_left_sprites.append(pygame.transform.scale(pygame.image.load('./images/BossOne/Move/Left/Left 2.png'), (55.5, 87)))
        # self.move_left_sprites.append(pygame.transform.scale(pygame.image.load('./images/BossOne/Move/Left/Left 3.png'), (55.5, 87)))
        # self.move_left_sprites.append(pygame.transform.scale(pygame.image.load('./images/BossOne/Move/Left/Left 4.png'), (55.5, 87)))
        # self.move_left_sprites.append(pygame.transform.scale(pygame.image.load('./images/BossOne/Move/Left/Left 5.png'), (55.5, 87)))
        # self.move_left_sprites.append(pygame.transform.scale(pygame.image.load('./images/BossOne/Move/Left/Left 6.png'), (55.5, 87)))

        # self.idle_sprites.append(pygame.transform.scale(pygame.image.load('./images/BossOne/Idle/Idle 1.png'), (55.5, 87)))
        # self.idle_sprites.append(pygame.transform.scale(pygame.image.load('./images/BossOne/Idle/Idle 2.png'), (55.5, 87)))
        # self.idle_sprites.append(pygame.transform.scale(pygame.image.load('./images/BossOne/Idle/Idle 3.png'), (55.5, 87)))
        # self.idle_sprites.append(pygame.transform.scale(pygame.image.load('./images/BossOne/Idle/Idle 4.png'), (55.5, 87)))
        # self.idle_sprites.append(pygame.transform.scale(pygame.image.load('./images/BossOne/Idle/Idle 5.png'), (55.5, 87)))
        # self.idle_sprites.append(pygame.transform.scale(pygame.image.load('./images/BossOne/Idle/Idle 6.png'), (55.5, 87)))

        # self.attack_left_sprites.append(pygame.transform.scale(pygame.image.load('./images/BossOne/Attack/Left/Attack Left 1.png'), (55.5, 87)))
        # self.attack_left_sprites.append(pygame.transform.scale(pygame.image.load('./images/BossOne/Attack/Left/Attack Left 2.png'), (55.5, 87)))
        # self.attack_left_sprites.append(pygame.transform.scale(pygame.image.load('./images/BossOne/Attack/Left/Attack Left 3.png'), (55.5, 87)))

        # self.attack_right_sprites.append(pygame.transform.scale(pygame.image.load('./images/BossOne/Attack/Right/Attack Right 1.png'), (55.5, 87)))
        # self.attack_right_sprites.append(pygame.transform.scale(pygame.image.load('./images/BossOne/Attack/Right/Attack Right 2.png'), (55.5, 87)))
        # self.attack_right_sprites.append(pygame.transform.scale(pygame.image.load('./images/BossOne/Attack/Right/Attack Right 3.png'), (55.5, 87)))


        # index of the current sprite 
        # self.current_sprite = 0

        # self.image = self.move_right_sprites[self.current_sprite]
        # self.rect = self.image.get_rect()

        self.x = x
        self.y = y
        # self.rect.bottomleft = (x, y)

        self.turns = 0

        self.move_speed = 1
        self.right = True
    
    def update(self):
        self.move()


    def move(self):
        # i want this movement to be left then right then left then right...
        # i essentially want to have the x value get updated every frame until
        # a width parameter is reached
        # print(self.position)
        
        if self.right:
            self.rect.centerx += self.move_speed
            # print(self.rect.centerx) --> not changing  
            # print("position: ", self.position)
            # print("position individual: ", self.position[0])
            # # self.position[0] = self.rect[0]
            # print("rect: ", self.rect[0])
            self.animate(self.move_right_sprites, 0.1)
            if self.rect.x > WINDOW_WIDTH - 40:
                self.right = False
                self.turns += 1
        else:
            self.rect.x -= self.move_speed
            if self.turns % 2 == 0:
                self.animate(self.attack_left_sprites, 0.02)
            else:
                self.animate(self.move_left_sprites, 0.1)
            if self.rect.x < 500:
                self.right = True


    def animate(self, sprite_list, speed):
        # loop through sprite list and change current sprite 
        if self.current_sprite < len(sprite_list) - 1:
            self.current_sprite += speed
        else:
            self.current_sprite = 0
        
        self.image = sprite_list[int(self.current_sprite)]



# video tmx code
tmx_data = load_pygame('./levelOne/maps/levelOne.tmx')

# sprite group for collision detection
land_sprite_group = pygame.sprite.Group()
water_sprite_group = pygame.sprite.Group()



# cycle through all layers
for layer in tmx_data.visible_layers:
	# if layer.name in ('Floor', 'Plants and rocks', 'Pipes')

    print(layer.name)
    if hasattr(layer,'data'):
        for x, y, surf in layer.tiles():
            # for tile in layer.tiles():
            #     print(tile.data)
                # NOTE: here i need to check if the tile is an edge tile , use the ID of the edge tile to check this, just am not sure 
                # how to do that because the documentation is so shit and basic 
            pos = (x * 31, y * 31)
            temp = Tile(pos = pos, surf = surf, groups = sprite_group)
            if layer.name in ('Yellow Dirt', 'Brown Dirt'):
                land_sprite_group.add(temp)
            elif layer.name in ('Water'):
                water_sprite_group.add(temp)








my_player_group = pygame.sprite.Group()

my_player = Player(164, 164, land_sprite_group, water_sprite_group)
my_player_group.add(my_player)



running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                my_player.jump()

    display_surface.fill('black')
    sprite_group.draw(display_surface)

    my_player_group.update()
    my_player_group.draw(display_surface)
    

    pygame.display.flip()

    clock.tick(FPS)


pygame.quit()