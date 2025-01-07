"""  Inspired by 'The ultimate introduction to Pygame' by 'Clear Code'.
    This was my very first python project and hence there are many comments
    that explained the code to myself. I left them in here, because I think 
    they might be helpful for other beginners as well."""

"""Useful Knowledge:
        - The parameter of a surface always position it's upper left corner 
        - With the help of rectangles, you can position a surface also by it's other corners or edges
        - You can get information about the mouse input of the user via pygame.mouse or the event loop -> see doc
"""

import pygame
from sys import exit
from random import randint, choice

class Player(pygame.sprite.Sprite): # inherits from class in the braces

    def __init__(self):
        super().__init__()
        player_walk_1 = pygame.image.load('graphics/player/player_walk_1.png').convert_alpha()
        player_walk_2 = pygame.image.load('graphics/player/player_walk_2.png').convert_alpha()
        self.player_walk = [player_walk_1, player_walk_2] # 'self.' because I am going to need that in the entire class (global variable)
        self.player_index = 0
        self.player_jump = pygame.image.load('graphics/player/jump.png').convert_alpha()
        
        self.image = self.player_walk[self.player_index]
        self.rect = self.image.get_rect(midbottom =(80,300))
        self.gravity = 0

        self.jump_sound = pygame.mixer.Sound('audio/jump.mp3')
        self.jump_sound.set_volume(0.05)

    def player_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.rect.bottom >= 300:
            self.gravity = -20
            self.jump_sound.play()

    def apply_gravity(self):
        self.gravity += 1
        self.rect.y += self.gravity
        if self.rect.bottom >= 300:
            self.rect.bottom = 300

    def animation_state(self):
        if self.rect.bottom < 300:
            self.image = self.player_jump
        else:
            self.player_index = (self.player_index + 0.1) % len(self.player_walk)
            self.image = self.player_walk[int(self.player_index)]
    
    def update(self):
        self.player_input()
        self.apply_gravity()
        self.animation_state()

class Obstacle(pygame.sprite.Sprite):
    def __init__(self, type):
        super().__init__()

        if type == 'fly':
            fly_1 = pygame.image.load('graphics/fly/Fly1.png').convert_alpha()
            fly_2 = pygame.image.load('graphics/fly/Fly2.png').convert_alpha()
            self.frames = [fly_1, fly_2]
            y_pos = 210
        else:
            snail_1 = pygame.image.load('graphics/snail/snail1.png').convert_alpha()
            snail_2 = pygame.image.load('graphics/snail/snail2.png').convert_alpha()
            self.frames = [snail_1, snail_2]
            y_pos = 300

        self.animation_index = 0
        self.image = self.frames[self.animation_index]
        self.rect = self.image.get_rect(midbottom = (randint(900,1100), y_pos))

    def animation_state(self):
        self.animation_index = (self.animation_index + 0.1) % len(self.frames)
        self.image = self.frames[int(self.animation_index)]

    def update(self):
        self.animation_state()
        self.rect.x -= 10
        self.destroy()

    def destroy(self):
        if self.rect.x <= - 100:
            self.kill() # destroys the sprite


def display_score():
    current_time = (pygame.time.get_ticks() - start_time) // 1000
    score_surf = test_font.render(f'{current_time}', False, (64,64,64)) # f string!
    score_rect = score_surf.get_rect(center = (400, 50))
    screen.blit(score_surf, score_rect)
    return current_time

def obstacle_movement(obstacle_list):
    if obstacle_list:
        for obstacle_rect in obstacle_list:
            obstacle_rect.x -= 5 # move obstacle to left

            if obstacle_rect.bottom == 300: screen.blit(snail_surf, obstacle_rect)
            else: screen.blit(fly_surf, obstacle_rect)
        
        obstacle_list = [obstacle for obstacle in obstacle_list if obstacle.x > -100] # delete rectangles if they leave the screen

        return obstacle_list
    else: return []

def collisons(player, obstacles):
    if obstacles:
        for obstacle_rect in obstacles:
            if player.colliderect(obstacle_rect): return False
    return True

def collision_sprite():
    if pygame.sprite.spritecollide(player.sprite, obstacle_group, False): # returns a list of collided objects
        obstacle_group.empty()
        return False
    return True

def player_animation():
    """play walking animation if player is on floor
        display jumping animation if player not on floor"""
    global player_surf, player_index
    if player_rect.bottom < 300:
        player_surf = player_jump
    else:
        player_index = (player_index + 0.1) % len(player_walk)
        player_surf = player_walk[int(player_index)]
    

pygame.init()
# create display surface
display_width = 800
display_height = 400
screen = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption('Runner game')
clock = pygame.time.Clock()
test_font = pygame.font.Font('font/Pixeltype.ttf', 50) # also some standard fonts available via .font.SysFont('arial', size)
game_active = False
start_time = 0
score = 0
background_music = pygame.mixer.Sound('audio/music.wav')
background_music.set_volume(0.1)
background_music.play(loops = -1) # means til infinity

# Groups
player = pygame.sprite.GroupSingle() # if only one object is in the group
player.add(Player())

obstacle_group = pygame.sprite.Group() # if multiple objects are in the group


sky_surface = pygame.image.load('graphics/Sky.png').convert() # the program code has to be in the same (or top) folder as the referenced files!
ground_surface = pygame.image.load('graphics/ground.png').convert() # 'convert()' converts the png-image into a format that pygame can work faster and more easily with


# Snail
snail_frame1 = pygame.image.load('graphics/snail/snail1.png').convert_alpha() # the alpha removes the white background of the snail
snail_frame2 = pygame.image.load('graphics/snail/snail2.png').convert_alpha() # the alpha removes the white background of the snail
snail_frames= [snail_frame1, snail_frame2]
snail_frame_index = 0
snail_surf = snail_frames[snail_frame_index]

# Fly
fly_frame1 = pygame.image.load('graphics/fly/Fly1.png').convert_alpha()
fly_frame2 = pygame.image.load('graphics/fly/Fly2.png').convert_alpha()
fly_frames = [fly_frame1, fly_frame2]
fly_frame_index = 0
fly_surf = fly_frames[fly_frame_index]

obstacle_rect_list = []

player_walk_1 = pygame.image.load('graphics/player/player_walk_1.png').convert_alpha()
player_walk_2 = pygame.image.load('graphics/player/player_walk_2.png').convert_alpha()
player_walk = [player_walk_1, player_walk_2]
player_index = 0
player_jump = pygame.image.load('graphics/player/jump.png').convert_alpha()

player_surf = player_walk[player_index]
player_rect = player_surf.get_rect(midbottom = (80, 300))
player_gravity = 0

#Intro screen
player_stand = pygame.image.load('graphics/player/player_stand.png').convert_alpha()
player_stand = pygame.transform.rotozoom(player_stand, 0, 2) # scale player_surface to a larger size, cool function!
player_stand_rect = player_stand.get_rect(center = (display_width/2, display_height/2))

game_name = test_font.render('Pixel Runner', False, (111,196,169))
game_name_rect = game_name.get_rect(center=(display_width/2, 80))

game_message = test_font.render('Press Space to start', False, (111,196,169))
game_message_rect = game_message.get_rect(center = (display_width/2, 330))

#Timer
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer, 1500)

snail_animation_timer = pygame.USEREVENT + 2
pygame.time.set_timer(snail_animation_timer,500)

fly_animation_timer = pygame.USEREVENT + 3
pygame.time.set_timer(fly_animation_timer,200)



while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: # red x in window was clicked
            pygame.quit()
            exit() # vgl exit in C
        if game_active:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if player_rect.collidepoint(event.pos):
                    player_gravity = -20
            
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and player_rect.bottom == 300:
                    player_gravity = -20
        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                game_active = True
                start_time = pygame.time.get_ticks()

        if game_active:
            if event.type == obstacle_timer: # spawn new enimies randomly
                obstacle_group.add(Obstacle(choice(['fly', 'snail', 'snail', 'snail'])))
                
            elif event.type == snail_animation_timer:
                snail_frame_index = (snail_frame_index + 1) % len(snail_frames)
                snail_surf = snail_frames[snail_frame_index]
            
            elif event.type == fly_animation_timer:
                fly_frame_index = (fly_frame_index + 1) % len(fly_frames)
                fly_surf = fly_frames[fly_frame_index]
    
    if game_active:
        screen.blit(sky_surface, (0, 0)) # 'block image transfer': draw one image onto another at position (x,y)
        screen.blit(ground_surface, (0, 300))
        
        #Score
        score = display_score()
    
        # move snail to the left until it's out of screen
        # snail_rect.x -= 6
        # if snail_rect.right < 0: snail_rect.left = display_width 
        # screen.blit(snail_surf, snail_rect)

        # Player
        # player_gravity += 1
        # player_rect.y += player_gravity
        # if player_rect.bottom >= 300: player_rect.bottom = 300
        # player_animation()
        # screen.blit(player_surf, player_rect)
        player.draw(screen) # on screen
        player.update()

        obstacle_group.draw(screen)
        obstacle_group.update()

        # Obstacle movement
        #obstacle_rect_list = obstacle_movement(obstacle_rect_list)

        # collision
        #game_active = collisons(player_rect, obstacle_rect_list)
        game_active = collision_sprite()

    else:
        screen.fill((94, 129, 162))
        screen.blit(player_stand, player_stand_rect)
        
        #reset game variables
        obstacle_rect_list.clear()
        player_rect.midbottom = (80, 300)
        player_gravity = 0
        
        score_message = test_font.render(f'Your score: {score}', False, (111,196,169))
        score_message_rect = score_message.get_rect(center = (display_width/2, 330))
        screen.blit(game_name, game_name_rect)
        
        if score == 0: screen.blit(game_message, game_message_rect)
        else: screen.blit(score_message, score_message_rect)
    
    pygame.display.update()
    clock.tick(60) # sets the maximum fps border = maximum speed, even if pc could go faster




"""Bonus section including useful functions that've been taught in the video:"""

#test_surface = pygame.Surface((100, 200)) # create a surface
#test_surface.fill('Red') # fills surface with a specific color

#if event.type == pygame.MOUSEMOTION:
        #    print(event.pos)    # prints the pos of the mouse
        # prints if any button of the mouse is pressed or released
        # if event.type == pygame.MOUSEBUTTONDOWN:
        #     print('mouse down')
        # if event.type == pygame.MOUSEBUTTONUP:
        #     print('mouse up')

# pygame.draw.ellipse(screen, 'Brown', pygame.Rect(50, 200, 100, 100), 10)

# pygame.draw.line(screen, 'Gold', (0, 0), pygame.mouse.get_pos(), 10)

# keys = pygame.key.get_pressed()
# if keys[pygame.K_SPACE]:
#     print('jump')

# check collisions
    # if player_rect.colliderect(snail_rect): # collide rect
    #     print('collision')
    
    # mouse_pos = pygame.mouse.get_pos()
    # if player_rect.collidepoint(mouse_pos):
    #     print(pygame.mouse.get_pressed()) # prints which buttons of the mouse are being pressed

# pygame.draw.rect(screen, '#c0e8ec', score_rect) 
        # pygame.draw.rect(screen, '#c0e8ec', score_rect, 10)
        # screen.blit(score_surf, score_rect) 

# smartest way to create a color is to use photoshop or similar (choose color and program shows you the rgb values)
#score_surf = score_font.render('Score: ', False, (64, 64, 64)) # antialias adds shadow etc
#score_rect = score_surf.get_rect(center = (display_width/2, 50))
# snail_rect = snail_surf.get_rect(bottomright = (600, 300)) # use position of ground (see below) to position the object exactly on the ground
# if randint(0,2):
                #     obstacle_rect_list.append(snail_surf.get_rect(bottomright = (display_width + randint(100, 300),300)))
                # else:
                #     obstacle_rect_list.append(fly_surf.get_rect(bottomright = (display_width + randint(100, 300),210)))

