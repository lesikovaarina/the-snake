"""Игра Змейка на PyGame."""
import sys
from random import choice, randint

import pygame as pg

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
SCREEN_CENTER = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Направления движения:
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Цвета для отрисовки объектов:
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (93, 216, 228)

BOARD_BACKGROUND_COLOR = BLACK
BORDER_COLOR = BLUE
APPLE_COLOR = RED
SNAKE_COLOR = GREEN

# Скорость движения змейки:
SPEED = 20

# Настройка игрового окна:
screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pg.display.set_caption('Змейка')

# Настройка времени:
clock = pg.time.Clock()


# Классы игры.
class GameObject:
    """Базовый класс для игровых объектов."""

    def __init__(self, body_color=None, position=SCREEN_CENTER):
        """Задаёт позицию и цвет объекта."""
        self.position = position
        self.body_color = body_color

    def draw(self):
        """Метод отрисовки объекта на экране для наследования."""
        raise NotImplementedError(
            f"Метод draw() не определен в классе {self.__class__.__name__}."
        )

    def draw_cell(self, position, body_color=None, border_color=BORDER_COLOR):
        """Метод отрисовки клетки на экране."""
        color = body_color or self.body_color
        rect = pg.Rect(position, (GRID_SIZE, GRID_SIZE))
        pg.draw.rect(screen, color, rect)
        pg.draw.rect(screen, border_color, rect, 1)


class Apple(GameObject):
    """Класс яблока."""

    def __init__(self, occupied_positions=(), body_color=APPLE_COLOR):
        """Задаёт цвет яблока и случайную позицию на игровом поле."""
        super().__init__(body_color)
        self.randomize_position(occupied_positions)

    def draw(self):
        """Метод отрисовки яблока на экране."""
        self.draw_cell(self.position, self.body_color)

    def randomize_position(self, occupied_positions=()):
        """Метод задаёт случайную позицию яблока на свободном участке поля."""
        while True:
            self.position = (
                randint(0, GRID_WIDTH - 1) * GRID_SIZE,
                randint(0, GRID_HEIGHT - 1) * GRID_SIZE
            )
            if self.position not in occupied_positions:
                break


class Snake(GameObject):
    """Класс змейки."""

    def __init__(self, body_color=SNAKE_COLOR):
        """Задаёт цвет змейки, длину и начальную позицию."""
        super().__init__(body_color)
        self.reset()
        self.direction = RIGHT
        self.last = None

    def update_direction(self):
        """Метод обновляет направление движения змейки."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def move(self):
        """Метод перемещает змейку в текущем направлении."""
        head_x, head_y = self.get_head_position()
        dx, dy = self.direction
        new_head = (head_x + dx * GRID_SIZE, head_y + dy * GRID_SIZE)
        new_head = (
            new_head[0] % SCREEN_WIDTH,
            new_head[1] % SCREEN_HEIGHT
        )
        self.positions.insert(0, new_head)
        if len(self.positions) > self.length:
            self.last = self.positions.pop()
        else:
            self.last = None

    def draw(self):
        """Метод отрисовки змейки на экране."""
        for position in self.positions[:-1]:
            self.draw_cell(position, self.body_color)

        # Отрисовка головы змейки
        self.draw_cell(self.get_head_position(), self.body_color)

        # Затирание последнего сегмента
        if self.last:
            self.draw_cell(
                self.last, BOARD_BACKGROUND_COLOR, BOARD_BACKGROUND_COLOR
            )

    def get_head_position(self):
        """Метод возвращает позицию головы змейки."""
        return self.positions[0]

    def reset(self):
        """Метод сбрасывает змейку в начальное состояние."""
        self.length = 1
        self.positions = [self.position]
        self.direction = choice([UP, DOWN, LEFT, RIGHT])
        self.next_direction = None


def handle_keys(game_object):
    """Функция обработки действий пользователя."""
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            sys.exit()
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_UP and game_object.direction != DOWN:
                game_object.next_direction = UP
            elif event.key == pg.K_DOWN and game_object.direction != UP:
                game_object.next_direction = DOWN
            elif event.key == pg.K_LEFT and game_object.direction != RIGHT:
                game_object.next_direction = LEFT
            elif event.key == pg.K_RIGHT and game_object.direction != LEFT:
                game_object.next_direction = RIGHT


def main():
    """Основной игровой цикл."""
    pg.init()
    # Экземпляры классов.
    snake = Snake()
    apple = Apple(snake.positions)

    while True:
        clock.tick(SPEED)
        handle_keys(snake)
        snake.update_direction()
        snake.move()

        if snake.get_head_position() == apple.position:
            snake.length += 1
            apple.randomize_position(snake.positions)
        elif snake.get_head_position() in snake.positions[4:]:
            snake.reset()
            screen.fill(BOARD_BACKGROUND_COLOR)
            apple.randomize_position(snake.positions)
        snake.draw()
        apple.draw()
        pg.display.update()


if __name__ == '__main__':
    main()
