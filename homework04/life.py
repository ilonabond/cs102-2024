import pathlib
import random
import typing as tp

import pygame
from pygame.locals import *

Cell = tp.Tuple[int, int]
Cells = tp.List[int]
Grid = tp.List[Cells]


class GameOfLife:
    def __init__(
        self,
        size: tp.Tuple[int, int],
        randomize: bool = True,
        max_generations: tp.Optional[float] = float("inf"),
    ) -> None:
        self.rows, self.cols = size
        self.prev_generation = self.create_grid()
        self.curr_generation = self.create_grid(randomize=randomize)
        self.max_generations = max_generations
        self.generations = 1  # Начинаем с первого поколения

    def create_grid(self, randomize: bool = False) -> Grid:
        return [
            [random.randint(0, 1) if randomize else 0 for _ in range(self.cols)]
            for _ in range(self.rows)
        ]

    def get_neighbours(self, cell: Cell) -> Cells:
        row, col = cell
        neighbours = []

        for dr in (-1, 0, 1):
            for dc in (-1, 0, 1):
                if dr == 0 and dc == 0:
                    continue
                r, c = row + dr, col + dc
                if 0 <= r < self.rows and 0 <= c < self.cols:
                    neighbours.append(self.curr_generation[r][c])

        return neighbours

    def get_next_generation(self) -> Grid:
        next_generation = self.create_grid()

        for row in range(self.rows):
            for col in range(self.cols):
                live_neighbours = sum(self.get_neighbours((row, col)))

                if self.curr_generation[row][col] == 1:
                    if live_neighbours in (2, 3):
                        next_generation[row][col] = 1
                elif live_neighbours == 3:
                    next_generation[row][col] = 1

        return next_generation

    def step(self) -> None:
        """
        Выполнить один шаг игры.
        """
        if self.max_generations is not None and self.generations >= self.max_generations:
            return  # Если достигнут максимальный лимит, не увеличиваем поколение

        self.prev_generation = [row[:] for row in self.curr_generation]
        self.curr_generation = self.get_next_generation()
        self.generations += 1

    @property
    def is_max_generations_exceeded(self) -> bool:
        """
        Проверяет, превышено ли максимальное число поколений.
        """
        # Должно возвращать True, когда количество поколений **достигло** максимума
        return self.max_generations is not None and self.generations >= self.max_generations

    @property
    def is_changing(self) -> bool:
        """
        Проверка, изменилось ли состояние клеток с предыдущего шага.
        """
        return self.curr_generation != self.prev_generation
