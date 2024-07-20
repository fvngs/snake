import os
import pygame

white = (255, 255, 255)
yellow = (255, 255, 102)
black = (0, 0, 0)
red = (213, 50, 80)
green = (0, 255, 0)
blue = (50, 153, 213)
gray = (50, 50, 50)

dis_width = 1000
dis_height = 1000

grow_counter = 0
grow_segments = 0
grow_speed = 5

snake_block = int(dis_height / 40)
snake_speed = 15

if os.path.isfile('textures/snake_head.png'):
    headtexture = pygame.image.load('textures/snake_head.png')
    headtexture = pygame.transform.scale(headtexture, (snake_block, snake_block))
else:
    headtexture = pygame.Surface((snake_block, snake_block))
    headtexture.fill(green)

if os.path.isfile('textures/snake_body.png'):
    bodytexture = pygame.image.load('textures/snake_body.png')
    bodytexture = pygame.transform.scale(bodytexture, (snake_block, snake_block))
else:
    bodytexture = pygame.Surface((snake_block, snake_block))
    bodytexture.fill(green)


#TODO: create a constant that lowers the brightness of the background image + cropping from center instead of stretching
if os.path.isfile('textures/background.png'):
    background_texture = pygame.image.load('textures/background.png')
    background_texture = pygame.transform.scale(background_texture, (dis_width, dis_height))
else:
    background_texture = pygame.Surface((dis_width, dis_height))
    background_texture.fill(black)