import pygame
import time
import random

from constants import *

pygame.init()

dis = pygame.display.set_mode((dis_width, dis_height))
pygame.display.set_caption('fvngs/snake')

clock = pygame.time.Clock()

font_style = pygame.font.Font('font.ttf', 35)

def our_score(score):
    value = font_style.render("Score: " + str(score), True, white)
    dis.blit(value, [0, 0])

def our_snake(snake_block, snake_list, direction):
    if direction == 'up':
        head_texture = headtexture
    elif direction == 'right':
        head_texture = pygame.transform.rotate(headtexture, -90)
    elif direction == 'down':
        head_texture = pygame.transform.rotate(headtexture, 180)
    elif direction == 'left':
        head_texture = pygame.transform.rotate(headtexture, 90)

    for i, x in enumerate(snake_list):
        if i == len(snake_list) - 1:
            dis.blit(head_texture, [x[0], x[1]])
        else:
            dis.blit(bodytexture, [x[0], x[1]])

def message(msg, color):
    mesg = font_style.render(msg, True, color)
    dis.blit(mesg, [dis_width / 5, dis_height / 2])

def gameLoop():
    game_over = False
    game_close = False

    x1 = dis_width / 2
    y1 = dis_height / 2

    x1_change = 0
    y1_change = 0

    direction = 'up'

    snake_List = []
    Length_of_snake = 1

    foodx = round(random.randrange(0, dis_width - snake_block) / snake_block) * snake_block
    foody = round(random.randrange(0, dis_height - snake_block) / snake_block) * snake_block

    while not game_over:

        while game_close == True:
            dis.blit(background_texture, (0, 0))
            message("You Lost! Press Q-Quit or R-Restart", red)
            our_score(Length_of_snake - 1)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_r:
                        gameLoop()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key in [pygame.K_LEFT, pygame.K_a] and x1_change != snake_block:
                    x1_change = -snake_block
                    y1_change = 0
                    direction = 'left'
                elif event.key in [pygame.K_RIGHT, pygame.K_d] and x1_change != -snake_block:
                    x1_change = snake_block
                    y1_change = 0
                    direction = 'right'
                elif event.key in [pygame.K_UP, pygame.K_w] and y1_change != snake_block:
                    y1_change = -snake_block
                    x1_change = 0
                    direction = 'up'
                elif event.key in [pygame.K_DOWN, pygame.K_s] and y1_change != -snake_block:
                    y1_change = snake_block
                    x1_change = 0
                    direction = 'down'

        if x1 >= dis_width or x1 < 0 or y1 >= dis_height or y1 < 0:
            game_close = True
        x1 += x1_change
        y1 += y1_change
        dis.blit(background_texture, (0, 0))
        pygame.draw.rect(dis, red, [foodx, foody, snake_block, snake_block])
        snake_Head = []
        snake_Head.append(x1)
        snake_Head.append(y1)
        snake_List.append(snake_Head)
        if len(snake_List) > Length_of_snake:
            del snake_List[0]

        for x in snake_List[:-1]:
            if x == snake_Head:
                game_close = True

        our_snake(snake_block, snake_List, direction)
        our_score(Length_of_snake - 1)

        pygame.display.update()

        if x1 == foodx and y1 == foody:
            foodx = round(random.randrange(0, dis_width - snake_block) / snake_block) * snake_block
            foody = round(random.randrange(0, dis_height - snake_block) / snake_block) * snake_block
            Length_of_snake += 1

        clock.tick(snake_speed)

    pygame.quit()
    quit()

gameLoop()
