import pygame
from const import *

from pygame.locals import (
    RLEACCEL,
    K_LEFT,
    K_RIGHT,
    K_a,
    K_d,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
)

pygame.init()

myfont = pygame.font.SysFont("monospace", 16)
pygame.display.set_caption("Pong")

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))


class Player(pygame.sprite.Sprite):
    def __init__(self, player_no):
        super(Player, self).__init__()
        self.surf = pygame.Surface((75, 15))
        self.surf.fill((255, 255, 255))
        self.rect = self.surf.get_rect(center=player_no[1])
        self.player_no = player_no[0]
        self.score = 0

    def update(self, pressed_keys):
        if self.player_no == 1:
            if pressed_keys[K_LEFT]:
                self.rect.move_ip(-PLAYER_SPEED, 0)
            if pressed_keys[K_RIGHT]:
                self.rect.move_ip(PLAYER_SPEED, 0)
        elif self.player_no == 2:
            if pressed_keys[K_a]:
                self.rect.move_ip(-PLAYER_SPEED, 0)
            if pressed_keys[K_d]:
                self.rect.move_ip(PLAYER_SPEED, 0)
        # Keep player on the screen
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH


class Ball(pygame.sprite.Sprite):
    def __init__(self):
        super(Ball, self).__init__()
        self.surf = pygame.Surface((10, 10))
        self.surf.fill((255, 0, 0))
        self.rect = self.surf.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2))
        self.x_heading = CENTER
        self.y_heading = TOP
        self.start_timer = 120

    def update(self):
        # start delay
        if self.start_timer != 0:
            self.start_timer -= 1
            return
        # bounce
        if ball.rect.left <= 0:
            self.x_heading = RIGHT
        elif ball.rect.right >= SCREEN_WIDTH:
            self.x_heading = LEFT
        # normal move
        self.rect.move_ip(self.x_heading, self.y_heading)

        # Border collisions
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        if self.rect.top < 15:
            self.rect.top = 15
        if self.rect.bottom > SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT

    def change_heading(self, x_heading, y_heading):
        self.x_heading = x_heading
        self.y_heading = y_heading

    def reset_position(self):
        self.rect = self.surf.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2))
        self.start_timer = 120
        # self.rect.move(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)


player1 = Player(PLAYER_1)
player2 = Player(PLAYER_2)
ball = Ball()

all_sprites = pygame.sprite.Group()

all_sprites.add(player1)
all_sprites.add(player2)

all_sprites.add(ball)


running = True


def event_handler(events):
    running = True
    for event in events:
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                running = False
        elif event.type == QUIT:
            running = False
    return running
    pass

def paddle_collision_handler(pressed_keys):
    if pygame.sprite.collide_rect(player1, ball):
        if pressed_keys[K_LEFT]:
            ball.change_heading(LEFT, BOTTOM)
        elif pressed_keys[K_RIGHT]:
            ball.change_heading(RIGHT, BOTTOM)
        elif ball.x_heading == RIGHT:
            ball.change_heading(LEFT, BOTTOM)
        else:
            ball.change_heading(RIGHT, BOTTOM)

    if pygame.sprite.collide_rect(player2, ball):
        if pressed_keys[K_a]:
            ball.change_heading(LEFT, TOP)
        elif pressed_keys[K_d]:
            ball.change_heading(RIGHT, TOP)
        elif ball.x_heading == RIGHT:
            ball.change_heading(LEFT, TOP)
        else:
            ball.change_heading(RIGHT, TOP)

def calculate_score():
    if ball.rect.bottom == SCREEN_HEIGHT:
        player1.score += 1
        ball.change_heading(CENTER, TOP)
        ball.reset_position()
    elif ball.rect.top <= 15:
        player2.score += 1
        ball.change_heading(CENTER, BOTTOM)
        ball.reset_position()

    p1_score = myfont.render("P1 Score = " + str(player1.score), 1, (255, 255, 255))
    p2_score = myfont.render("P2 Score = " + str(player2.score), 1, (255, 255, 255))
    return p1_score,p2_score

def game_loop():
    running = event_handler(pygame.event.get())

    pressed_keys = pygame.key.get_pressed()
    player1.update(pressed_keys)
    player2.update(pressed_keys)

    screen.fill((0, 0, 0))
    pygame.draw.line(screen, (255, 255, 255), (0, 15), (SCREEN_WIDTH, 15))

    paddle_collision_handler(pressed_keys)
    p1_score, p2_score = calculate_score()
    ball.update()

    screen.blit(p1_score, (10, 0))
    screen.blit(p2_score, (SCREEN_WIDTH - 145, 0))

    for entity in all_sprites:
        screen.blit(entity.surf, entity.rect)

    pygame.display.flip()
    clock.tick(120)

    return running


clock = pygame.time.Clock()
while running:
    running = game_loop()
