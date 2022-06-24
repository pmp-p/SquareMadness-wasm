import pygame as pg
from sys import exit
from button import Button

pg.init()

screen = pg.display.set_mode((1280, 720))
pg.display.set_caption("Menu")

BG = pg.image.load("assets/Background.png")


def get_font(size):  # Returns Press-Start-2P in the desired size
    return pg.font.Font("assets/font.ttf", size)


def play():
    while True:
        play_mouse_pos = pg.mouse.get_pos()

        screen.fill("black")

        play_text = get_font(45).render("This is the PLAY screen.", True, "gray")
        play_rect = play_text.get_rect(center=(640, 260))
        screen.blit(play_text, play_rect)

        play_back = Button(image=None, pos=(640, 460),
                           text_input="BACK", font=get_font(75), base_color="gray", hovering_color="Green")

        play_back.changeColor(play_mouse_pos)
        play_back.update(screen)

        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            if event.type == pg.MOUSEBUTTONDOWN:
                if play_back.checkForInput(play_mouse_pos):
                    main_menu()

        pg.display.update()


def options():
    while True:
        options_mouse_pos = pg.mouse.get_pos()

        screen.fill("black")

        options_text = get_font(45).render("This is the OPTIONS screen.", True, "gray")
        options_rect = options_text.get_rect(center=(640, 260))
        screen.blit(options_text, options_rect)

        options_back = Button(image=None, pos=(640, 460),
                              text_input="BACK", font=get_font(75), base_color="gray", hovering_color="Green")

        options_back.changeColor(options_mouse_pos)
        options_back.update(screen)

        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            if event.type == pg.MOUSEBUTTONDOWN:
                if options_back.checkForInput(options_mouse_pos):
                    main_menu()

        pg.display.update()


def main_menu():
    while True:
        screen.blit(BG, (0, 0))

        menu_mouse_pos = pg.mouse.get_pos()

        menu_text = get_font(100).render("MAIN MENU", True, "#b68f40")
        menu_rect = menu_text.get_rect(center=(640, 100))

        play_button = Button(image=pg.image.load("assets/Play Rect.png"), pos=(640, 250),
                             text_input="PLAY", font=get_font(75), base_color="#d7fcd4", hovering_color="gray")
        options_button = Button(image=pg.image.load("assets/Options Rect.png"), pos=(640, 400),
                                text_input="OPTIONS", font=get_font(75), base_color="#d7fcd4", hovering_color="gray")
        quit_button = Button(image=pg.image.load("assets/Quit Rect.png"), pos=(640, 550),
                             text_input="QUIT", font=get_font(75), base_color="#d7fcd4", hovering_color="gray")

        screen.blit(menu_text, menu_rect)

        for button in [play_button, options_button, quit_button]:
            button.changeColor(menu_mouse_pos)
            button.update(screen)

        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            if event.type == pg.MOUSEBUTTONDOWN:
                if play_button.checkForInput(menu_mouse_pos):
                    play()
                if options_button.checkForInput(menu_mouse_pos):
                    options()
                if quit_button.checkForInput(menu_mouse_pos):
                    pg.quit()
                    sys.exit()

        pg.display.update()


if __name__ == '__main__':
    main_menu()
