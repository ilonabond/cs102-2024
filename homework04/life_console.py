import curses
import sys
from pathlib import Path

from life import GameOfLife
from ui import UI


class Console(UI):
    def __init__(self, life: GameOfLife) -> None:
        super().__init__(life)

    def draw_borders(self, screen) -> None:
        """Отобразить рамку."""
        screen.border(0)

    def draw_grid(self, screen) -> None:
        """Отобразить состояние клеток."""
        for i, row in enumerate(self.life.curr_generation):
            for j, cell in enumerate(row):
                char = "█" if cell else " "
                screen.addch(i + 1, j + 1, char)

    def run(self) -> None:
        """Главный цикл игры в консоли."""
        screen = curses.initscr()
        curses.curs_set(0)  # Скрыть курсор
        screen.nodelay(True)  # Сделать ввод с клавиатуры неблокирующим
        running = True

        try:
            while running:
                screen.clear()
                self.draw_borders(screen)
                self.draw_grid(screen)
                screen.refresh()

                key = screen.getch()
                if key == ord("q"):  # Завершить игру на клавишу 'q'
                    running = False

                if not self.life.is_changing or self.life.is_max_generations_exceeded:
                    running = False  # Завершить игру при остановке изменений
                self.life.step()
                curses.napms(200)  # Задержка обновления (200 мс)
        finally:
            curses.endwin()


if __name__ == "__main__":
    if len(sys.argv) > 1:
        filepath = Path(sys.argv[1])
        life = GameOfLife.from_file(filepath)
    else:
        life = GameOfLife((10, 10), randomize=True, max_generations=50)

    console = Console(life)
    console.run()
