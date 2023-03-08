import pygame
from wall import Wall
from paddle import Paddle
from ball import Ball
from os.path import exists

pygame.init()

# визначення розміру вікна гри
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))

# визначення назви в заголовку вікна
pygame.display.set_caption('Breakout')

# визначення шрифту
font = pygame.font.SysFont('Arial', 30)

# колір фону
bg = (0, 0, 0)

# колір тексту
text_col = (20, 212, 205)

# визначення рахунку
score = 0

# ігрові змінні
cols = 2
rows = 2
clock = pygame.time.Clock()
live_ball = False
game_over = 0
life = 3
if not exists("max_score.txt"):
    with open("max_score.txt", "w") as f:
        f.write("0")
        max_score = 0
else:
    with open("max_score.txt", "r") as f:
        max_score = int(f.read())


# функція для виводу тексту на екран
def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))


check_first_pressing = False

# створення стіни
wall = Wall(screen_width, screen_height, cols, rows)
wall.create_wall()

# створення ракетки
player_paddle = Paddle(screen_width, screen_height)

# створення м'ячу
ball = Ball(player_paddle.x + (player_paddle.width // 2),
            player_paddle.y - player_paddle.height,
            screen_width, screen_height, player_paddle)

run = True
while run:

    clock.tick(60)

    screen.fill(bg)

    if check_first_pressing:
        # малювання всіх створених об'єктів
        wall.draw_wall()
        player_paddle.draw()
        ball.draw()

        # друк рахунку та життя на екрані
        draw_text("Рахунок: " + str(score), font, text_col, 0, 0)
        draw_text("Життя: " + str(life), font, text_col, screen_width - 125, 0)

        if live_ball:
            # малювання ракетки
            player_paddle.move()
            # малювання м'ячу
            check_game = ball.move(wall)

            # перевірка статусу гри, життя та рахунку
            game_over = check_game[0]
            life = check_game[1]
            score += check_game[2]
            if game_over != 0:
                live_ball = False

    # друк тексту на екрані
    if not live_ball:
        if game_over == 0:
            draw_text("Кращий рахунок: " + str(max_score),
                      font, text_col, screen_width // 2 - 130, screen_height // 2 + 50)
            draw_text('Натисніть будь-де, щоб почати',
                      font, text_col, screen_width // 2 - 200, screen_height // 2 + 100)
        elif game_over == 1:
            draw_text("Ваш рахунок: " + str(score),
                      font, text_col, screen_width // 2 - 100, screen_height // 2)
            draw_text('Ви виграли!', font, text_col, screen_width // 2 - 75, screen_height // 2 + 50)
            draw_text('Натисніть будь-де, щоб перейти на наступний рівень',
                      font, text_col, 30, screen_height // 2 + 100)
        elif game_over == -1:
            draw_text("Ваш рахунок: " + str(score),
                      font, text_col, screen_width // 2 - 110, screen_height // 2)
            draw_text('Ви програли!', font, text_col, screen_width // 2 - 75, screen_height // 2 + 50)
            draw_text('Натисніть будь-де, щоб почати спочатку',
                      font, text_col, screen_width // 2 - 250, screen_height // 2 + 100)
            check_first_pressing = False
            if score > max_score:
                with open("max_score.txt", "w") as f:
                    f.write(str(score))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN and not live_ball:
            check_first_pressing = True
            if game_over == -1:
                score = 0
                cols = 3
                rows = 2
            else:
                if cols == rows:
                    cols += 1
                elif cols > rows:
                    rows += 1
            live_ball = True
            ball.reset()
            player_paddle.reset()
            wall.reset(cols, rows, screen_width, screen_height)

    pygame.display.update()

pygame.quit()
