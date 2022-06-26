import random

import pygame
import pygame as pg
from sys import exit
from button import Button
from player import *


# ! NOTES:
# ! add this sounds where a player powers up:
# power_up_sound = pg.mixer.Sound('assets/Sounds/powerupes.wav')
# power_up_sound.set_volume(0.05)
# power_up_sound.play()
# ! add this sounds where a player dies:
# death_sound = pg.mixer.Sound('assets/Sounds/death.wav')
# death_sound.set_volume(0.05)
# death_sound.play()
# ! add this sounds where a player wins:
# victory_sound = pg.mixer.Sound('assets/Sounds/8-bit-retro-success-victory.mp3')
# victory_sound.set_volume(0.05)
# victory_sound.play()

# turrets


class turrets:
    def __init__(self):
        super(turrets, self).__init__()


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
pg.display.set_caption("Menu ")
bg_music = pg.mixer.Sound('assets/music/geoswap-v3.wav')
bg_music.play(loops=-1)
bg_music.set_volume(0.3)
click_sound = pg.mixer.Sound('assets/Sounds/blipSelect.wav')
click_sound.set_volume(0.05)

Clock = pg.time.Clock()
background = pg.image.load("assets/Backgrounds/Background.png")

player = Player(5, 10, 700, 80)

collectables = [Collectable() for _ in range(150)]

wave_timer = pygame.USEREVENT + 1
pygame.time.set_timer(wave_timer, 5000)

wave_enemy_count = 10
wave_count = 0


def get_font(size):  # supportive function
    return pg.font.Font("assets/Fonts/font.ttf", size)


def adding_sprites():  # for loading the sprites
    triangle = pg.image.load('assets/Sprites/triangle-purple.png').convert_alpha()
    triangle_rect = triangle.get_rect()
    circle = pg.image.load('assets/Sprites/circle-green.png').convert_alpha()
    circle_rect = circle.get_rect(center=(400, 50))
    triangle_rect = triangle.get_rect(center=(600, 50))

    screen.blit(circle, circle_rect)
    screen.blit(triangle, triangle_rect)


def upgrade_screen():
    global wave_count
    screen_w, screen_h = pygame.display.get_window_size()
    size = 150
    exit_ = False
    upgrades = ["damage", shoot_rate]
    selected_upgrade = 0

    def upgrade(index, upgrade_select):
        if upgrade_select == shoot_rate:
            sides[index][upgrade_select] -= 10
        else:
            sides[index][upgrade_select] += 1

    while not exit_:
        screen.fill("black")
        t2 = get_font(20).render(f"Upgrade screen", True, (180, 180, 180))
        screen.blit(t2, (10, 10))

        t = get_font(20).render(f"Upgrade {upgrades[selected_upgrade]}", True, (180, 180, 180))
        screen.blit(t, (10, t2.get_height() + 10))

        pygame.draw.rect(screen, (255, 255, 255), ((screen_w // 2) - size, (screen_h // 2) - size, size * 2, size * 2),
                         5)
        t2 = get_font(20).render(f"(1)", True, (180, 180, 180))
        blit_center(screen, t2, (screen_w // 2 - (size + t2.get_width() + 10), screen_h // 2))

        t2 = get_font(20).render(f"(2)", True, (180, 180, 180))
        blit_center(screen, t2, (screen_w // 2, screen_h // 2 - (size + t2.get_height() + 10)))

        t2 = get_font(20).render(f"(3)", True, (180, 180, 180))
        blit_center(screen, t2, (screen_w // 2 + (size + t2.get_width() + 10), screen_h // 2))

        t2 = get_font(20).render(f"(4)", True, (180, 180, 180))
        blit_center(screen, t2, (screen_w // 2, screen_h // 2 + (size + t2.get_height() + 10)))

        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP: selected_upgrade -= 1
                if event.key == pygame.K_DOWN: selected_upgrade += 1
                if selected_upgrade > len(upgrades) - 1: selected_upgrade = 0
                if selected_upgrade < 0: selected_upgrade = len(upgrades) - 1

                selected_one = upgrades[selected_upgrade]

                if event.key == pygame.K_1:
                    upgrade(0, selected_one)
                    exit_ = True

                if event.key == pygame.K_2:
                    upgrade(1, selected_one)
                    exit_ = True

                if event.key == pygame.K_3:
                    upgrade(2, selected_one)
                    exit_ = True

                if event.key == pygame.K_4:
                    upgrade(3, selected_one)
                    exit_ = True
                player.update_side_date()
        pg.display.update()

    wave_count += 1
    spawn_enemy(screen_w, screen_h)


def spawn_enemy(screen_w, screen_h):
    for enemy_i in range(wave_enemy_count):
        i = random.random()
        if i < .25:
            x = random.randint(-screen_w, 0)
            y = random.randint(0, screen_h)
        elif i < .50:
            x = random.randint(screen_w, screen_w * 2)
            y = random.randint(0, screen_h)
        elif i < .75:
            x = random.randint(0, screen_w)
            y = random.randint(-screen_h, 0)

        else:
            x = random.randint(0, screen_w)
            y = random.randint(screen_h, screen_h * 2)

        items.append(Enemy(x, y, 30, 30, (255, 0, 0)))


shoot_event = pygame.USEREVENT + 2
pygame.time.set_timer(shoot_event, 500)


def play():  # what happens after play button gets clicked
    global wave_count
    screen_w, screen_h = pygame.display.get_window_size()
    while True:
        player.shoot()

        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                exit()
            if len(items) == 0:
                if wave_count % 3 == 0:
                    upgrade_screen()
                elif event.type == wave_timer:
                    wave_count += 1
                    spawn_enemy(screen_w, screen_h)

            # if event.type == shoot_event:
            #     # print(event.button)
            #     # if event.button == 1:
            #     # player.shoot()
            #     hit_sound = pg.mixer.Sound('assets/Sounds/hitHurt.wav')
            #     hit_sound.set_volume(0.05)
            #     hit_sound.play()
            #     # else:
            #     #     items.append(Enemy(*pygame.mouse.get_pos(), 30, 30, (255, 0, 255)))

        player.move(items + collectables, screen_w, screen_h)
        screen.fill("black")

        player.draw(screen, items, screen_w, screen_h)

        for item in items:
            item.update(player)
            for b in player.bullets:
                if item.rect.collidepoint(b["pos"].x, b["pos"].y):
                    item.health -= b["damage"]

                    if item.health <= 0 and item in items:
                        items.remove(item)

                    if b in player.bullets:
                        player.bullets.remove(b)

        for collectable in collectables:
            collectable.draw(screen)
        t = get_font(20).render(f"FPS: {round(Clock.get_fps(), 2)}", True, (180, 180, 180))
        screen.blit(t, (10, 50))
        t2 = get_font(20).render(f"Wave count: {wave_count}", True, (180, 180, 180))
        screen.blit(t2, (10, 50 + (t.get_height() + 10)))

        collisions = player.rect.collidelistall([pygame.Rect(c.pos.x, c.pos.y, 20, 20) for c in collectables])
        player.score += len(collisions)

        for collision in collisions:
            collect_sound = pg.mixer.Sound('assets/Sounds/pickupCoin.wav')
            collect_sound.set_volume(0.05)
            collect_sound.play()

            collectables.pop(collision)
        # collectables = collectables_copy.copy()

        t = get_font(34).render(f"Score:{player.score}", True, (255, 255, 255))
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
                click_sound.play()
                pg.quit()
                exit()
            if event.type == pg.MOUSEBUTTONDOWN:  # what happens if a certain button gets clicked
                if options_video_back.checkForInput(options_video_mouse_pos):
                    click_sound.play()
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
                click_sound.play()
                pg.quit()
                exit()
            if event.type == pg.MOUSEBUTTONDOWN:  # what happens if a certain button gets clicked
                if options_audio_back.checkForInput(options_audio_mouse_pos):
                    click_sound.play()
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
                click_sound.play()
                pg.quit()
                exit()
            if event.type == pg.MOUSEBUTTONDOWN:  # what happens if a certain button gets clicked

                if options_audio_btn.checkForInput(options_mouse_pos):
                    click_sound.play()
                    options_audio()
                if options_video_btn.checkForInput(options_mouse_pos):
                    click_sound.play()
                    options_video()
                if options_back.checkForInput(options_mouse_pos):
                    click_sound.play()
                    main_menu()

        pg.display.update()


def main_menu():  # Main screen upon opening the game, showing the main menu
    while True:
        sw, sh = pygame.display.get_window_size()
        background_ = pygame.transform.scale(background, (sw, sh))
        screen.blit(background_, (0, 0))

        menu_mouse_pos = pg.mouse.get_pos()

        menu_text = get_font(100).render("MAIN MENU", True, "#b68f40")
        menu_rect = menu_text.get_rect(center=(sw // 2, int(sh * 0.138888889)))

        play_button = Button(image=pg.image.load("assets/Buttons/Play Rect.png"), pos=(sw // 2, int(sh * 0.347222222)),
                             text_input="PLAY", font=get_font(75), base_color="#d7fcd4", hovering_color="gray")

        options_button = Button(image=pg.image.load("assets/Buttons/Options Rect.png"),
                                pos=(sw // 2, int(sh * 0.555555556)),
                                text_input="OPTIONS", font=get_font(75), base_color="#d7fcd4", hovering_color="gray")

        quit_button = Button(image=pg.image.load("assets/Buttons/Quit Rect.png"), pos=(sw // 2, int(sh * 0.763888889)),
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
