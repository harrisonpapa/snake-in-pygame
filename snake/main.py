from pygame.locals import *
from random import randint
import pygame
import time
import os

os.system('clear')


class Bonus:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.step = 20

    def gen_pos(self):
        self.x = randint(1, 39) * self.step
        self.y = randint(1, 29) * self.step

    def render(self, display, img):
        display.blit(img, (self.x, self.y))


class Food:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.step = 20

    def gen_pos(self):
        self.x = randint(1, 39) * self.step
        self.y = randint(1, 29) * self.step

    def render(self, display, img):
        display.blit(img, (self.x, self.y))


class Snake:
    def __init__(self):
        self.x = []
        self.y = []
        self.step = 20
        self.direction = 0
        self.length = 400

        self.loop = 0

        for i in range(0, self.length):
            self.x.append(0)
            self.y.append(0)
        self.y[0] = 20

    def right(self):
        if self.direction != 1:
            self.direction = 0

    def left(self):
        if self.direction != 0:
            self.direction = 1

    def up(self):
        if self.direction != 3:
            self.direction = 2

    def down(self):
        if self.direction != 2:
            self.direction = 3

    def render(self, display, img):
        for i in range(0, self.length - 1):
            display.blit(img, (self.x[i], self.y[i]))

    def increase_length(self, length):
        self.length += length
        for i in range(length):
            self.x.append(0)
            self.y.append(0)

    def update(self):
        for i in range(self.length - 1, 0, -1):
            self.x[i] = self.x[i - 1]
            self.y[i] = self.y[i - 1]

        if self.direction == 0:
            if self.x[0] <= 760:
                self.x[0] += self.step
            else:
                self.x[0] = 0

        if self.direction == 1:
            if self.x[0] >= 20:
                self.x[0] -= self.step
            else:
                self.x[0] = 780

        if self.direction == 2:
            if self.y[0] >= 40:
                self.y[0] -= self.step
            else:
                self.y[0] = 580

        if self.direction == 3:
            if self.y[0] <= 560:
                self.y[0] += self.step
            else:
                self.y[0] = 20


class Game:
    width = 800
    height = 600

    def __init__(self):
        self.snake = Snake()
        self.food = Food()
        self.bonus = Bonus()
        self.running = True
        self.display_surf = None
        self.image_surf = None
        self.when_bonus = 0
        self.bonus_on_screen = False

        pygame.init()
        self.display_surf = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Python with PyGame")
        self.snake_img = pygame.image.load('snake.png').convert()
        self.food_img = pygame.image.load('food.png').convert()
        self.bonus_img = pygame.image.load('bonus.png').convert()

    def score_bar(self):
        pygame.draw.rect(self.display_surf, (255, 255, 255), (0, 0, 800, 20))
        font = pygame.font.SysFont("Arial", 16, True)
        text = font.render("Score: " + str(self.snake.length - 1), True, (0, 0, 0))
        text_rect = text.get_rect()
        self.display_surf.blit(text, (self.width / 2 - text_rect.width / 2, 1))
        pygame.display.update()

    def game_over(self):
        while self.running:
            self.display_surf.fill((0, 0, 0))
            font = pygame.font.SysFont("Arial", 52, True)
            text = font.render("Game Over!", True, (255, 255, 255))
            text_rect = text.get_rect()

            font = pygame.font.SysFont("Arial", 35, True)
            score = font.render("Score: " + str(self.snake.length - 1), True, (255, 255, 255))
            text_rect_2 = score.get_rect()

            font = pygame.font.SysFont("Arial", 28)
            details = font.render("Press ESC to exit. Press R to restart.", True, (255, 255, 255))
            text_rect_3 = details.get_rect()

            self.display_surf.blit(text, (self.width / 2 - text_rect.width / 2, self.height / 2 - 45))
            self.display_surf.blit(score, (self.width / 2 - text_rect_2.width / 2, self.height / 2 + 22))
            self.display_surf.blit(details, (self.width / 2 - text_rect_3.width / 2, self.height / 2 + 70))
            pygame.display.update()

            pygame.event.pump()
            keys = pygame.key.get_pressed()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            if keys[K_ESCAPE]:
                self.running = False

            if keys[K_r]:
                game_restart = Game()
                game_restart.loop()

    def render(self):
        self.display_surf.fill((0, 0, 0))
        self.snake.render(self.display_surf, self.snake_img)
        self.food.render(self.display_surf, self.food_img)
        self.bonus.render(self.display_surf, self.bonus_img)
        pygame.display.flip()

    def spawn_food(self):
        self.food.gen_pos()
        if self.bonus.x == self.food.x and self.bonus.y == self.food.y:
            self.food.gen_pos()

    def spawn_bonus(self):
        self.bonus.gen_pos()
        self.bonus_on_screen = True
        for i in range(1, self.snake.length):
            if self.bonus.x == self.snake.x[i] and self.bonus.y == self.snake.y[i]:
                self.bonus.gen_pos()

            if self.bonus.x == self.food.x and self.bonus.y == self.food.y:
                self.bonus.gen_pos()

    def col_with_food(self):
        if self.food.x == self.snake.x[0] and self.food.y == self.snake.y[0]:
            if not self.bonus_on_screen:
                self.when_bonus += 1
            self.snake.increase_length(1)
            self.food.gen_pos()
            for i in range(1, self.snake.length):
                if self.food.x == self.snake.x[i] and self.food.y == self.snake.y[i]:
                    self.food.gen_pos()

    def col_with_bonus(self):
        if self.bonus.x == self.snake.x[0] and self.bonus.y == self.snake.y[0]:
            self.bonus_on_screen = False
            self.when_bonus = 0
            self.snake.increase_length(3)
            self.bonus.x = 0
            self.bonus.y = 0

    def col_with_self(self):
        for i in range(1, self.snake.length):
            if self.snake.x[0] == self.snake.x[i] and self.snake.y[0] == self.snake.y[i]:
                self.game_over()

    def delay(self):
        for i in range(100):
            pygame.event.pump()
            keys = pygame.key.get_pressed()

            if keys[K_RIGHT]:
                self.snake.right()

            if keys[K_LEFT]:
                self.snake.left()

            if keys[K_UP]:
                self.snake.up()

            if keys[K_DOWN]:
                self.snake.down()

            if keys[K_ESCAPE]:
                self.running = False

            time.sleep(0.1 / 100)

    def exit(self):
        pygame.quit()

    def loop(self):
        self.spawn_food()
        self.spawn_bonus()
        while self.running:
            self.snake.loop += 1
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            pygame.event.pump()
            keys = pygame.key.get_pressed()

            if keys[K_RIGHT]:
                self.snake.right()

            if keys[K_LEFT]:
                self.snake.left()

            if keys[K_UP]:
                self.snake.up()

            if keys[K_DOWN]:
                self.snake.down()

            if keys[K_ESCAPE]:
                self.running = False

            self.snake.update()
            self.col_with_food()
            self.col_with_bonus()
            if self.snake.loop >= self.snake.length:
                self.col_with_self()
            if self.when_bonus == 5:
                self.when_bonus = 0
                self.spawn_bonus()
            self.render()
            self.score_bar()

            self.delay()

        self.exit()


if __name__ == '__main__':
    game = Game()
    game.loop()
