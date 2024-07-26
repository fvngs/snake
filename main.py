import pygame
import random
import datetime
from pypresence import Presence
from constants import *

pygame.init()

dis = pygame.display.set_mode((dis_width, dis_height))
pygame.display.set_caption('fvngs/snake')
pygame.display.set_icon(icon)

pygame.mixer.init()
pygame.mixer.music.load('textures\\beep.mp3')

clock = pygame.time.Clock()

if do_rpc:
    client_id = "1264914630682349571"
    RPC = Presence(client_id)
    RPC.connect()

font_style = pygame.font.Font('font.ttf', int(dis_width/30))
font_style_large = pygame.font.Font('font.ttf', int(dis_width/20))

def our_score(score, x, y, color):
    if showscore:
        value = font_style.render(f"Score: {score}", True, color)
        dis.blit(value, [x, y])
    if showtime:
        timevalue = font_style.render(str(datetime.datetime.today().strftime("%H:%M:%S")), True, white)
        dis.blit(timevalue, [0, dis_width-(dis_width/25)])

def our_snake(snake_block, snake_list, direction, head_texture, body_texture):
    for i, x in enumerate(snake_list):
        if i == len(snake_list) - 1:
            dis.blit(head_texture, [x[0], x[1]])
        else:
            dis.blit(body_texture, [x[0], x[1]])

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
    grid_surface.set_alpha(grid_alpha)

    for x in range(0, dis_width, snake_block):
        pygame.draw.line(grid_surface, gray, (x, 0), (x, dis_height))
    for y in range(0, dis_height, snake_block):
        pygame.draw.line(grid_surface, gray, (0, y), (dis_width, y))
    
    return grid_surface

grid_surface = draw_grid()

def gameLoop():
    global highscore
    global mask_texture
    game_over = False
    game_close = False

    x1 = dis_width / 2
    y1 = dis_height / 2

    x1_change = 0
    y1_change = 0

    direction = 'up'
    last_direction = direction

    snake_List = []
    Length_of_snake = 1

    foodx = round(random.randrange(0, dis_width - snake_block) / snake_block) * snake_block
    foody = round(random.randrange(0, dis_height - snake_block) / snake_block) * snake_block
    
    grow_counter = 0
    grow_segments = 0

    while not game_over:
        while game_close:
            dis.blit(background_texture, (0, 0))
            message("Game Over!", white)
            final_score_msg = f"Final Score: {Length_of_snake - 1}"
            high_score_msg = f"High Score: {highscore}"
            restart_msg = "Press R to Restart, Q to Quit, or M for Main Menu"

            final_score_surface = font_style.render(final_score_msg, True, white)
            high_score_surface = font_style.render(high_score_msg, True, white)
            restart_surface = font_style.render(restart_msg, True, white)

            final_score_rect = final_score_surface.get_rect(center=(dis_width / 2, dis_height / 2 + 50))
            high_score_rect = high_score_surface.get_rect(center=(dis_width / 2, dis_height / 2 + 100))
            restart_rect = restart_surface.get_rect(center=(dis_width / 2, dis_height / 2 + 150))

            dis.blit(final_score_surface, final_score_rect)
            dis.blit(high_score_surface, high_score_rect)
            dis.blit(restart_surface, restart_rect)
            
            our_score(Length_of_snake - 1, 0, 0, white)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_r:
                        gameLoop()
                        return
                    if event.key == pygame.K_m:
                        main_menu()
                        return

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            elif event.type == pygame.KEYDOWN:
                if (event.key in key_mapping['left']) and direction != 'right' and last_direction != 'right':
                    x1_change = -snake_block
                    y1_change = 0
                    direction = 'left'
                elif (event.key in key_mapping['right']) and direction != 'left' and last_direction != 'left':
                    x1_change = snake_block
                    y1_change = 0
                    direction = 'right'
                elif (event.key in key_mapping['up']) and direction != 'down' and last_direction != 'down':
                    y1_change = -snake_block
                    x1_change = 0
                    direction = 'up'
                elif (event.key in key_mapping['down']) and direction != 'up' and last_direction != 'up':
                    y1_change = snake_block
                    x1_change = 0
                    direction = 'down'

        if x1 >= dis_width or x1 < 0 or y1 >= dis_height or y1 < 0:
            game_close = True
        x1 += x1_change
        y1 += y1_change
        dis.blit(background_texture, (0, 0))
        dis.blit(mask_texture, (0, 0))
        if grid: dis.blit(grid_surface, (0, 0))
        pygame.draw.rect(dis, food_color, [foodx, foody, snake_block, snake_block])
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

        our_snake(snake_block, snake_List, direction, headtexture, bodytexture)
        our_score(Length_of_snake - 1, 0, 0, white)
        if (Length_of_snake - 1) > highscore:
            highscore = Length_of_snake - 1

        pygame.display.update()

        if x1 == foodx and y1 == foody:
            foodx = round(random.randrange(0, dis_width - snake_block) / snake_block) * snake_block
            foody = round(random.randrange(0, dis_height - snake_block) / snake_block) * snake_block
            pygame.mixer.music.play()
            if animation:
                grow_counter = grow_speed
            else:
                Length_of_snake += 1
                
        if do_rpc: RPC.update(state=f"score: {Length_of_snake-1} | highscore: {highscore}", start=game_start, large_image="big-image", large_text="snake")

        clock.tick(snake_speed)

        last_direction = direction

    with open('highscore', 'w') as f:
        f.write(str(highscore))
    
    pygame.quit()
    quit()

def gameLoop_vs_ai():
    global highscore
    global mask_texture
    game_over = False
    game_close = False
    ai_lost = False

    x1 = dis_width / 2
    y1 = dis_height / 2
    x1_change = 0
    y1_change = 0
    direction1 = 'up'
    last_direction1 = direction1
    snake_List1 = []
    Length_of_snake1 = 1

    x2 = dis_width / 4
    y2 = dis_height / 4
    x2_change = 0
    y2_change = 0
    direction2 = 'up'
    last_direction2 = direction2
    snake_List2 = []
    Length_of_snake2 = 1

    foodx = round(random.randrange(0, dis_width - snake_block) / snake_block) * snake_block
    foody = round(random.randrange(0, dis_height - snake_block) / snake_block) * snake_block
    
    grow_counter1 = 0
    grow_counter2 = 0
    player_started = False

    while not game_over:
        while game_close:
            dis.blit(background_texture, (0, 0))
            if ai_lost:
                message("AI Lost!", white)
            else:
                message("You Lost!", white)
            final_score_msg1 = f"Final Score: {Length_of_snake1 - 1}"
            final_score_msg2 = f"AI Score: {Length_of_snake2 - 1}"
            high_score_msg = f"High Score: {highscore}"
            restart_msg = "Press R to Restart, Q to Quit, or M for Main Menu"

            final_score_surface1 = font_style.render(final_score_msg1, True, white)
            final_score_surface2 = font_style.render(final_score_msg2, True, white)
            high_score_surface = font_style.render(high_score_msg, True, white)
            restart_surface = font_style.render(restart_msg, True, white)

            final_score_rect1 = final_score_surface1.get_rect(center=(dis_width / 2, dis_height / 2 + 60))
            final_score_rect2 = final_score_surface2.get_rect(center=(dis_width / 2, dis_height / 2 + 90))
            high_score_rect = high_score_surface.get_rect(center=(dis_width / 2, dis_height / 2 + 120))
            restart_rect = restart_surface.get_rect(center=(dis_width / 2, dis_height / 2 + 180))

            dis.blit(final_score_surface1, final_score_rect1)
            dis.blit(final_score_surface2, final_score_rect2)
            dis.blit(high_score_surface, high_score_rect)
            dis.blit(restart_surface, restart_rect)
            
            our_score(Length_of_snake1 - 1, 0, 0, white)
            our_score(Length_of_snake2 - 1, 0, 30, red)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_r:
                        gameLoop_vs_ai()
                        return
                    if event.key == pygame.K_m:
                        main_menu()
                        return

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            elif event.type == pygame.KEYDOWN:
                if (event.key in key_mapping['left']) and direction1 != 'right' and last_direction1 != 'right':
                    x1_change = -snake_block
                    y1_change = 0
                    direction1 = 'left'
                    player_started = True
                elif (event.key in key_mapping['right']) and direction1 != 'left' and last_direction1 != 'left':
                    x1_change = snake_block
                    y1_change = 0
                    direction1 = 'right'
                    player_started = True
                elif (event.key in key_mapping['up']) and direction1 != 'down' and last_direction1 != 'down':
                    y1_change = -snake_block
                    x1_change = 0
                    direction1 = 'up'
                    player_started = True
                elif (event.key in key_mapping['down']) and direction1 != 'up' and last_direction1 != 'up':
                    y1_change = snake_block
                    x1_change = 0
                    direction1 = 'down'
                    player_started = True

        if player_started:
            if x2 < foodx and direction2 != 'left':
                x2_change = snake_block
                y2_change = 0
                direction2 = 'right'
            elif x2 > foodx and direction2 != 'right':
                x2_change = -snake_block
                y2_change = 0
                direction2 = 'left'
            elif y2 < foody and direction2 != 'up':
                y2_change = snake_block
                x2_change = 0
                direction2 = 'down'
            elif y2 > foody and direction2 != 'down':
                y2_change = -snake_block
                x2_change = 0
                direction2 = 'up'

        if x1 >= dis_width or x1 < 0 or y1 >= dis_height or y1 < 0:
            game_close = True
        if x2 >= dis_width or x2 < 0 or y2 >= dis_height or y2 < 0:
            game_close = True
            ai_lost = True

        x1 += x1_change
        y1 += y1_change
        x2 += x2_change
        y2 += y2_change

        dis.blit(background_texture, (0, 0))
        dis.blit(mask_texture, (0, 0))
        if grid: dis.blit(grid_surface, (0, 0))
        pygame.draw.rect(dis, food_color, [foodx, foody, snake_block, snake_block])

        snake_Head1 = [x1, y1]
        snake_List1.append(snake_Head1)
        if len(snake_List1) > Length_of_snake1:
            del snake_List1[0]

        snake_Head2 = [x2, y2]
        snake_List2.append(snake_Head2)
        if len(snake_List2) > Length_of_snake2:
            del snake_List2[0]

        for x in snake_List1[:-1]:
            if x == snake_Head1:
                game_close = True
        for x in snake_List2[:-1]:
            if x == snake_Head2:
                game_close = True
                ai_lost = True

        for x in snake_List2:
            if x == snake_Head1:
                game_close = True
        for x in snake_List1:
            if x == snake_Head2:
                game_close = True
                ai_lost = True

        if animation:
            if grow_counter1 > 0:
                grow_counter1 -= 1
                if grow_counter1 == 0:
                    Length_of_snake1 += 1
            if grow_counter2 > 0:
                grow_counter2 -= 1
                if grow_counter2 == 0:
                    Length_of_snake2 += 1

        our_snake(snake_block, snake_List1, direction1, headtexture, bodytexture)
        our_snake(snake_block, snake_List2, direction2, ai_texture, ai_texture)
        our_score(Length_of_snake1 - 1, 0, 0, white)
        our_score(Length_of_snake2 - 1, 0, 30, red)

        if (Length_of_snake1 - 1) > highscore:
            highscore = Length_of_snake1 - 1
        if (Length_of_snake2 - 1) > highscore:
            highscore = Length_of_snake2 - 1

        pygame.display.update()

        if x1 == foodx and y1 == foody:
            foodx = round(random.randrange(0, dis_width - snake_block) / snake_block) * snake_block
            foody = round(random.randrange(0, dis_height - snake_block) / snake_block) * snake_block
            pygame.mixer.music.play()
            if animation:
                grow_counter1 = grow_speed
            else:
                Length_of_snake1 += 1
        if x2 == foodx and y2 == foody:
            foodx = round(random.randrange(0, dis_width - snake_block) / snake_block) * snake_block
            foody = round(random.randrange(0, dis_height - snake_block) / snake_block) * snake_block
            pygame.mixer.music.play()
            if animation:
                grow_counter2 = grow_speed
            else:
                Length_of_snake2 += 1
                
        if do_rpc: RPC.update(state=f"score: {Length_of_snake1-1} | highscore: {highscore}", start=game_start, large_image="big-image", large_text="snake")

        clock.tick(snake_speed)

        last_direction1 = direction1
        last_direction2 = direction2

    with open('highscore', 'w') as f:
        f.write(str(highscore))
    
    pygame.quit()
    quit()


def main_menu():
    menu = True
    while menu:
        dis.blit(background_texture, (0, 0))
        title_msg = "Snake by fvngs"
        solo_msg = "Press S to Play Solo"
        ai_msg = "Press A to Play vs AI"
        
        title_surface = font_style_large.render(title_msg, True, white)
        solo_surface = font_style.render(solo_msg, True, white)
        ai_surface = font_style.render(ai_msg, True, white)
        
        title_rect = title_surface.get_rect(center=(dis_width / 2, dis_height / 4))
        solo_rect = solo_surface.get_rect(center=(dis_width / 2, dis_height / 2))
        ai_rect = ai_surface.get_rect(center=(dis_width / 2, dis_height / 2 + 50))
        
        dis.blit(title_surface, title_rect)
        dis.blit(solo_surface, solo_rect)
        dis.blit(ai_surface, ai_rect)
        
        pygame.display.update()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                menu = False
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s:
                    menu = False
                    gameLoop()
                if event.key == pygame.K_a:
                    menu = False
                    gameLoop_vs_ai()

main_menu()
