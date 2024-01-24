"""  From 'The ultimate introduction to Pygame' (Clear Code)  """

""" Continue at 01:07:00 """

"""Knowledge:
        - The parameter of a surface always position it's upper left corner 
        - With the help of rectangles, you can position a surface also by it's other corners or edges

"""

import pygame
from sys import exit

pygame.init()
# create display surface
display_width = 800
display_height = 400
screen = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption('Runner game')
clock = pygame.time.Clock()
test_font = pygame.font.Font('font/Pixeltype.ttf', 50) # also some standard fonts available via .font.SysFont('arial', size)

sky_surface = pygame.image.load('graphics/Sky.png').convert() # the program code has to be in the same top folder where the referenced files are!
ground_surface = pygame.image.load('graphics/ground.png').convert() # the convert converts the png-image into a format that pygame can work faster and more easily with
text_surface = test_font.render('My game', False, 'Black') # antialias adds shadow etc

snail_surf = pygame.image.load('graphics/snail/snail1.png').convert_alpha() # the alpha removes the white background of the snail
snail_rect = snail_surf.get_rect(bottomright = (600, 300)) # use position of ground (see below) to position the object exactly on the ground

player_surf = pygame.image.load('graphics/player/player_walk_1.png').convert_alpha()
player_rect = player_surf.get_rect(midbottom = (80, 300)) 

#test_surface = pygame.Surface((100, 200)) # create a surface
#test_surface.fill('Red') # fills surface with a specific color

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: # red x in window was clicked
            pygame.quit()
            exit() # vgl exit in C

    screen.blit(sky_surface, (0, 0)) # 'block image transfer': put one surface on another surface at position (x,y)
    screen.blit(ground_surface, (0, 300))
    screen.blit(text_surface, (300, 50)) 
    screen.blit(snail_surf, snail_rect)
    
    # move snail to the left until it's out of screen
    snail_rect.x -= 4
    if snail_rect.right < 0: snail_rect.left = display_width 
    screen.blit(player_surf, player_rect)
    
    # check collisions
    if player_rect.colliderect(snail_rect): # collide rect
        print("collision")
    
    pygame.display.update()
    clock.tick(60) # sets the maximum fps border = maximum speed, even if pc could go faster
