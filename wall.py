import pygame
import random

# колір цеглин
block_red = (255, 0, 0)
block_green = (0, 255, 0)
block_blue = (0, 0, 255)


# класс стіни
class Wall:
    def __init__(self, screen_width, screen_height, cols, rows):
        self.reset(cols, rows, screen_width, screen_height)

    def create_wall(self):
        # визначення порожнього списку для окремих блоків
        for row in range(self.rows):
            # скидання списку рядків цеглин
            block_row = []
            # перехід до кожного стовпця в цьому рядку
            for col in range(self.cols):
                # визначення x та y позиції для кожної цеглини та створення прямокутника на цих координатах
                block_x = col * self.width
                block_y = row * self.height + 50
                rect = pygame.Rect(block_x, block_y, self.width, self.height)
                # визначення здоров'я для цеглин
                health = random.randint(1, 3)
                score_per_block = 100
                if health == 2:
                    score_per_block = 200
                elif health == 3:
                    score_per_block = 300
                # створення списку індивідуальної цеглини з параметрами
                block_individual = [rect, health, score_per_block]
                # додавання списку індивідуальної цеглини до списку рядку цеглин
                block_row.append(block_individual)
            # додавання рядку цеглин до повного списку цеглин
            self.blocks.append(block_row)

    def draw_wall(self):
        for row in self.blocks:
            for block in row:
                # визначення кольору цеглини в залежності від здоров'я цеглини
                if block[1] == 3:
                    block_col = block_blue
                elif block[1] == 2:
                    block_col = block_green
                elif block[1] == 1:
                    block_col = block_red
                pygame.draw.rect(self.screen, block_col, block[0])
                pygame.draw.rect(self.screen, (0, 0, 0), block[0], 2)

    def reset(self, cols, rows, screen_width, screen_height):
        self.blocks = []
        self.width = screen_width // cols
        self.screen = pygame.display.set_mode((screen_width, screen_height))
        self.height = 30
        self.cols = cols
        self.rows = rows
        self.cols = cols
        self.rows = rows
        self.create_wall()
