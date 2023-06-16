# PacMan with PyGame
from board import boards
import pygame
import math


pygame.init()


# Game Settings
WIDTH, HEIGHT = 900, 950
fps = 60
level = boards
color = 'blue'

# Player Settings
player_images = []
for i in range(1, 5):
    player_images.append(pygame.transform.scale(
        pygame.image.load(f'assets/player_images/{i}.png'), (45, 45)))
blinky_img = pygame.transform.scale(pygame.image.load('assets/ghost_images/red.png'), (45, 45))
pinky_img = pygame.transform.scale(pygame.image.load('assets/ghost_images/pink.png'), (45, 45))
inky_img = pygame.transform.scale(pygame.image.load('assets/ghost_images/blue.png'), (45, 45))
clyde_img = pygame.transform.scale(pygame.image.load('assets/ghost_images/orange.png'), (45, 45))
spooked_img = pygame.transform.scale(pygame.image.load('assets/ghost_images/powerup.png'), (45, 45))
dead_img = pygame.transform.scale(pygame.image.load('assets/ghost_images/dead.png'), (45, 45))
player_x, player_y = 440, 663
blinky_x, blinky_y, blinky_direction = 56, 58, 0
pinky_x, pinky_y, pinky_direction = 440, 438, 2
inky_x, inky_y, inky_direction = 440, 388, 2
clyde_x, clyde_y, clyde_direction = 440, 438, 2
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
targets = [(player_x, player_y), (player_x, player_y),
          (player_x, player_y), (player_x, player_y)]
blinky_dead, pinky_dead, inky_dead, clyde_dead = False, False, False, False
blinky_box, pinky_box, inky_box, clyde_box = False, False, False, False
ghost_speed = 2
# moving = False
moving = True
startup_counter = 0
lives = 3


class Ghost:
    def __init__(self, x_coord, y_coord, target, speed, img, direction, dead, box, id):
        self.x_pos, self.y_pos = x_coord, y_coord
        self.center_x, self.center_y = (self.x_pos + 22), (self.y_pos + 22)
        self.target = target
        self.speed = speed
        self.img = img
        self.in_box = box
        self.id = id
        self.direction = direction
        self.dead = dead
        self.turns, self.in_box = self.check_collisions()
        self.rect = self.draw()


    def draw(self):
        if (not powerup and not self.dead) or (eaten_ghost[self.id] and powerup and not self.dead):
            screen.blit(self.img, (self.x_pos, self.y_pos))
        elif powerup and not self.dead and not eaten_ghost[self.id]:
            screen.blit(spooked_img, (self.x_pos, self.y_pos))
        else:
            screen.blit(dead_img, (self.x_pos, self.y_pos))

        ghost_rect = pygame.rect.Rect((self.center_x - 18, self.center_y - 18), (36, 36))
        return ghost_rect


    def check_collisions(self):
        num1 = (HEIGHT - 50) // 32 # 28
        num2 = WIDTH // 30 # 30
        num3 = 15 
        self.turns = [False, False, False, False]

        # R L U D
        if self.center_x // 30 < 29:
            # Check RIGHT 
            if level[self.center_y // num1][(self.center_x + num3) // num2] < 3 \
                or (level[self.center_y // num1][(self.center_x + num3) // num2] == 9 and (
                    self.in_box or self.dead)):
                    self.turns[0] = True
            # Check LEFT
            if level[self.center_y // num1][(self.center_x - num3) // num2] < 3 \
                or (level[self.center_y // num1][(self.center_x - num3) // num2] == 9 and (
                    self.in_box or self.dead)):
                    self.turns[1] = True
            # Check UP
            if level[(self.center_y - num3) // num1][self.center_x // num2] < 3 \
                or (level[(self.center_y - num3) // num1][self.center_x // num2] == 9 and (
                    self.in_box or self.dead)):
                    self.turns[2] = True
            # Check DOWN
            if level[(self.center_y + num3) // num1][self.center_x // num2] < 3 \
                or (level[(self.center_y + num3) // num1][self.center_x // num2] == 9 and (
                    self.in_box or self.dead)):
                    self.turns[3] = True

            # Check up and down
            if self.direction == 2 or self.direction == 3:
                if 12 <= self.center_x % num2 < 18:
                    if level[(self.center_y + num3) // num1][self.center_x // num2] < 3 \
                        or (level[(self.center_y + num3) // num1][self.center_x // num2] == 0 \
                            and self.in_box or self.dead):
                        self.turns[3] = True
                    if level[(self.center_y - num3) // num1][self.center_x // num2] < 3 \
                        or (level[(self.center_y - num3) // num1][self.center_x // num2] == 0 \
                            and self.in_box or self.dead):
                        self.turns[2] = True
                if 12 <= self.center_y % num1 < 18:
                    if level[self.center_y // num1][(self.center_x - num2)// num2] < 3 \
                        or (level[self.center_y // num1][(self.center_x - num2 )// num2] == 0
                            and self.in_box or self.dead):
                        self.turns[0] = True
                    if level[self.center_y // num1][(self.center_x + num2)// num2] < 3 \
                        or (level[self.center_y // num1][(self.center_x + num2) // num2] == 0
                            and self.in_box or self.dead):
                        self.turns[1] = True
            
            # Check right and left
            if self.direction == 0 or self.direction == 1:
                if 12 <= self.center_x % num2 < 18:
                    if level[(self.center_y + num3) // num1][self.center_x // num2] < 3 \
                        or (level[(self.center_y + num3) // num1][self.center_x // num2] == 0 \
                            and self.in_box or self.dead):
                        self.turns[3] = True
                    if level[(self.center_y - num3) // num1][self.center_x // num2] < 3 \
                        or (level[(self.center_y - num3) // num1][self.center_x // num2] == 0 \
                            and self.in_box or self.dead):
                        self.turns[2] = True
                if 12 <= self.center_y % num1 < 18:
                    if level[self.center_y // num1][(self.center_x - num3)// num2] < 3 \
                        or (level[self.center_y // num1][(self.center_x - num3 )// num2] == 0
                            and self.in_box or self.dead):
                        self.turns[1] = True
                    if level[self.center_y // num1][(self.center_x + num3)// num2] < 3 \
                        or (level[self.center_y // num1][(self.center_x + num3) // num2] == 0
                            and self.in_box or self.dead):
                        self.turns[0] = True
        else:
            self.turns[0] = True
            self.turns[1] = True
        
        # Check if inside the middle box
        if 350 < self.x_pos < 550 and 370 < self.y_pos < 490:
            self.in_box = True
        else:
            self.in_box = False

        return  self.turns, self.in_box


    def move_clyde(self):
        # R L U D
        # Clyde is going to turn whenever advantageous for pursuit
        # IF RIGHT
        print(self.direction)
        print(self.turns)
        if self.direction == 0:
            # if targetX(to the right) > selfX and turnRight then GoRight
            if self.target[0] > self.x_pos and self.turns[0]:
                self.x_pos += self.speed
            #else if not turnRight
            elif not self.turns[0]:
                # if targetY (lower on the board) > selfY and turnDown
                if self.target[1] > self.y_pos and self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                # else if targetY(above on the board) < selfY and TurnUp
                elif self.target[1] < self.y_pos and self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                # else if targetX(to the left) < selfX and turnLeft
                elif self.target[0] < self.x_pos and self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                #else if turnDown
                elif self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                #else if turnUp
                elif self.turns[2]:
                    self.direction = 2
                    self.y_pos += self.speed
                #else if turnLeft
                elif self.turns[1]:
                     self.direction = 1
                     self.x_pos -= self.speed
            elif self.turns[0]:
                if self.target[1] > self.y_pos and self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                if self.target[1] < self.y_pos and self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                else:
                    self.x_pos += self.speed
        # IF LEFT                    
        elif self.direction == 1:
            # if targetY > selfY and turnDown then Direction=Down
            if self.target[1] > self.y_pos and self.turns[3]:
                self.direction = 3
            # else if targetX(is to the left) < selfX and turnUp then Go
            elif self.target[0] < self.x_pos and self.turns[1]:
                self.x_pos -= self.speed
            # else if not turnUp
            elif not self.turns[1]:
                if self.target[1] > self.y_pos and self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.target[1] < self.y_pos and self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.target[0] > self.x_pos and self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
                elif self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.turns[2]:
                    self.direction = 2
                    self.y_pos += self.speed
                elif self.turns[0]:
                     self.direction = 1
                     self.x_pos += self.speed
            elif self.turns[1]:
                if self.target[1] > self.y_pos and self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                if self.target[1] < self.y_pos and self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                else:
                    self.x_pos -= self.speed
        # IF UP
        elif self.direction == 2:
            if self.target[0] < self.x_pos and self.turns[0]:
                self.direction = 0
                self.x_pos -= self.speed
            elif self.target[1] < self.y_pos and self.turns[2]:
                self.y_pos -= self.speed
            elif not self.turns[2]:
                if self.target[0] > self.x_pos and self.turns[0]:
                    self.direction = 0
                    self.y_pos += self.speed
                elif self.target[0] < self.x_pos and self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                elif self.target[1] > self.y_pos and self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                elif self.turns[0]:
                     self.direction = 1
                     self.x_pos += self.speed
            elif self.turns[2]:
                if self.target[0] > self.x_pos and self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
                if self.target[0] < self.x_pos and self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                else:
                    self.x_pos -= self.speed
        # IF DOWN
        elif self.direction == 3:
            if self.target[1] > self.y_pos and self.turns[3]:
                self.y_pos += self.speed
            elif not self.turns[3]:
                if self.target[0] > self.x_pos and self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
                elif self.target[0] < self.x_pos and self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                elif self.target[1] < self.y_pos and self.turns[2]:
                    self.direction = 2
                    self.y_pos += self.speed
                elif self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                elif self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
            elif self.turns[3]:
                if self.target[0] > self.x_pos and self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
                if self.target[0] < self.x_pos and self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                else:
                    self.y_pos += self.speed
        if self.x_pos < -30:
            self.x_pos = 900
        elif self.x_pos > 900:
            self.x_pos - 30
        return self.x_pos, self.y_pos, self.direction


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


def draw_misc():
    score_text = font.render(f'Score: {score}', True, 'white')
    # countdown_timer
    screen.blit(score_text, (10, 915))
    if powerup:
        pygame.draw.circle(screen, 'blue', (148, 930), 15)
    for i in range(lives):
        screen.blit(pygame.transform.scale(
            player_images[0], (26, 26)), (650 + i * 40, 918))


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


# def get_targets(blink_x, blink_y, ink_x, ink_y, pink_x, pink_y, clyd_x, clyd_y):
#     if player_x < 450:
#         runaway_x = 900
#     else:
#         runaway_x = 0
#     if player_y < 450:
#         runaway_y = 900
#     else:
#         runaway_y = 0
#     return_target = (380, 400)

#     if powerup:
#         if not blinky_dead:
#             blink_target = (runaway_x, runaway_y)
#         else:
#             blink_target = return_target

#         if not inky_dead:
#             ink_target = (runaway_x, player_y)
#         else:
#             ink_target = return_target

#         if not pinky_dead:
#             pink_target = (player_x, runaway_y)
#         else:
#             pink_target = return_target

#         if not clyde_dead:
#             clyd_target = (450, 450)
#         else:
#             clyd_target = return_target
#     else:
#         if not blinky_dead:
#             if 340 < blink_y < 560 and 560 < blink_y < 500:
#                 blink_target = (400, 100)
#             else:
#                 blink_target = (player_x, player_y)
#         else:
#             blink_target = return_target

#         if not inky_dead:
#             if 340 < ink_y < 560 and 560 < ink_y < 500:
#                 ink_target = (400, 100)
#             else:
#                 ink_target = (player_x, player_y)
#         else:
#             ink_target = return_target

#         if not pinky_dead:
#             if 340 < pink_y < 560 and 560 < pink_y < 500:
#                 pink_target = (400, 100)
#             else:
#                 pink_target = (player_x, player_y)
#         else:
#             pink_target = return_target

#         if not clyde_dead:
#             if 340 < clyd_y < 560 and 560 < clyd_y < 500:
#                 clyd_target = (400, 100)
#             else:
#                 clyd_target = (player_x, player_y)
#         else:
#             clyd_target = return_target
    
#     return target_list


#Explaination here soon
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
    # targets = get_targets(blinky_x, blinky_y, inky_x, inky_y, pinky_x, pinky_y, clyde_x, clyde_y)
    blinky = Ghost(blinky_x, blinky_y, targets[0], ghost_speed, blinky_img, blinky_direction, blinky_dead, blinky_box , 0)
    inky = Ghost(inky_x, inky_y, targets[2], ghost_speed, inky_img, inky_direction, inky_dead, inky_box , 1)
    pinky = Ghost(pinky_x, pinky_y, targets[1], ghost_speed, pinky_img, pinky_direction, pinky_dead, pinky_box, 2)
    clyde = Ghost(clyde_x, clyde_y, targets[3], ghost_speed, clyde_img, clyde_direction, clyde_dead, clyde_box, 3)
    center_x = player_x + 23
    center_y = player_y + 24
    turns_allowed = check_position(center_x, center_y)
    if moving:
        player_x, player_y = move_player(player_x, player_y)
        blinky_x, blinky_y, blinky_direction = blinky.move_clyde()
        pinky_x, pinky_y, pinky_direction = pinky.move_clyde()
        inky_x, inky_y, inky_direction = inky.move_clyde()
        clyde_x, clyde_y, clyde_direction = clyde.move_clyde()

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

    pygame.display.flip() # Refresh screen
pygame.quit()