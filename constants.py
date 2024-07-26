import os
import pygame
import json
import time

white = (255, 255, 255)
yellow = (255, 255, 102)
black = (0, 0, 0)
red = (213, 50, 80)
green = (0, 255, 0)
blue = (50, 153, 213)
gray = (50, 50, 50)

def mapkey(key_str):
    return getattr(pygame, f'K_{key_str}')





highscorecheck = True
color = 'white'

icon = pygame.image.load('textures\icon.png')

game_start = time.time()

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
    showtime = config["show_time"] == "True"
    showscore = config["show_score"] == "True"
    showhighscore = config["save_highscore"] == "True"
    do_rpc = config["discord-rpc"] == "True"
    
    bg_alpha = config['background_transparency']
    grid_alpha = config['grid_transparency']
    
    snake_color = config['snake_color']
    food_color = config['food_color']
    ai_color = config['ai_color']
    
    
    key_mapping = {
    'left': [mapkey(key) for key in config['keys']['left']],
    'right': [mapkey(key) for key in config['keys']['right']],
    'up': [mapkey(key) for key in config['keys']['up']],
    'down': [mapkey(key) for key in config['keys']['down']]
}

try:
    with open('highscore', 'r') as f:
        highscore = int(f.readline())
except FileNotFoundError:
    with open('highscore', 'w+') as f:
        f.write('0')
except ValueError:
    with open('highscore', 'w+') as f:
        f.write('0')
    

if os.path.isfile('textures/snake_head.png'):
    headtexture = pygame.image.load('textures/snake_head.png')
    headtexture = pygame.transform.scale(headtexture, (snake_block, snake_block))
else:
    headtexture = pygame.Surface((snake_block, snake_block))
    headtexture.fill(snake_color)

if os.path.isfile('textures/snake_body.png'):
    bodytexture = pygame.image.load('textures/snake_body.png')
    bodytexture = pygame.transform.scale(bodytexture, (snake_block, snake_block))
else:
    bodytexture = pygame.Surface((snake_block, snake_block))
    bodytexture.fill(snake_color)
    
ai_texture = pygame.Surface((snake_block, snake_block))
ai_texture.fill(ai_color)


if os.path.isfile('textures/background.png'):
    background_texture = pygame.image.load('textures/background.png')
    background_texture = pygame.transform.scale(background_texture, (dis_width, dis_height))
    mask_texture = pygame.Surface((dis_width, dis_height))
    mask_texture.fill(black)
    mask_texture.set_alpha(bg_alpha)
else:
    background_texture = pygame.Surface((dis_width, dis_height))
    background_texture.fill(black)
    mask_texture = pygame.Surface((dis_width, dis_height))
    mask_texture.fill(black)