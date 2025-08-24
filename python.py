import pygame
import time
import random
import os

# Initialize Pygame
pygame.init()

# Define colors
white = (255, 255, 255)
yellow = (255, 255, 102)
black = (0, 0, 0)
red = (213, 50, 80)
green = (0, 255, 0)
blue = (50, 153, 213)

# Display dimensions
dis_width = 400
dis_height = 300

# Initialize display
dis = pygame.display.set_mode((dis_width, dis_height))
pygame.display.set_caption('Snake Game by GitHub Copilot')

clock = pygame.time.Clock()
snake_block = 10
snake_speed = 15  # default, set on splash
snake_color = black  # will update on difficulty

# Fonts
font_style = pygame.font.SysFont("bahnschrift", 20)
score_font = pygame.font.SysFont("comicsansms", 20)

# Load sounds
chomp_sound = pygame.mixer.Sound("chomp.wav")
highscore_sound = pygame.mixer.Sound("highscore.wav")
gameover_sound = pygame.mixer.Sound("gameover.wav")

# High score file
highscore_file = "highscore.txt"
if os.path.exists(highscore_file):
    with open(highscore_file, "r") as f:
        high_score = int(f.read().strip())
else:
    high_score = 0

def Your_score(score, high_score):
    score_text = score_font.render("Score: " + str(score), True, yellow)
    high_text = score_font.render("High: " + str(high_score), True, yellow)
    dis.blit(score_text, [5, 5])
    dis.blit(high_text, [dis_width - 100, 5])

def our_snake(snake_block, snake_list, color):
    for x in snake_list:
        pygame.draw.rect(dis, color, [x[0], x[1], snake_block, snake_block])

def message(msg, color, y_offset=0):
    mesg = font_style.render(msg, True, color)
    dis.blit(mesg, [dis_width / 6, (dis_height / 3) + y_offset])

def splash_screen():
    dis.fill(blue)
    title = pygame.font.SysFont("comicsansms", 30).render("Snake Game", True, yellow)
    tip1 = font_style.render("Press 1 for Easy", True, white)
    tip2 = font_style.render("Press 2 for Medium", True, white)
    tip3 = font_style.render("Press 3 for Hard", True, white)
    tip4 = font_style.render("Press Q to Quit", True, red)

    dis.blit(title, [dis_width / 3.5, dis_height / 6])
    dis.blit(tip1, [dis_width / 3.2, dis_height / 3])
    dis.blit(tip2, [dis_width / 3.2, dis_height / 3 + 30])
    dis.blit(tip3, [dis_width / 3.2, dis_height / 3 + 60])
    dis.blit(tip4, [dis_width / 3.2, dis_height / 3 + 100])

    pygame.display.update()

    global snake_speed, snake_color
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:  # Easy
                    snake_speed = 10
                    snake_color = green
                    waiting = False
                elif event.key == pygame.K_2:  # Medium
                    snake_speed = 15
                    snake_color = yellow
                    waiting = False
                elif event.key == pygame.K_3:  # Hard
                    snake_speed = 25
                    snake_color = red
                    waiting = False
                elif event.key == pygame.K_q:
                    pygame.quit()
                    quit()

def pause_game():
    paused = True
    while paused:
        dis.fill(blue)
        message("Game Paused", yellow, -20)
        message("Press P to Resume or Q to Quit", white, 20)
        pygame.display.update()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    paused = False
                elif event.key == pygame.K_q:
                    pygame.quit()
                    quit()

def gameLoop():
    global high_score
    game_over = False
    game_close = False

    x1 = dis_width / 2
    y1 = dis_height / 2
    x1_change = 0
    y1_change = 0

    snake_List = []
    Length_of_snake = 1

    foodx = round(random.randrange(0, dis_width - snake_block) / 10.0) * 10.0
    foody = round(random.randrange(0, dis_height - snake_block) / 10.0) * 10.0

    while not game_over:
        while game_close:
            dis.fill(blue)
            message("You Lost!", red, -20)
            message("Press C-Play Again or Q-Quit", white, 20)
            Your_score(Length_of_snake - 1, high_score)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_c:
                        splash_screen()
                        gameLoop()
                        return

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and x1_change == 0:
                    x1_change = -snake_block
                    y1_change = 0
                elif event.key == pygame.K_RIGHT and x1_change == 0:
                    x1_change = snake_block
                    y1_change = 0
                elif event.key == pygame.K_UP and y1_change == 0:
                    y1_change = -snake_block
                    x1_change = 0
                elif event.key == pygame.K_DOWN and y1_change == 0:
                    y1_change = snake_block
                    x1_change = 0
                elif event.key == pygame.K_p:
                    pause_game()

        if x1 >= dis_width or x1 < 0 or y1 >= dis_height or y1 < 0:
            pygame.mixer.Sound.play(gameover_sound)
            game_close = True

        x1 += x1_change
        y1 += y1_change
        dis.fill(blue)
        pygame.draw.rect(dis, green, [foodx, foody, snake_block, snake_block])  # food is green
        snake_Head = [x1, y1]
        snake_List.append(snake_Head)
        if len(snake_List) > Length_of_snake:
            del snake_List[0]

        for x in snake_List[:-1]:
            if x == snake_Head:
                pygame.mixer.Sound.play(gameover_sound)
                game_close = True

        our_snake(snake_block, snake_List, snake_color)
        Your_score(Length_of_snake - 1, high_score)
        pygame.display.update()

        if x1 == foodx and y1 == foody:
            pygame.mixer.Sound.play(chomp_sound)
            foodx = round(random.randrange(0, dis_width - snake_block) / 10.0) * 10.0
            foody = round(random.randrange(0, dis_height - snake_block) / 10.0) * 10.0
            Length_of_snake += 1

            if (Length_of_snake - 1) > high_score:
                high_score = Length_of_snake - 1
                with open(highscore_file, "w") as f:
                    f.write(str(high_score))
                pygame.mixer.Sound.play(highscore_sound)

        clock.tick(snake_speed)

    pygame.quit()
    quit()

# Run splash screen first
splash_screen()
gameLoop()
