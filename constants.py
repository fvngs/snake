import os
import pygame
import json

white = (255, 255, 255)
yellow = (255, 255, 102)
black = (0, 0, 0)
red = (213, 50, 80)
green = (0, 255, 0)
blue = (50, 153, 213)
gray = (50, 50, 50)

with open('config.json', 'r') as f:
    config = json.load(f)
    dis_width = config['resolution']
    dis_height = dis_width

    grow_speed = config['grow_speed']

    snake_block = int(dis_height / 40)
    snake_speed = config['snake_speed']
    
    animation = bool()
    
    pause_hotkey = config['pause_hotkey']
    
    animation = config['grow_animation'] == "True"
    grid = config["background_grid"] == "True"
    time = config["show_time"] == "True"
    

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