import random

import pygame
import pygame as pg
from sys import exit
from button import Button
from player import *


class Collectable:
    def __init__(self):
        self.pos = Vector2(random.randint(-1280 * 2, 1280 * 2), random.randint(-720 * 2, 720 * 2))

    def update_pos(self, dir):
        self.pos.x += dir[0]
        self.pos.y += dir[1]

    def draw(self, win):
        pygame.draw.circle(win, (0, 255, 0), self.pos, 20)


pg.init()
screen = pg.display.set_mode((1280, 720), pg.RESIZABLE)
pg.display.set_caption("Menu")
Clock = pg.time.Clock()
background = pg.image.load("assets/Background.png")

player = Player(5, 10, 700, 80)

collectables = [Collectable() for _ in range(500)]


def get_font(size):  # supportive function
    return pg.font.Font("assets/font.ttf", size)


def play():  # what happens after play button gets clicked
    while True:
        screen_w, screen_h = pygame.display.get_window_size()

        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                items.append(Item(*pygame.mouse.get_pos(), 15, 15, (255, 0, 255)))

        player.move(items + collectables, screen_w, screen_h)
        screen.fill("black")
        player.draw(screen, items)

        for item in items:
            item.update(player)
        for collectable in collectables:
            collectable.draw(screen)

        collisions = player.rect.collidelistall([pygame.Rect(c.pos.x, c.pos.y, 20, 20) for c in collectables])
        player.score += len(collisions)
        for collision in collisions:
            collectables.pop(collision)
        # collectables = collectables_copy.copy()

        t = get_font(35).render(f"Score:{player.score}", True, (255, 255, 255))
        screen.blit(t, (10, 10))
        pg.display.update()
        Clock.tick(60)


def options_video():  # what happens after options -> video button gets clicked
    while True:
        options_video_mouse_pos = pg.mouse.get_pos()
        options_video_text = get_font(45).render("This is the VIDEO screen.", True, "gray")
        options_video_rect = options_video_text.get_rect(center=(640, 260))

        options_video_back = Button(image=None, pos=(640, 460),
                                    text_input="BACK", font=get_font(75), base_color="gray", hovering_color="Green")

        screen.fill("black")
        options_video_back.changeColor(options_video_mouse_pos)
        options_video_back.update(screen)
        screen.blit(options_video_text, options_video_rect)
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                exit()
            if event.type == pg.MOUSEBUTTONDOWN:  # what happens if a certain button gets clicked
                if options_video_back.checkForInput(options_video_mouse_pos):
                    options()
        pg.display.update()


def options_audio():  # what happens after options -> audio button gets clicked
    while True:
        options_audio_mouse_pos = pg.mouse.get_pos()
        options_audio_text = get_font(45).render("This is the PLAY screen.", True, "gray")
        options_audio_rect = options_audio_text.get_rect(center=(640, 260))
        screen.blit(options_audio_text, options_audio_rect)

        options_audio_back = Button(image=None, pos=(640, 460),
                                    text_input="BACK", font=get_font(75), base_color="gray", hovering_color="Green")

        screen.fill("black")
        options_audio_back.changeColor(options_audio_mouse_pos)
        options_audio_back.update(screen)
        options_text = get_font(45).render("This is the AUDIO screen.", True, "gray")
        options_rect = options_text.get_rect(center=(640, 260))
        screen.blit(options_text, options_rect)
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                exit()
            if event.type == pg.MOUSEBUTTONDOWN:  # what happens if a certain button gets clicked
                if options_audio_back.checkForInput(options_audio_mouse_pos):
                    options()
        pg.display.update()


def options():  # what happens after options button gets clicked
    while True:
        options_mouse_pos = pg.mouse.get_pos()
        screen.fill("black")

        options_text = get_font(45).render("This is the OPTIONS screen.", True, "gray")
        options_rect = options_text.get_rect(center=(640, 160))

        screen.blit(options_text, options_rect)

        options_audio_btn = Button(image=None, pos=(640, 260),
                                   text_input="AUDIO", font=get_font(75), base_color="gray", hovering_color="Green")
        options_video_btn = Button(image=None, pos=(640, 360),
                                   text_input="VIDEO", font=get_font(75), base_color="gray", hovering_color="Green")
        options_back = Button(image=None, pos=(640, 460),
                              text_input="BACK", font=get_font(75), base_color="gray", hovering_color="Green")
        options_buttons = [options_audio_btn, options_video_btn, options_back]
        options_back.changeColor(options_mouse_pos)
        options_back.update(screen)
        options_audio_btn.changeColor(options_mouse_pos)
        options_audio_btn.update(screen)
        options_video_btn.changeColor(options_mouse_pos)
        options_video_btn.update(screen)
        for button in options_buttons:
            button.changeColor(options_mouse_pos)
            button.update(screen)
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                exit()
            if event.type == pg.MOUSEBUTTONDOWN:  # what happens if a certain button gets clicked

                if options_audio_btn.checkForInput(options_mouse_pos):
                    options_audio()
                if options_video_btn.checkForInput(options_mouse_pos):
                    options_video()
                if options_back.checkForInput(options_mouse_pos):
                    main_menu()

        pg.display.update()


def main_menu():  # Main screen upon opening the game, showing the main menu
    while True:
        sw, sh = pygame.display.get_window_size()
        background_ = pygame.transform.scale(background,(sw,sh))
        screen.blit(background_, (0, 0))

        menu_mouse_pos = pg.mouse.get_pos()

        menu_text = get_font(100).render("MAIN MENU", True, "#b68f40")
        menu_rect = menu_text.get_rect(center=(sw // 2, int(sh*0.138888889)))

        play_button = Button(image=pg.image.load("assets/Play Rect.png"), pos=(sw // 2, int(sh * 0.347222222)),
                             text_input="PLAY", font=get_font(75), base_color="#d7fcd4", hovering_color="gray")
        options_button = Button(image=pg.image.load("assets/Options Rect.png"), pos=(sw // 2, int(sh * 0.555555556)),
                                text_input="OPTIONS", font=get_font(75), base_color="#d7fcd4", hovering_color="gray")
        quit_button = Button(image=pg.image.load("assets/Quit Rect.png"), pos=(sw // 2, int(sh * 0.763888889)),
                             text_input="QUIT", font=get_font(75), base_color="#d7fcd4", hovering_color="gray")
        buttons = [play_button, options_button, quit_button]
        screen.blit(menu_text, menu_rect)

        for button in buttons:
            button.changeColor(menu_mouse_pos)
            button.update(screen)

        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                exit()

            if event.type == pg.MOUSEBUTTONDOWN:  # what happens if a certain button gets clicked
                if play_button.checkForInput(menu_mouse_pos):
                    play()
                if options_button.checkForInput(menu_mouse_pos):
                    options()
                if quit_button.checkForInput(menu_mouse_pos):
                    pg.quit()
                    exit()

        pg.display.update()
        Clock.tick(60)


if __name__ == '__main__':
    main_menu()
