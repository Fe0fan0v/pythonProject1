import pygame
import pygame_gui
import os
from pygame_widgets import Button
from PIL import Image
from constants import dict_colors, dictionary, colors

size = 1920, 1080
flag_game = False
list_images = os.listdir('image/big_fraction')


def load_image(name, color_key=None):
    fullname = os.path.join('image', name)
    try:
        image = pygame.image.load(fullname).convert()
    except pygame.error as message:
        print('Такого файла не существует')
        raise SystemExit(message)
    if color_key is not None:
        color_key = image.get_at((0, 0))
        image.set_colorkey(color_key)
    else:
        image = image.convert_alpha()
    return image


def blit_pil_image(screen, img, position):
    image = Image.open(img)
    image.resize((400, 400), Image.ANTIALIAS)
    pygame_image = pygame.image.fromstring(image.tobytes(), image.size, "RGBA")
    screen.blit(pygame_image, position)


def choice(screen, index=0):
    blit_pil_image(screen, 'image/arrow_r.png', (1050, 500))
    blit_pil_image(screen, 'image/arrow_l.png', (750, 500))
    screen.blit(load_image(f'big_fraction/{list_images[index]}', color_key=(0, 0, 0)), (800, 400))
    screen.fill(dict_colors[colors[list_images[index]]], pygame.Rect(750, 700, 300, 35))
    screen.blit(pygame.font.Font("fonts/пр.ttf", 18).render(f"{dictionary[colors[list_images[index]]]}",
                                                                True, (220, 220, 220)), (840, 708))


def not_flag():
    global flag_game
    flag_game = True


def start_screen():
    pygame.init()
    screen = pygame.display.set_mode(size)
    first_box = False
    second_box = False
    third_box = False
    fourth_box = False
    button = Button(
        screen, 800, 810, 200, 35, pressedColour=(78, 102, 122), inactiveColour=(58, 82, 102),
        textColour=(220, 220, 220), fontSize=30,
        hoverColour=(68, 92, 112), text='Начать игру', onRelease=lambda: not_flag())
    pygame.display.set_caption('GUI')
    clock = pygame.time.Clock()

    manager = pygame_gui.UIManager(size)

    all_sprites = pygame.sprite.Group()
    ng_bt = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((775, 280), (360, 100)),
                                         text='New game',
                                         manager=manager)
    ct_bt = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((775, 405), (360, 100)),
                                         text='Continue',
                                         manager=manager)
    dw_bt = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((775, 530), (360, 100)),
                                         text='Load savefile',
                                         manager=manager)
    ex_bt = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((775, 655), (360, 100)),
                                         text='Exit',
                                         manager=manager)

    bg_image = load_image('window/bg.jpg')
    ng_image = load_image('window/ng.png')
    ct_image = load_image('window/ct.png')
    ex_image = load_image('window/ex.png')
    dw_image = load_image('window/dw.png')
    ng = pygame.sprite.Sprite(all_sprites)
    ct = pygame.sprite.Sprite(all_sprites)
    ex = pygame.sprite.Sprite(all_sprites)
    dw = pygame.sprite.Sprite(all_sprites)
    ng.image = ng_image
    ct.image = ct_image
    ex.image = ex_image
    dw.image = dw_image
    ng.rect = ng.image.get_rect()
    ng.rect.topleft = 775, 280
    ct.rect = ct.image.get_rect()
    ct.rect.topleft = 775, 405
    dw.rect = dw.image.get_rect()
    dw.rect.topleft = 775, 530
    ex.rect = dw.image.get_rect()
    ex.rect.topleft = 775, 655
    choice_flag = False
    index = 0
    running = True
    while running:
        time_delta = clock.tick(60) / 1000.0
        for event in pygame.event.get():
            mouse = pygame.mouse.get_pos()
            if event.type == pygame.QUIT:
                running = False
            if flag_game:
                return dictionary[colors[list_images[index]]]
            if event.type == pygame.USEREVENT:
                if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == ex_bt:
                        running = False
                    if event.ui_element == ng_bt:
                        choice_flag = True
            if mouse:
                if not first_box and (775 <= mouse[0] <= 1135 and 280 <= mouse[1] <= 380):
                    ng_h_image = load_image('window/ng_h.png')
                    ng_h = pygame.sprite.Sprite(all_sprites)
                    ng_h.image = ng_h_image
                    ng_h.rect = ng_h.image.get_rect()
                    ng_h.rect.topleft = 775, 280
                    first_box = True

                if first_box and (mouse[0] < 775 or mouse[0] > 1135 or mouse[1] < 280 or mouse[1] > 380):
                    first_box = False
                    ng_h.kill()

                if not second_box and (775 <= mouse[0] <= 1135 and 405 <= mouse[1] <= 505):
                    ct_h_image = load_image('window/ct_h.png')
                    ct_h = pygame.sprite.Sprite(all_sprites)
                    ct_h.image = ct_h_image
                    ct_h.rect = ct_h.image.get_rect()
                    ct_h.rect.topleft = 775, 405
                    second_box = True

                if second_box and (mouse[0] < 775 or mouse[0] > 1135 or mouse[1] < 405 or mouse[1] > 505):
                    second_box = False
                    ct_h.kill()

                if not third_box and (775 <= mouse[0] <= 1135 and 530 <= mouse[1] <= 630):
                    dw_h_image = load_image('window/dw_h.png')
                    dw_h = pygame.sprite.Sprite(all_sprites)
                    dw_h.image = dw_h_image
                    dw_h.rect = dw_h.image.get_rect()
                    dw_h.rect.topleft = 775, 530
                    third_box = True

                if third_box and (mouse[0] < 775 or mouse[0] > 1135 or mouse[1] < 530 or mouse[1] > 630):
                    third_box = False
                    dw_h.kill()

                if not fourth_box and (775 <= mouse[0] <= 1135 and 655 <= mouse[1] <= 755):
                    ex_h_image = load_image('window/ex_h.png')
                    ex_h = pygame.sprite.Sprite(all_sprites)
                    ex_h.image = ex_h_image
                    ex_h.rect = ex_h.image.get_rect()
                    ex_h.rect.topleft = 775, 655
                    fourth_box = True

                if fourth_box and (mouse[0] < 775 or mouse[0] > 1135 or mouse[1] < 655 or mouse[1] > 755):
                    fourth_box = False
                    ex_h.kill()
            key = pygame.key.get_pressed()
            if key[pygame.K_ESCAPE]:
                running = False
            if key[pygame.K_RIGHT]:
                if index < len(list_images) - 1:
                    index += 1
                else:
                    index = 0
            elif key[pygame.K_LEFT]:
                if index > 0:
                    index -= 1
                else:
                    index = len(list_images) - 1
            if event.type == pygame.MOUSEBUTTONDOWN:
                if 1050 <= mouse[0] <= 1090 and 500 <= mouse[1] <= 540:
                    if index < len(list_images) - 1:
                        index += 1
                    else:
                        index = 0
                elif 750 <= mouse[0] <= 790 and 500 <= mouse[1] <= 540:
                    if index > 0:
                        index -= 1
                    else:
                        index = len(list_images) - 1
        screen.blit(bg_image, (0, 0))
        if not choice_flag:
            manager.process_events(event)
            manager.update(time_delta)
            manager.draw_ui(screen)
            all_sprites.draw(screen)
        else:
            button.listen(pygame.event.get())
            button.draw()
            choice(screen, index)
        pygame.display.flip()
        pygame.display.update()


start_screen()
