import pygame
from pygame.locals import *
from paddle import paddle_col, paddle_outline


# класс м'ячу
class Ball:
    def __init__(self, x, y, screen_width, screen_height, player_paddle):
        self.ball_rad = 10
        self.x = x - self.ball_rad
        self.y = y
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.player_paddle = player_paddle
        self.screen = pygame.display.set_mode((screen_width, screen_height))
        self.speed_max = 20
        self.speed_y = -4
        self.speed_x = 4
        self.game_over = 1
        self.life = 3

    def move(self, wall):
        # поріг зіткнення
        collision_thresh = 6
        wall_destroyed = 1
        row_count = 0
        score = 0

        for row in wall.blocks:
            item_count = 0
            for item in row:
                # перевірка зіткнення
                if self.rect.colliderect(item[0]):
                    # перевірка, чи зіткнення було зверху від цегли
                    if abs(self.rect.bottom - item[0].top) < collision_thresh and self.speed_y > 0:
                        self.speed_y *= -1
                    # перевірка, чи зіткнення було знизу від цегли
                    if abs(self.rect.top - item[0].bottom) < collision_thresh and self.speed_y < 0:
                        self.speed_y *= -1
                    # перевірка, чи зіткнення було ліворуч від цегли
                    if abs(self.rect.right - item[0].left) < collision_thresh and self.speed_x > 0:
                        self.speed_x *= -1
                    # перевірка, чи зіткнення було праворуч від цегли
                    if abs(self.rect.left - item[0].right) < collision_thresh and self.speed_x < 0:
                        self.speed_x *= -1
                    # зменшення здоров'я цегли, при завдані йому пошкодження
                    if wall.blocks[row_count][item_count][1] > 1:
                        wall.blocks[row_count][item_count][1] -= 1
                    else:
                        wall.blocks[row_count][item_count][0] = (0, 0, 0, 0)
                        score += wall.blocks[row_count][item_count][2]
                        # збільшення швидкості м'яча при зруйнувані цеглини
                        if self.speed_x > 0:
                            self.speed_x += 1
                        else:
                            self.speed_x -= 1

                # перевірка, чи цеглина ще не зруйнована
                if wall.blocks[row_count][item_count][0] != (0, 0, 0, 0):
                    wall_destroyed = 0
                # збільшення лічильника item_counter
                item_count += 1
            # збільшення лічильника row_counter
            row_count += 1
        # після проходження всіх ітерацій, йде перевірка, чи зруйнована стіна
        if wall_destroyed == 1:
            self.game_over = 1

        # перевірка зіткнень з лівою та правою границями екрану
        if self.rect.left < 0 or self.rect.right > self.screen_width:
            self.speed_x *= -1

        # перевірка зіткнень з верхньою та нижньою границями екрану
        if self.rect.top < 0:
            self.speed_y *= -1
        if self.rect.bottom > self.screen_height:
            self.life -= 1
            self.rect = Rect(self.x, self.y, self.ball_rad * 2, self.ball_rad * 2)
            self.speed_y = -4
            self.speed_x = 4
        if self.life <= 0:
            self.game_over = -1

        # перевірка зіткнення з ракеткою
        if self.rect.colliderect(self.player_paddle):
            # перевірка зіткнення зверху ракетки
            if abs(self.rect.bottom - self.player_paddle.rect.top) < collision_thresh and self.speed_y > 0:
                self.speed_y *= -1
                if self.speed_x > self.speed_max:
                    self.speed_x = self.speed_max
                elif self.speed_x < 0 and self.speed_x < -self.speed_max:
                    self.speed_x = -self.speed_max
            else:
                self.speed_x *= -1

        self.rect.x += self.speed_x
        self.rect.y += self.speed_y

        return (self.game_over, self.life, score)

    def draw(self):
        pygame.draw.circle(self.screen, paddle_col,
                           (self.rect.x + self.ball_rad, self.rect.y + self.ball_rad),
                           self.ball_rad)
        pygame.draw.circle(self.screen, paddle_outline,
                           (self.rect.x + self.ball_rad, self.rect.y + self.ball_rad),
                           self.ball_rad, 3)

    def reset(self):
        # створити заново м'яч
        self.rect = Rect(self.x, self.y, self.ball_rad * 2, self.ball_rad * 2)
        self.speed_y = -4
        self.speed_x = 4
        self.game_over = 0
        self.life = 3
