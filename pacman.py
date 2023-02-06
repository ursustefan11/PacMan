# PacMan with PyGame
from board import boards
import pygame
import math


pygame.init()


# Game Settings
WIDTH = 900
HEIGHT = 950
fps = 60
level = boards
color = 'blue'

# Player Settings
player_images = []
for i in range(1, 5):
    player_images.append(pygame.transform.scale(
        pygame.image.load(f'assets/player_images/{i}.png'), (45, 45)))

player_x = 440
player_y = 663
player_speed = 2


# Set the variables
screen = pygame.display.set_mode([WIDTH, HEIGHT])
timer = pygame.time.Clock()
font = pygame.font.Font('assets/OpenSansRegular.ttf', 20)
PI = math.pi
turns_allowed = [False, False, False, False]  # R, L, U, D
direction_command = 0
direction = 0
counter = 0
flicker = False
score = 0
powerup = False
power_counter = 0
eaten_ghost = [False, False, False, False]
moving = False
startup_counter = 0
lives = 3


# Draw the board. 32x32, Tile-based.
def draw_board():
    num1 = ((HEIGHT - 50) // 32)
    num2 = ((WIDTH) // 30)
    for i in range(len(level)):
        for j in range(len(level[i])):
            if level[i][j] == 1:
                pygame.draw.circle(
                    screen, 'white', (j * num2 + (0.5 * num2), i * num1 + (0.5 * num1)), 4)
            if level[i][j] == 2 and not flicker:
                pygame.draw.circle(
                    screen, 'white', (j * num2 + (0.5 * num2), i * num1 + (0.5 * num1)), 10)
            if level[i][j] == 3:
                pygame.draw.line(screen, color, (j * num2 + (0.5 * num2),
                                 i * num1), (j * num2 + (0.5 * num2), i * num1 + num1), 3)
            if level[i][j] == 4:
                pygame.draw.line(screen, color, (j * num2, i * num1 + (0.5 * num1)),
                                 (j * num2 + num2, i * num1 + (0.5 * num1)), 3)
            if level[i][j] == 5:
                pygame.draw.arc(screen, color, [
                                (j*num2 - (0.5*num2)), (i*num1+(0.5*num1)), num2, num1], 0, PI/2, 3)
            if level[i][j] == 6:
                pygame.draw.arc(screen, color, [
                                (j*num2+(0.5*num2)), (i*num1+(0.5*num1)), num2, num1], PI/2, PI, 3)
            if level[i][j] == 7:
                pygame.draw.arc(screen, color, [
                                (j*num2+(0.5*num2)), (i*num1-(0.5*num1)), num2, num1], PI, 3*PI/2, 3)
            if level[i][j] == 8:
                pygame.draw.arc(screen, color, [
                                (j*num2-(0.5*num2)), (i*num1-(0.5*num1)), num2, num1], 3*PI/2, 0, 3)
            if level[i][j] == 9:
                pygame.draw.line(screen, 'white', (j * num2, i * num1 +
                                 (0.5 * num1)), (j * num2 + num2, i * num1 + (0.5 * num1)), 3)


# Draw the player. Rotate according to the direction.
def draw_player():
    # 0-RIGHT, 1-LEFT, 2-UP, 3-DOWN
    if direction == 0:
        screen.blit(player_images[counter // 5], (player_x, player_y))
    elif direction == 1:
        screen.blit(pygame.transform.flip(
            player_images[counter // 5], True, False), (player_x, player_y))
    elif direction == 2:
        screen.blit(pygame.transform.rotate(
            player_images[counter // 5], 90), (player_x, player_y))
    elif direction == 3:
        screen.blit(pygame.transform.rotate(
            player_images[counter // 5], -90), (player_x, player_y))


# Check if next position is available.
def check_position(center_x, center_y):
    turns = [False, False, False, False]
    num1 = (HEIGHT - 50) // 32
    num2 = (WIDTH) // 30 
    num3 = 15
    # check collisions based on center_x and center_y of player +/- fudge number
    # check if center of player is within the board width()
    if center_x // 30 < 29:
        # right // returns opposite=True
        if direction == 0:
            if level[center_y // num1][(center_x - num3) // num2] < 3:
                turns[1] = True
        # left // returns opposite=True
        if direction == 1:
            if level[center_y // num1][(center_x + num3) // num2] < 3:
                turns[0] = True
        # up // returns opposite=True
        if direction == 2:
            if level[(center_y + num3) // num1][center_x // num2] < 3:
                turns[3] = True
        # down // returns opposite=True
        if direction == 3:
            if level[(center_y - num3) // num1][center_x // num2] < 3:
                turns[2] = True

        if direction == 2 or direction == 3:
            if 12 <= center_x % num2 <= 18:
                if level[(center_y + num3) // num1][center_x // num2] < 3:
                    turns[3] = True
                if level[(center_y - num3) // num1][center_x // num2] < 3:
                    turns[2] = True
            
            if 12 <= center_y % num1 <= 18:
                if level[center_y // num1][(center_x - num2)// num2] < 3:
                    turns[1] = True
                if level[center_y // num1][(center_x + num2)// num2] < 3:
                    turns[0] = True
        
        if direction == 0 or direction == 1:
            if 12 <= center_x % num2 <= 18:
                if level[(center_y + num1) // num1][center_x // num2] < 3:
                    turns[3] = True
                if level[(center_y - num1) // num1][center_x // num2] < 3:
                    turns[2] = True
            
            if 12 <= center_y % num1 <= 18:
                if level[center_y // num1][(center_x - num3) // num2] < 3:
                    turns[1] = True
                if level[center_y // num1][(center_x + num3) // num2] < 3:
                    turns[0] = True
    else:
        turns[0] = True
        turns[1] = True
    
    return turns


# Move player if next position is available and key is pressed or direction is set.
def move_player(move_x, move_y):
    # R, L, U, D
    if direction == 0 and turns_allowed[0]:
        move_x += player_speed
    elif direction == 1 and turns_allowed[1]:
        move_x -= player_speed

    if direction == 2 and turns_allowed[2]:
        move_y -= player_speed
    elif direction == 3 and turns_allowed[3]:
        move_y += player_speed
    return move_x, move_y

def check_collisions(scor, power, power_count, eaten_ghosts):
    num1 = (HEIGHT - 50) // 32
    num2 = WIDTH // 30
    if 0 < player_x < 870:
        if level[center_y // num1][center_x // num2] == 1:
            level[center_y // num1][center_x // num2] = 0
            scor += 10
        if level[center_y // num1][center_x // num2] == 2:
            level[center_y // num1][center_x // num2] = 0
            scor += 50
            power = True
            power_count = 0
            eaten_ghosts = [False, False, False, False]
    return scor, power, power_count, eaten_ghosts


def draw_misc():
    score_text = font.render(f'Score: {score}', True, 'white')
    #countdown_timer
    screen.blit(score_text, (10, 915))
    if powerup:
        pygame.draw.circle(screen, 'blue', (148, 930), 15)
    for i in range(lives):
        screen.blit(pygame.transform.scale(player_images[0], (26, 26)), (650 + i * 40, 918))


run = True
while run:
    timer.tick(fps)
    if counter < 19:
        counter += 1
        if counter > 3:
            flicker = False
    else:
        counter = 0
        flicker = True
    if powerup and power_counter < 600:
        power_counter += 1
    elif powerup and power_counter >= 600:
        power_counter = 0
        powerup = False
        eaten_ghost = [False, False, False, False]
    if startup_counter < 180:
        moving = False
        startup_counter += 1
    else:
        moving = True

    screen.fill('black')
    draw_board()
    draw_player()
    draw_misc()
    center_x = player_x + 23
    center_y = player_y + 24
    turns_allowed = check_position(center_x, center_y)
    if moving:
        player_x, player_y = move_player(player_x, player_y)

    score, powerup, power_counter, eaten_ghost = check_collisions(score, powerup, power_counter, eaten_ghost)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        # If a key is pressed
        if event.type == pygame.KEYDOWN:
            # If a specific key is pressed
            if event.key == pygame.K_RIGHT:
                direction_command = 0
            if event.key == pygame.K_LEFT:
                direction_command = 1
            if event.key == pygame.K_UP:
                direction_command = 2
            if event.key == pygame.K_DOWN:
                direction_command = 3


    # If moving in direction and next pos is available then keep moving
    if direction_command == 0 and turns_allowed[0]:
        direction = 0
    if direction_command == 1 and turns_allowed[1]:
        direction = 1
    if direction_command == 2 and turns_allowed[2]:
        direction = 2
    if direction_command == 3 and turns_allowed[3]:
        direction = 3

    if player_x > 900:
        player_x = -47
    elif player_x < -50:
        player_x = 897

    pygame.display.flip() # Updates to the visuals
pygame.quit()