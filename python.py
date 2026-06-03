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

# --- Game Config (just change these to resize!) ---
snake_block = 20        # Size of snake segments
snake_speed = 15        # Base snake speed
grid_width = 40         # Number of blocks horizontally (windowed mode)
grid_height = 30        # Number of blocks vertically (windowed mode)

# Auto-calculate display size
dis_width = grid_width * snake_block
dis_height = grid_height * snake_block

# Initialize display
dis = pygame.display.set_mode((dis_width, dis_height))
pygame.display.set_caption('Snake Game Enhanced')

clock = pygame.time.Clock()

# Fonts
font_style = pygame.font.SysFont("bahnschrift", 20)
score_font = pygame.font.SysFont("comicsansms", 16)  # made smaller
title_font = pygame.font.SysFont("comicsansms", 32, bold=True)

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

def snap_to_grid(v):
    """Snap a coordinate to the nearest snake_block multiple."""
    return int(round(v / snake_block)) * snake_block

def clamp_to_playfield(v, max_dim):
    """Clamp a snapped coordinate so the block stays fully on-screen."""
    return max(0, min(v, max_dim - snake_block))

def spawn_food(snake_List):
    """Spawn strictly on-grid within current screen."""
    cols = dis_width // snake_block
    rows = dis_height // snake_block
    while True:
        foodx = random.randrange(cols) * snake_block
        foody = random.randrange(rows) * snake_block
        if [foodx, foody] not in snake_List:
            return foodx, foody

def toggle_fullscreen(fullscreen):
    """Switch modes; keep dis_width/height updated."""
    global dis, dis_width, dis_height
    if fullscreen:
        dis = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        dis_width, dis_height = dis.get_size()
    else:
        dis_width = grid_width * snake_block
        dis_height = grid_height * snake_block
        dis = pygame.display.set_mode((dis_width, dis_height))

def start_screen():
    global high_score
    start = True
    fullscreen = False
    while start:
        dis.fill(blue)
        message("🐍 Snake Game 🐍", yellow, -40, center=True, big=True)
        message(f"High Score: {high_score}", white, 10, center=True)
        message("Press C to Play, Q to Quit, F for Fullscreen", red, 50, center=True)
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c:
                    start = False
                elif event.key == pygame.K_q:
                    pygame.quit(); quit()
                elif event.key == pygame.K_f:
                    fullscreen = not fullscreen
                    toggle_fullscreen(fullscreen)

def gameLoop():
    global high_score

    game_over = False
    game_close = False
    paused = False
    fullscreen = False

    # Start centered on the grid (not just half the pixels)
    cols = dis_width // snake_block
    rows = dis_height // snake_block
    x1 = (cols // 2) * snake_block
    y1 = (rows // 2) * snake_block

    x1_change = 0
    y1_change = 0

    snake_List = []
    Length_of_snake = 1

    foodx, foody = spawn_food(snake_List)

    snake_speed_local = snake_speed
    new_high = False  # Track if new high score achieved

    while not game_over:

        while game_close:
            dis.fill(blue)
            message("You Lost!", red, -50, center=True, big=True)

            if new_high:
                message("🎉 New High Score! 🎉", yellow, -10, center=True, big=True)
            else:
                message("Better luck next time!", white, -10, center=True)

            message("Press C-Play Again, Q-Quit, F-Fullscreen", red, 40, center=True)
            Your_score(Length_of_snake - 1, high_score)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    elif event.key == pygame.K_c:
                        gameLoop(); return  # Exit the current function call
                    elif event.key == pygame.K_f:
                        fullscreen = not fullscreen
                        toggle_fullscreen(fullscreen)
                        # Recompute grid and snap everything to grid & bounds
                        cols = dis_width // snake_block
                        rows = dis_height // snake_block
                        x1 = clamp_to_playfield(snap_to_grid(x1), dis_width)
                        y1 = clamp_to_playfield(snap_to_grid(y1), dis_height)
                        snake_List = [[clamp_to_playfield(snap_to_grid(px), dis_width),
                                       clamp_to_playfield(snap_to_grid(py), dis_height)]
                                      for px, py in snake_List]
                        # Keep food within new bounds (still on grid already)
                        foodx = clamp_to_playfield(foodx, dis_width)
                        foody = clamp_to_playfield(foody, dis_height)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and x1_change == 0:
                    x1_change = -snake_block; y1_change = 0
                elif event.key == pygame.K_RIGHT and x1_change == 0:
                    x1_change = snake_block; y1_change = 0
                elif event.key == pygame.K_UP and y1_change == 0:
                    y1_change = -snake_block; x1_change = 0
                elif event.key == pygame.K_DOWN and y1_change == 0:
                    y1_change = snake_block; x1_change = 0
                elif event.key == pygame.K_p:  # Pause toggle
                    paused = not paused
                elif event.key == pygame.K_r:  # Restart anytime
                    gameLoop(); return
                elif event.key == pygame.K_f:  # Toggle fullscreen
                    fullscreen = not fullscreen
                    toggle_fullscreen(fullscreen)
                    # Recompute grid and snap everything to grid & bounds
                    cols = dis_width // snake_block
                    rows = dis_height // snake_block
                    x1 = clamp_to_playfield(snap_to_grid(x1), dis_width)
                    y1 = clamp_to_playfield(snap_to_grid(y1), dis_height)
                    snake_List = [[clamp_to_playfield(snap_to_grid(px), dis_width),
                                   clamp_to_playfield(snap_to_grid(py), dis_height)]
                                  for px, py in snake_List]
                    foodx = clamp_to_playfield(foodx, dis_width)
                    foody = clamp_to_playfield(foody, dis_height)

        if paused:
            dis.fill(blue)
            message("Paused - Press P to Resume", yellow, 0, center=True)
            Your_score(Length_of_snake - 1, high_score)
            pygame.display.update()
            continue

        # Use bounds that keep the whole block on screen
        if (x1 < 0 or x1 > dis_width - snake_block or
            y1 < 0 or y1 > dis_height - snake_block):
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
            new_high = True  # flag for celebration

        Your_score(score_now, high_score)
        pygame.display.update()

        # Eat food (now both are guaranteed on-grid ints)
        if x1 == foodx and y1 == foody:
            foodx, foody = spawn_food(snake_List)
            Length_of_snake += 1
            # Optional: snake_speed_local += 1

        clock.tick(snake_speed_local)

    pygame.quit()
    quit()

# Start screen before game
start_screen()
gameLoop()
