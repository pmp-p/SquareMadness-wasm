import math

import pygame
from pygame.math import Vector2


class Item:
    SPEED = 2

    def __init__(self, x, y, w, h, color):
        self.rect = pygame.Rect(x, y, w, h)
        self.dir = Vector2()
        self.color = color

    def draw(self, win):
        pygame.draw.rect(win, self.color, self.rect)

    def update_pos(self, dir):
        self.rect.x += dir[0]
        self.rect.y += dir[1]

    def update(self, player):
        self.move(player)

    def get_direction_to_player(self, player):
        angle = math.atan2(player.rect.y - self.rect.y, player.rect.x - self.rect.x)
        return math.cos(angle), math.sin(angle)

    def move(self, player):
        dx, dy = self.get_direction_to_player(player)

        self.rect.x += dx * self.SPEED
        self.rect.y += dy * self.SPEED
        print(dx, dy, self.rect.center)


test_obstacle = Item(50, 50, 15, 15, (255, 0, 0))
items = [test_obstacle]


class Player:
    def __init__(self, speed, health, x, y):
        self.speed = speed
        self.health = health
        self.score = 0
        self.rect = pygame.rect.Rect(x, y, 50, 50)

    def draw(self, screen, items):

        pygame.draw.rect(screen, (255, 255, 255), self.rect)
        for item in items:
            item.draw(screen)

    def move(self, items, w, h):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_w]:
            if self.rect.top > 75:
                self.rect.y -= self.speed
            else:
                for item in items:
                    item.update_pos((0, self.speed))

        elif keys[pygame.K_s]:
            if self.rect.bottom < h - 75:
                self.rect.y += self.speed
            else:
                for item in items:
                    item.update_pos((0, -self.speed))

        if keys[pygame.K_a]:
            if self.rect.left > 75:
                self.rect.x -= self.speed
            else:
                for item in items:
                    item.update_pos((+self.speed, 0))

        elif keys[pygame.K_d]:
            if self.rect.right < w - 75:
                self.rect.x += self.speed
            else:
                for item in items:
                    item.update_pos((-self.speed, 0))
