import typing as tp

import pygame
from life import GameOfLife
from pygame.locals import *
from ui import UI


class GUI(UI):
    def __init__(self, life: GameOfLife, cell_size: int = 20) -> None:
        super().__init__(life)
        self.cell_size = cell_size
        self.width = self.life.cols * self.cell_size
        self.height = self.life.rows * self.cell_size
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.init()
        self.paused = False  # Новый атрибут для управления паузой

    def draw_grid(self) -> None:
        for x in range(0, self.width, self.cell_size):
            for y in range(0, self.height, self.cell_size):
                rect = pygame.Rect(x, y, self.cell_size, self.cell_size)
                color = (
                    (0, 255, 0) if self.life.curr_generation[y // self.cell_size][x // self.cell_size] else (0, 0, 0)
                )
                pygame.draw.rect(self.screen, color, rect, 0)
                pygame.draw.rect(self.screen, (50, 50, 50), rect, 1)  # Рамки клеток

    def toggle_cell(self, pos: tp.Tuple[int, int]) -> None:
        """Изменить состояние клетки при клике."""
        x, y = pos
        row = y // self.cell_size
        col = x // self.cell_size
        self.life.curr_generation[row][col] ^= 1  # Инвертировать состояние клетки

    def run(self) -> None:
        clock = pygame.time.Clock()
        running = True

        while running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False
                elif event.type == KEYDOWN:
                    if event.key == K_SPACE:  # Пробел для паузы
                        self.paused = not self.paused
                elif event.type == MOUSEBUTTONDOWN and self.paused:
                    self.toggle_cell(event.pos)

            if not self.paused:
                if not self.life.is_changing or self.life.is_max_generations_exceeded:
                    break  # Завершить игру при условии остановки
                self.life.step()

            self.screen.fill((0, 0, 0))
            self.draw_grid()
            pygame.display.flip()
            clock.tick(10)

        pygame.quit()


if __name__ == "__main__":
    life = GameOfLife((20, 20), max_generations=100)
    gui = GUI(life, cell_size=20)
    gui.run()
