import pygame
from pygame.locals import *

# колір ракетки
paddle_col = (210, 210, 210)
paddle_outline = (100, 100, 100)


# класс ракетки
class Paddle:
    def __init__(self, screen_width, screen_height):
        self.direction = 0
        self.speed = 10
        self.width = 150
        self.height = 20
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.screen = pygame.display.set_mode((screen_width, screen_height))
        self.x = int((screen_width / 2) - (self.width / 2))
        self.y = screen_height - (self.height * 2)
        self.rect = Rect(self.x, self.y, self.width, self.height)

    def move(self):
        # скинути напрямок руху
        self.direction = 0
        key = pygame.key.get_pressed()
        if key[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.speed
            self.direction = -1
        if key[pygame.K_RIGHT] and self.rect.right < self.screen_width:
            self.rect.x += self.speed
            self.direction = 1

    def draw(self):
        pygame.draw.rect(self.screen, paddle_col, self.rect)
        pygame.draw.rect(self.screen, paddle_outline, self.rect, 3)

    def reset(self):
        # створити заново ракетку
        self.x = int((self.screen_width / 2) - (self.width / 2))
        self.y = self.screen_height - (self.height * 2)
        self.rect = Rect(self.x, self.y, self.width, self.height)
