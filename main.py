import pygame
import random
import datetime

from constants import *

pygame.init()

dis = pygame.display.set_mode((dis_width, dis_height))
pygame.display.set_caption('fvngs/snake')

clock = pygame.time.Clock()

font_style = pygame.font.Font('font.ttf', int(dis_width/30))
font_style_large = pygame.font.Font('font.ttf', int(dis_width/20))


def our_score(score):
    value = font_style.render("Score: " + str(score), True, white)
    dis.blit(value, [0, 0])
    timevalue = font_style.render(str(datetime.datetime.today().strftime("%H:%M:%S")), True, white)
    dis.blit(timevalue, [0, dis_width-(dis_width/25)])

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
    mesg = font_style_large.render(msg, True, color)
    shadow = font_style_large.render(msg, True, gray)
    text_rect = mesg.get_rect(center=(dis_width / 2, dis_height / 2))
    shadow_rect = text_rect.copy()
    shadow_rect.move_ip(2, 2)
    dis.blit(shadow, shadow_rect)
    dis.blit(mesg, text_rect)


def draw_grid():
    grid_surface = pygame.Surface((dis_width, dis_height))
    grid_surface.set_alpha(128)

    for x in range(0, dis_width, snake_block):
        pygame.draw.line(grid_surface, gray, (x, 0), (x, dis_height))
    for y in range(0, dis_height, snake_block):
        pygame.draw.line(grid_surface, gray, (0, y), (dis_width, y))
    
    return grid_surface

grid_surface = draw_grid()

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
    
    grow_counter = 0
    grow_segments = 0

    while not game_over:
        while game_close:
            dis.blit(background_texture, (0, 0))
            message("You Lost! Press Q-Quit or R-Restart", white)
            our_score(Length_of_snake - 1)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_r:
                        gameLoop()
                        return

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            elif event.type == pygame.KEYDOWN:
                if (event.key == pygame.K_LEFT or event.key == pygame.K_a) and direction != 'right':
                    x1_change = -snake_block
                    y1_change = 0
                    direction = 'left'
                elif (event.key == pygame.K_RIGHT or event.key == pygame.K_d) and direction != 'left':
                    x1_change = snake_block
                    y1_change = 0
                    direction = 'right'
                elif (event.key == pygame.K_UP or event.key == pygame.K_w) and direction != 'down':
                    y1_change = -snake_block
                    x1_change = 0
                    direction = 'up'
                elif (event.key == pygame.K_DOWN or event.key == pygame.K_s) and direction != 'up':
                    y1_change = snake_block
                    x1_change = 0
                    direction = 'down'

        if x1 >= dis_width or x1 < 0 or y1 >= dis_height or y1 < 0:
            game_close = True
        x1 += x1_change
        y1 += y1_change
        dis.blit(background_texture, (0, 0))
        dis.blit(grid_surface, (0, 0))
        pygame.draw.rect(dis, red, [foodx, foody, snake_block, snake_block])
        snake_Head = [x1, y1]
        snake_List.append(snake_Head)
        if len(snake_List) > Length_of_snake:
            del snake_List[0]

        for x in snake_List[:-1]:
            if x == snake_Head:
                game_close = True

        if animation:
            if grow_counter > 0:
                grow_counter -= 1
                if grow_counter == 0:
                    Length_of_snake += 1

        our_snake(snake_block, snake_List, direction)
        our_score(Length_of_snake - 1)

        pygame.display.update()

        if x1 == foodx and y1 == foody:
            foodx = round(random.randrange(0, dis_width - snake_block) / snake_block) * snake_block
            foody = round(random.randrange(0, dis_height - snake_block) / snake_block) * snake_block
            if animation:
                grow_counter = grow_speed
            else:
                Length_of_snake += 1

        clock.tick(snake_speed)

    pygame.quit()
    quit()

gameLoop()
