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

    def draw_grid(self) -> None:
        for x in range(0, self.width, self.cell_size):
            for y in range(0, self.height, self.cell_size):
                rect = pygame.Rect(x, y, self.cell_size, self.cell_size)
                color = (
                    (0, 255, 0) if self.life.curr_generation[y // self.cell_size][x // self.cell_size] else (0, 0, 0)
                )
                pygame.draw.rect(self.screen, color, rect)

    def run(self) -> None:
        clock = pygame.time.Clock()
        running = True
        while running and not self.life.is_max_generations_exceeded and self.life.is_changing:
            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False
            self.life.step()
            self.screen.fill((0, 0, 0))
            self.draw_grid()
            pygame.display.flip()
            clock.tick(10)
        pygame.quit()
