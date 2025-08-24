import pygame
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
pygame.display.set_caption('Snake Game Enhanced')

clock = pygame.time.Clock()
snake_block = 10
snake_speed = 15

# Fonts
font_style = pygame.font.SysFont("bahnschrift", 20)
score_font = pygame.font.SysFont("comicsansms", 18)
title_font = pygame.font.SysFont("comicsansms", 28, bold=True)

# --- High Score Management ---
def load_high_score():
    if os.path.exists("highscore.txt"):
        with open("highscore.txt", "r") as f:
            try:
                return int(f.read())
            except:
                return 0
    return 0

def save_high_score(score):
    with open("highscore.txt", "w") as f:
        f.write(str(score))

high_score = load_high_score()


def Your_score(score, high_score):
    value = score_font.render(f"Score: {score}  High Score: {high_score}", True, yellow)
    dis.blit(value, [5, 5])  # neatly in top-left


def our_snake(snake_block, snake_list):
    for i, x in enumerate(snake_list):
        if i == len(snake_list) - 1:
            pygame.draw.rect(dis, red, [x[0], x[1], snake_block, snake_block])  # Head
        else:
            pygame.draw.rect(dis, black, [x[0], x[1], snake_block, snake_block])


def message(msg, color, y_offset=0, center=True, big=False):
    font_used = title_font if big else font_style
    mesg = font_used.render(msg, True, color)
    if center:
        dis.blit(mesg, [dis_width / 2 - mesg.get_width() / 2, dis_height / 3 + y_offset])
    else:
        dis.blit(mesg, [dis_width / 8, dis_height / 3 + y_offset])


def spawn_food(snake_List):
    while True:
        foodx = round(random.randrange(0, dis_width - snake_block) / 10.0) * 10.0
        foody = round(random.randrange(0, dis_height - snake_block) / 10.0) * 10.0
        if [foodx, foody] not in snake_List:
            return foodx, foody


def start_screen():
    global high_score
    start = True
    while start:
        dis.fill(blue)
        message("🐍 Snake Game 🐍", yellow, -40, center=True, big=True)
        message(f"High Score: {high_score}", white, 10, center=True)
        message("Press C to Play or Q to Quit", red, 50, center=True)
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c:
                    start = False
                if event.key == pygame.K_q:
                    pygame.quit()
                    quit()


def gameLoop():
    global high_score

    game_over = False
    game_close = False
    paused = False

    # Snake starting position
    x1 = dis_width / 2
    y1 = dis_height / 2

    x1_change = 0
    y1_change = 0

    snake_List = []
    Length_of_snake = 1

    foodx, foody = spawn_food(snake_List)

    snake_speed_local = snake_speed

    while not game_over:

        while game_close:
            dis.fill(blue)
            message("You Lost!", red, -30, center=True, big=True)
            message("Press C-Play Again or Q-Quit", white, 20, center=True)
            Your_score(Length_of_snake - 1, high_score)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_c:
                        gameLoop()
                        return  # Exit the current function call

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
                elif event.key == pygame.K_p:  # Pause toggle
                    paused = not paused
                elif event.key == pygame.K_r:  # Restart anytime
                    gameLoop()
                    return

        if paused:
            dis.fill(blue)
            message("Paused - Press P to Resume", yellow, 0, center=True)
            Your_score(Length_of_snake - 1, high_score)
            pygame.display.update()
            continue

        if x1 >= dis_width or x1 < 0 or y1 >= dis_height or y1 < 0:
            game_close = True

        x1 += x1_change
        y1 += y1_change
        dis.fill(blue)
        pygame.draw.rect(dis, green, [foodx, foody, snake_block, snake_block])
        snake_Head = [x1, y1]
        snake_List.append(snake_Head)
        if len(snake_List) > Length_of_snake:
            del snake_List[0]

        for x in snake_List[:-1]:
            if x == snake_Head:
                game_close = True

        our_snake(snake_block, snake_List)

        # Update high score
        score_now = Length_of_snake - 1
        if score_now > high_score:
            high_score = score_now
            save_high_score(high_score)

        Your_score(score_now, high_score)
        pygame.display.update()

        if x1 == foodx and y1 == foody:
            foodx, foody = spawn_food(snake_List)
            Length_of_snake += 1
            snake_speed_local += 1  # speed increase

        clock.tick(snake_speed_local)

    pygame.quit()
    quit()


# Start screen before game
start_screen()
gameLoop()
