import pygame
import sys
import random


pygame.init()


WIDTH, HEIGHT = 1280, 1024
BALL_RADIUS = 40
PADDLE_WIDTH, PADDLE_HEIGHT = 20, 120
FPS = 60
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)


def draw_text(text, font, color, surface, x, y):
    textobj = font.render(text, 1, color)
    textrect = textobj.get_rect()
    textrect.center = (x, y)
    surface.blit(textobj, textrect)


def play_multiplayer(starting_speed):
    paddle1_speed = 0
    paddle2_speed = 0
    paddle1_y = HEIGHT // 2 - PADDLE_HEIGHT // 2
    paddle2_y = HEIGHT // 2 - PADDLE_HEIGHT // 2
    ball_speed_x = starting_speed * random.choice((1, -1))
    ball_speed_y = starting_speed * random.choice((1, -1))
    ball_x = WIDTH // 2
    ball_y = HEIGHT // 2

    
    acceleration = 1.05

    
    score1 = 0
    score2 = 0

    
    font_score = pygame.font.Font(None, 72)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return  
                if event.key == pygame.K_w:
                    paddle1_speed = -8
                elif event.key == pygame.K_s:
                    paddle1_speed = 8
                elif event.key == pygame.K_UP:
                    paddle2_speed = -8
                elif event.key == pygame.K_DOWN:
                    paddle2_speed = 8
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_w or event.key == pygame.K_s:
                    paddle1_speed = 0
                elif event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                    paddle2_speed = 0

       
        paddle1_y += paddle1_speed
        paddle2_y += paddle2_speed

        if paddle1_y < 0:
            paddle1_y = 0
        elif paddle1_y > HEIGHT - PADDLE_HEIGHT:
            paddle1_y = HEIGHT - PADDLE_HEIGHT

        if paddle2_y < 0:
            paddle2_y = 0
        elif paddle2_y > HEIGHT - PADDLE_HEIGHT:
            paddle2_y = HEIGHT - PADDLE_HEIGHT

     
        ball_x += ball_speed_x
        ball_y += ball_speed_y

        
        if ball_y <= 0 or ball_y >= HEIGHT - BALL_RADIUS:
            ball_speed_y = -ball_speed_y
            ball_speed_x *= acceleration

        
        if (
            (ball_x <= PADDLE_WIDTH and paddle1_y <= ball_y <= paddle1_y + PADDLE_HEIGHT)
            or (ball_x >= WIDTH - PADDLE_WIDTH - BALL_RADIUS and paddle2_y <= ball_y <= paddle2_y + PADDLE_HEIGHT)
        ):
            ball_speed_x = -ball_speed_x
            ball_speed_x *= acceleration

        
        if ball_x < 0:
            score2 += 1
            ball_x = WIDTH // 2
            ball_y = HEIGHT // 2
            ball_speed_x = starting_speed * random.choice((1, -1))
            ball_speed_y = starting_speed * random.choice((1, -1))
        elif ball_x > WIDTH:
            score1 += 1
            ball_x = WIDTH // 2
            ball_y = HEIGHT // 2
            ball_speed_x = -starting_speed * random.choice((1, -1))
            ball_speed_y = starting_speed * random.choice((1, -1))

        
        screen.fill(BLACK)

        
        pygame.draw.line(screen, WHITE, (WIDTH // 2, 0), (WIDTH // 2, HEIGHT), 2)

        
        pygame.draw.rect(screen, WHITE, pygame.Rect(0, paddle1_y, PADDLE_WIDTH, PADDLE_HEIGHT))
        pygame.draw.rect(screen, WHITE, pygame.Rect(WIDTH - PADDLE_WIDTH, paddle2_y, PADDLE_WIDTH, PADDLE_HEIGHT))
        pygame.draw.ellipse(screen, WHITE, pygame.Rect(ball_x, ball_y, BALL_RADIUS, BALL_RADIUS))

        draw_text(str(score1), font_score, WHITE, screen, WIDTH // 4, 20)
        draw_text(str(score2), font_score, WHITE, screen, 3 * WIDTH // 4 - 20, 20)

        pygame.display.flip()
        clock.tick(FPS)
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("MUMIPET")
font_title = pygame.font.Font(None, 72)
font_buttons = pygame.font.Font(None, 36)
clock = pygame.time.Clock()
starting_speed = 5

while True:
    screen.fill(BLACK)

    draw_text("MUMIPET", font_title, WHITE, screen, WIDTH // 2, HEIGHT // 4)

    mouse_x, mouse_y = pygame.mouse.get_pos()
    play_button = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 - 25, 200, 50)
    two_player_button = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 + 75, 200, 50)

    pygame.draw.rect(screen, WHITE, play_button)
    pygame.draw.rect(screen, WHITE, two_player_button)

    draw_text("Играть", font_buttons, BLACK, screen, WIDTH // 2, HEIGHT // 2 - 15)
    draw_text("Играть вдвоем", font_buttons, BLACK, screen, WIDTH // 2, HEIGHT // 2 + 85)

    draw_text("Скорость мяча: {}".format(starting_speed), font_buttons, WHITE, screen, WIDTH // 2, HEIGHT // 2 + 150)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if play_button.collidepoint(mouse_x, mouse_y):
                print("Играть")
                play_multiplayer(starting_speed)
            elif two_player_button.collidepoint(mouse_x, mouse_y):
                play_multiplayer(starting_speed)
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            confirm_exit = pygame.Rect(WIDTH // 4, HEIGHT // 2 - 50, WIDTH // 2, 100)
            pygame.draw.rect(screen, WHITE, confirm_exit)
            draw_text("Вы точно хотите выйти?", font_buttons, BLACK, screen, WIDTH // 2, HEIGHT // 2)
            pygame.display.flip()
            pygame.time.delay(2000)

    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP]:
        starting_speed += 1
    elif keys[pygame.K_DOWN] and starting_speed > 1:
        starting_speed -= 1

    pygame.display.flip()
    clock.tick(FPS)
