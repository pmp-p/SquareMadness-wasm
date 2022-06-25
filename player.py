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
        # print(dx, dy, self.rect.center)


test_obstacle = Item(50, 50, 30, 30, (255, 0, 0))
items = [test_obstacle]

stats = {
    "triangle": {
        "img": pygame.image.load("assets/Sprites/triangle-purple.png"),
        "bullet_speed": 10

    }
}


def blit_center(screen, surface: pygame.Surface, position: Vector2):
    w, h = surface.get_width(), surface.get_height()
    screen.blit(surface, (position[0] - w // 2, position[1] - h // 2))


class Player:
    def __init__(self, speed, health, x, y):
        self.speed = speed
        self.health = health
        self.score = 0
        self.rect = pygame.rect.Rect(x, y, 50, 50)

        self.state = "triangle"
        self.tmp_bullet = {
            'pos': Vector2(0, 0),
            "vel": Vector2(0, 0)

        }
        self.bullets = []
        self.img = stats[self.state]["img"].convert_alpha()
        self.img = pygame.transform.scale(self.img, self.rect.size)

    def draw(self, screen, items, w, h):
        # placing = 360 / (self.score+1)
        # prev = None
        # for i in range(self.score+1):
        #     ang = i * placing
        #     ang = math.radians(ang)
        #     rad = self.rect.w
        #     x = math.cos(ang) * rad
        #     y = math.sin(ang) * rad
        #     # print(x+500, y+500)
        #     if prev is not None:
        #         # pygame.draw.line(screen, (255, 255, 255), (x + self.rect.centerx, y + self.rect.centery),                                 (prev[0] + self.rect.centerx, prev[1] + self.rect.centery), 2)
        #
        #         pygame.draw.line(screen, (255, 255, 255), (x + self.rect.centerx, y + self.rect.centery),
        #                          (prev[0] + self.rect.centerx, prev[1] + self.rect.centery), 2)
        #     prev = x, y

        # pygame.draw.rect(screen, (255, 255, 255), self.rect)
        angle = math.atan2(self.rect.y - pygame.mouse.get_pos()[1], self.rect.x - pygame.mouse.get_pos()[0])
        rotated_img = pygame.transform.rotozoom(self.img, math.degrees(-angle) + 90, 1)

        blit_center(screen, rotated_img, self.rect.center)

        for item in items:
            item.draw(screen)

        for bullet in self.bullets:
            if not 0 < bullet["pos"].x < w or not 0 < bullet["pos"].y < h:
                if bullet in self.bullets:
                    self.bullets.remove(bullet)
            pygame.draw.circle(screen, (255, 255, 255), bullet["pos"], 2)
            bullet["pos"] += bullet["vel"] * stats[self.state]["bullet_speed"]

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

    def shoot(self):
        tmp = self.tmp_bullet.copy()
        tmp["pos"] = Vector2(*self.rect.center)
        angle = math.atan2(pygame.mouse.get_pos()[1] - self.rect.y, pygame.mouse.get_pos()[0] - self.rect.x)
        tmp["vel"] = tmp["vel"].copy()
        tmp["vel"].x = math.cos(angle)
        tmp["vel"].y = math.sin(angle)

        self.bullets.append(tmp.copy())
