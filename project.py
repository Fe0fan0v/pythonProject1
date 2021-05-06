import pygame
import os
from pygame_widgets import Button
import sqlite3
from PIL import Image
from constants import *
from main_wind import *


def load_image(name, color_key=None):
    fullname = os.path.join('image', name)
    try:
        image = pygame.image.load(fullname).convert()
    except pygame.error as message:
        print('Такого файла не существует')
        raise SystemExit(message)
    if color_key is not None:
        image.set_colorkey(color_key)
    else:
        image = image.convert_alpha()
    return image


class ScreenFrame(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.rect = (0, 0, 1920, 1080)


class SpriteGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()

    def get_event(self, event):
        for sprite in self:
            sprite.get_event(event)


pygame.init()
FPS = 60
show_army = False
clock = pygame.time.Clock()
pygame.display.set_caption('Повторение')
screen = pygame.display.set_mode((1920, 1080))
all_sprites = SpriteGroup()
orders_sprites = SpriteGroup()
winning_tokens = SpriteGroup()
king_tokens = SpriteGroup()
small_things = SpriteGroup()
garrisons_group = SpriteGroup()
army = ''
astra_fraction_dict = {}
window_barrel, window_house = False, False
message_flag, move_flag = False, False
button_time = Button(screen, 1726, 979, 81, 81, radius=20, pressedColour=(255, 255, 255),
                     image=pygame.image.load('image/tokens/time_button.png'), onRelease=lambda: move())
button = Button(
    screen, 1840, 900, 60, 60, radius=50, pressedColour=(99, 129, 129), inactiveColour=(49, 79, 79),
    hoverColour=(79, 109, 109),
    image=load_image('tokens/homes.png', color_key=(0, 0, 0)), onRelease=lambda: window_b('h'))
button_barrel = Button(
    screen, 1840, 800, 60, 60, radius=50, pressedColour=(99, 129, 129), inactiveColour=(49, 79, 79),
    hoverColour=(79, 109, 109),
    image=load_image('tokens/barrel.png', color_key=(0, 0, 0)), onRelease=lambda: window_b('b'))
barrel_quit = Button(
    screen, 850, 900, 150, 27, pressedColour=(70, 70, 90), inactiveColour=(30, 30, 38), textColour=(220, 220, 220),
    hoverColour=(50, 50, 74), text='Вернуться на карту', onRelease=lambda: window_b('b'))
army_quit = Button(
    screen, 700, 750, 150, 27, pressedColour=(218, 195, 135), inactiveColour=(238, 215, 155),
    textColour=(50, 50, 50),
    hoverColour=(228, 205, 145), text='Вернуться на карту', onRelease=lambda show_army: not show_army)
message_quit = Button(
    screen, 700, 710, 150, 27, pressedColour=(218, 195, 135), inactiveColour=(238, 215, 155),
    textColour=(50, 50, 50),
    hoverColour=(228, 205, 145), text='Вернуться на карту', onRelease=lambda: not_message())
connect = sqlite3.connect('data/armies.sqlite')
iron_throne = ''
l_games = True
move_flag = False
valyrian_sword = ''
messenger_crow = ''
abandoned_orders = []
m_army, m_ter, m_lst = '', [], []


class Sprite(pygame.sprite.Sprite):

    def __init__(self, group):
        super().__init__(group)
        self.rect = None

    def get_event(self, event):
        pass


class Army(Sprite):
    def __init__(self, army_type, pos, composition):
        super().__init__(all_sprites)
        self.image = load_image(f'fractions/{army_type}', color_key=(0, 0, 0))
        self.armies = {'white.png': 'Старк', 'yellow.png': 'Баратеон', 'red.png': 'Ланнистер', 'black.png': 'Гренджой',
                       'green.png': 'Тирелл', 'orange.png': 'Мартелл', 'blue.png': 'Аррен'}
        self.territory = pos
        self.rect = self.image.get_rect().move(
            TERRITORY_DICT[ALL_TERRITORIES[self.territory]][0], TERRITORY_DICT[ALL_TERRITORIES[self.territory]][1])
        self.fraction = self.armies[army_type]
        for i in composition:
            composition[composition.index(i)] == i + '.png'
        self.detachment = ','.join(composition)
        # cursor = connect.cursor()
        # cursor.execute(f"""INSERT INTO composition VALUES ('{self.fraction}', '{self.detachment}') """)
        # connect.commit()
        self.order = f'shirt_orders/{army_type}'
        self.list_images = os.listdir('image/orders')
        if astra_fraction_dict[self.fraction] == 0:
            for i in self.list_images:
                if '_a' in i:
                    del self.list_images[self.list_images.index(i)]
        self.order_sprite = Order((920, 500), self.list_images)

    def get_event(self, event):
        global show_army
        if self.rect.collidepoint(event.pos):
            show_composition(screen, self)
            show_army = True
            return True
        return False

    def movement(self, territory, lst=[]):
        x_1 = self.rect[0]
        y_1 = self.rect[1]
        for i in range(len(lst)):
            new = Army(f'{DICT[self.fraction]}.png', self.territory, lst[i])
            new.order = self.order
            x_2 = TERRITORY_DICT[ALL_TERRITORIES[territory[i]]][0]
            y_2 = TERRITORY_DICT[ALL_TERRITORIES[territory[i]]][1]
            k = (y_2 - y_1) / (x_2 - x_1)
            b = y_1 - k * x_1
            det_lst = self.detachment.split(',')
            for j in lst[i]:
                del det_lst[det_lst.index(j)]
            self.detachment = ','.join(det_lst)
            while new.rect[0] != x_2 and new.rect[1] != y_2:
                if x_1 < x_2:
                    x_1 += 1
                    y_1 = k * x_1 + b
                elif x_1 > x_2:
                    x_1 -= 1
                    y_1 = k * x_1 + b
                if x_1 == x_2:
                    if y_1 > y_2:
                        y_1 -= 1
                new.rect = new.image.get_rect().move(x_1, y_1)
                screen.blit(new.image, new.rect)
            if ALL_TERRITORIES[new.territory] not in SEAS and \
                    ALL_TERRITORIES[self.territory] not in [16, 25, 51, 36, 31, 44, 26]:
                abandoned_orders.append((new.fraction, ALL_TERRITORIES[self.territory]))
                astra_dict[DICT[new.fraction]] -= 1
            new.territory = territory[i]
            pygame.display.flip()
        if territory[-1] != self.territory:
            x_1 = self.rect[0]
            y_1 = self.rect[1]
            x_2 = TERRITORY_DICT[ALL_TERRITORIES[territory[-1]]][0]
            y_2 = TERRITORY_DICT[ALL_TERRITORIES[territory[-1]]][1]
            k = (y_2 - y_1) / (x_2 - x_1)
            b = y_1 - k * x_1
            while self.rect[0] != x_2 and self.rect[1] != y_2:
                if x_1 < x_2:
                    x_1 += 1
                    y_1 = k * x_1 + b
                elif x_1 > x_2:
                    x_1 -= 1
                    y_1 = k * x_1 + b
                if x_1 == x_2:
                    if y_1 > y_2:
                        y_1 -= 1
                self.rect = self.image.get_rect().move(x_1, y_1)
                screen.blit(self.image, self.rect)
            self.territory = territory[-1]


class Small_things(Sprite):
    def __init__(self, args):
        super().__init__(small_things)
        self.image_text = args[0]
        if args[0] == 'arrow_l.png':
            self.image = load_image(f'arrow_l.png', color_key=(0, 0, 0))
            self.rect = self.image.get_rect().move(870, 520)
        elif args[0] == 'arrow_r.png':
            self.image = load_image(f'arrow_r.png', color_key=(0, 0, 0))
            self.rect = self.image.get_rect().move(1010, 520)
        elif args[0] == 'wildling_token.png':
            self.image = load_image('tokens/wildling_token.png', color_key=(0, 0, 0))
            self.dict_wildling = {0: 450, 2: 505, 4: 560, 6: 615, 8: 670, 10: 725, 12: 780}
            self.value = args[1]
            self.rect = self.image.get_rect().move(1495, self.dict_wildling[self.value])
        elif args[0] == 'time_token.png':
            self.image = load_image('tokens/time_token.png', color_key=(0, 0, 0))
            self.dict_time = {1: 30, 2: 75, 3: 122, 4: 167, 5: 215, 6: 260, 7: 307, 8: 352, 9: 400, 10: 447}
            self.value = args[1]
            self.rect = self.image.get_rect().move(self.dict_time[self.value], 50)

    def get_event(self, event):
        if left.rect.collidepoint(event.pos):
            army.order_sprite.get_event(event, 1)
        if right.rect.collidepoint(event.pos):
            army.order_order_sprite.get_event(event, -1)

    def draw(self, screen):
        screen.blit(self.image, self.rect)


class Win_token(Sprite):
    def __init__(self, image, place):
        super().__init__(winning_tokens)
        self.image = load_image(f'tokens/{image}', color_key=(0, 0, 0))
        self.place = place
        y_bias = self.bias()
        self.rect = self.image.get_rect().move(WINNING_TOKEN[place][0], WINNING_TOKEN[place][1] + y_bias)

    def bias(self):
        bia = 0
        for spr in winning_tokens:
            if spr.place == self.place:
                bia += 1
        return (bia - 1) * 10


class Kings_token(Sprite):
    def __init__(self, image, place, scale):
        super().__init__(king_tokens)
        fraction_dict = {'blue.png': 'Аррен', 'red.png': 'Ланнистер', 'black.png': 'Гренджой', 'green.png': 'Тирелл',
                         'orange.png': 'Мартелл', 'white.png': 'Старк', 'yellow.png': 'Баратеон'}
        self.fraction = fraction_dict[image]
        self.scale = scale
        self.place = place
        place_dict = {1: 650, 2: 730, 3: 810, 4: 890, 5: 972, 6: 1052, 7: 1135}
        scale_dict = {'throne': 18, 'sword': 98, 'crow': 176}
        if image == 'blue.png':
            image = 'blue_win.png'
        self.image = load_image(f'shirt_orders/{image}', color_key=(0, 0, 0))
        if image != 'blue_win.png':
            self.image = pygame.transform.scale(self.image, (60, 60))
        else:
            self.image = pygame.transform.scale(self.image, (55, 55))
        self.rect = self.image.get_rect().move(
            place_dict[place], scale_dict[scale])
        if scale == 'crow':
            if place in [1, 2]:
                self.astra = 3
            elif place == 3:
                self.astra = 2
            elif place == 4:
                self.astra = 1
            else:
                self.astra = 0


class Garrisons(Sprite):
    def __init__(self, fract):
        super().__init__(garrisons_group)
        self.image = load_image(f'garrisons/{fract}.png', color_key=(0, 0, 0))
        self.fract = fract
        fract_dict = {'red': (570, 450), 'white': (1250, 650), 'black': (800, 370), 'blue': (700, 770),
                      'yellow': (570, 920), 'green': (300, 450), 'orange': (160, 910), 'kings_port': (510, 710)}
        self.rect = self.image.get_rect().move(fract_dict[fract][0], fract_dict[fract][1])


class Order(Sprite):
    def __init__(self, pos, list_images, image='help.png'):
        super().__init__(orders_sprites)
        self.list_images = list_images
        self.image = load_image(f'orders/{self.list_images[0]}', color_key=(0, 0, 0))
        self.index = self.list_images.index(image)
        self.rect = self.image.get_rect().move(
            pos[0], pos[1])
        self.image_text = image

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def get_event(self, event, n=0):
        global army
        self.list_images = os.listdir('image/orders')
        n_astr = 0
        n_power = 0
        for i in all_sprites:
            if i.fraction == MY_ARMY:
                if '_a' in i.order:
                    n_astr += 1
                if i.order == 'orders/power.png':
                    n_power += 1
                if 'hike_0.png' in i.order and 'hike_0.png' in self.list_images:
                    del self.list_images[self.list_images.index('hike_0.png')]
                if 'hike_m1.png' in i.order and 'hike_m1.png' in self.list_images:
                    del self.list_images[self.list_images.index('hike_m1.png')]
                if 'help_sea.png' in i.order and 'help_sea.png' in self.list_images:
                    del self.list_images[self.list_images.index('help_sea.png')]
                if 'hike_sea.png' in i.order and 'hike_sea.png' in self.list_images:
                    del self.list_images[self.list_images.index('hike_sea.png')]
        if n_astr >= astra_fraction_dict[MY_ARMY]:
            for i in self.list_images:
                if '_a' in i:
                    del self.list_images[self.list_images.index(i)]
        if n_power > 1:
            for i in self.list_images:
                if 'power' in i:
                    del self.list_images[self.list_images.index(i)]
        if ALL_TERRITORIES[army.territory] not in SEAS:
            for i in self.list_images:
                if '_sea' in i:
                    del self.list_images[self.list_images.index(i)]
        elif ALL_TERRITORIES[army.territory] in SEAS and ALL_TERRITORIES[army.territory] < 14:
            lst = []
            for i in self.list_images:
                if i not in ['power.png', 'power_a.png']:
                    lst.append(i)
            self.list_images = lst
        if n == 1:
            self.index += 1
            if self.index == len(self.list_images):
                self.index = 0
        elif n == -1:
            self.index -= 1
            if self.index == -1:
                self.index = len(self.list_images) - 1
        for spr in all_sprites:
            if army.detachment == spr.detachment and army.fraction == spr.fraction:
                if self.index > len(self.list_images) - 1:
                    self.index = len(self.list_images) - 1
                spr.order_sprite.image = load_image(f'orders/{self.list_images[self.index]}',
                                                    color_key=(0, 0, 0))
                spr.order_sprite.image_txt = self.list_images[self.index]
                army = spr
                army.order_sprite.image_text = self.list_images[self.index]


def move_event(self, territory, lst=[]):
    global move_flag
    x_1 = self.rect[0]
    y_1 = self.rect[1]
    for i in range(len(lst)):
        new = Army(f'{DICT[self.fraction]}.png', self.territory, lst[i])
        new.order = self.order
        x_2 = TERRITORY_DICT[ALL_TERRITORIES[territory[i]]][0]
        y_2 = TERRITORY_DICT[ALL_TERRITORIES[territory[i]]][1]
        k = (y_2 - y_1) / (x_2 - x_1)
        b = y_1 - k * x_1
        det_lst = self.detachment.split(',')
        for j in lst[i]:
            del det_lst[det_lst.index(j)]
        self.detachment = ','.join(det_lst)
        if new.rect[0] != x_2 and new.rect[1] != y_2:
            if x_1 < x_2:
                x_1 += 1
                y_1 = k * x_1 + b
            elif x_1 > x_2:
                x_1 -= 1
                y_1 = k * x_1 + b
            if x_1 == x_2:
                if y_1 > y_2:
                    y_1 -= 1
            new.rect = new.image.get_rect().move(x_1, y_1)
            all_sprites.draw(screen)
        else:
            move_flag = False
        if ALL_TERRITORIES[new.territory] not in SEAS and \
                ALL_TERRITORIES[self.territory] not in [16, 25, 51, 36, 31, 44, 26]:
            abandoned_orders.append((new.fraction, ALL_TERRITORIES[self.territory]))
            astra_dict[DICT[new.fraction]] -= 1
        new.territory = territory[i]
        pygame.display.flip()
    if territory[-1] != self.territory:
        x_1 = self.rect[0]
        y_1 = self.rect[1]
        x_2 = TERRITORY_DICT[ALL_TERRITORIES[territory[-1]]][0]
        y_2 = TERRITORY_DICT[ALL_TERRITORIES[territory[-1]]][1]
        k = (y_2 - y_1) / (x_2 - x_1)
        b = y_1 - k * x_1
        if self.rect[0] != x_2 and self.rect[1] != y_2:
            if x_1 < x_2:
                x_1 += 1
                y_1 = k * x_1 + b
            elif x_1 > x_2:
                x_1 -= 1
                y_1 = k * x_1 + b
            if x_1 == x_2:
                if y_1 > y_2:
                    y_1 -= 1
            self.rect = self.image.get_rect().move(x_1, y_1)
            for i in all_sprites:
                if m_army.territory == i.territory:
                    pass
            all_sprites.draw(screen)
        else:
            move_flag = False
        self.territory = territory[-1]


def victory_points(fract):
    n = 0
    for i in all_sprites:
        if i.fraction == fract and ALL_TERRITORIES[i.territory] in CASTLE_TERRITORIES:
            n += 1
    return n


def superiority_tokens():
    global iron_throne, valyrian_sword, messenger_crow
    for i in king_tokens:
        if i.place == 1:
            if i.scale == 'throne':
                iron_throne = i.fraction
            elif i.scale == 'sword':
                valyrian_sword = i.fraction
            elif i.scale == 'crow':
                messenger_crow = i.fraction


def show_composition(background, event):
    global army
    armies = {'Старк': 'white.png', 'Баратеон': 'yellow.png', 'Ланнистер': 'red.png', 'Гренджой': 'black.png',
              'Тирелл': 'green.png', 'Мартелл': 'orange.png', 'Аррен': 'blue.png'}
    if ALL_TERRITORIES[event.territory] in SEAS:
        text = 'Флот'
        font_color = (0, 0, 139)
    else:
        text = 'Армия'
        font_color = (50, 50, 50)
    dect = event.detachment.split(',')
    fract = event.fraction
    army = event
    font = pygame.font.Font(None, 24)
    background.blit(load_image(f'fon_army.png', color_key=(0, 0, 0)), (450, 350))
    background.blit(pygame.image.load(f'image/fractions/{armies[fract]}'), (890, 410))

    background.blit(font.render(f"{text}: {fract}", 1, font_color), (730, 420))
    background.blit(font.render(f"Местоположение:", 1, font_color), (530, 420))
    if army.fraction == 'Старк':
        background.blit(font.render(f"{army.territory}", 1, (159, 159, 159)), (530, 460))
    elif army.fraction == 'Гренджой':
        background.blit(font.render(f"{army.territory}", 1, (50, 50, 50)), (530, 460))
    elif army.fraction == 'Баратеон':
        background.blit(font.render(f"{army.territory}", 1, (204, 204, 0)), (530, 460))
    else:
        background.blit(font.render(f"{army.territory}", 1, pygame.Color(f'dark{DICT[army.fraction]}')), (530, 460))
    background.blit(font.render(f"Состав: ", 1, font_color), (760, 450))
    for i in range(len(dect)):
        if i > 4:
            background.blit(load_image(f'detachments/{dect[i]}.png'), (600 + 50 * (i - 5), 620))
        else:
            background.blit(load_image(f'detachments/{dect[i]}.png'), (600 + 50 * i, 500))
    if army.fraction == MY_ARMY or move_flag:
        background.blit(load_image(f'{army.order}', color_key=(0, 0, 0)), (920, 630))
    else:
        background.blit(load_image(f'shirt_orders/{DICT[army.fraction]}.png', color_key=(0, 0, 0)), (920, 630))


def creature_kings_token():
    lst_thrones = ['yellow.png', 'red.png', 'white.png', 'orange.png', 'black.png', 'green.png', 'blue.png']
    for i in range(len(lst_thrones)):
        Kings_token(lst_thrones[i], i + 1, 'throne')
    lst_swords = ['black.png', 'green.png', 'orange.png', 'blue.png', 'white.png', 'yellow.png', 'red.png']
    for i in range(len(lst_swords)):
        Kings_token(lst_swords[i], i + 1, 'sword')
    lst_crows = ['red.png', 'white.png', 'orange.png', 'green.png', 'blue.png', 'yellow.png', 'black.png']
    for i in range(len(lst_crows)):
        Kings_token(lst_crows[i], i + 1, 'crow')


def not_message():
    global message_flag
    message_flag = False


def show_tokens(background):
    global show_army, message_flag
    all_sprites.draw(screen)
    winning_tokens.draw(screen)
    king_tokens.draw(screen)
    time.draw(screen)
    wildling.draw(screen)
    garrisons_group.draw(screen)
    if show_army:
        show_composition(screen, army)
        for i in all_sprites:
            if army.detachment == i.detachment and army.fraction == i.fraction and i.fraction == MY_ARMY and not move_flag:
                i.order_sprite.draw(screen)
        if army.fraction == MY_ARMY and not move_flag:
            left.draw(screen)
            right.draw(screen)
        army_quit.listen(pygame.event.get())
        army_quit.draw()
    background.blit(load_image('cards/karta_1.png'), (1600, 40))
    background.blit(load_image('cards/karta_2.png'), (1600, 340))
    background.blit(load_image('cards/karta_3.png'), (1600, 640))
    button.listen(pygame.event.get())
    button.draw()
    button_time.listen(pygame.event.get())
    button_time.draw()
    button_barrel.listen(pygame.event.get())
    button_barrel.draw()
    background.blit(load_image('tokens/time_image.png', color_key=(0, 0, 0)), (1690, 970))
    font = pygame.font.Font("fonts/пр.ttf", 14)
    background.blit(font.render(f"297 З . Э", True, (220, 220, 220)), (1828, 1010))
    dictin = {}
    for key, value in fraction_dict.items():
        dictin[value] = key
    lst = ['blue', 'black', 'green', 'orange', 'red', 'white', 'yellow']
    font = pygame.font.Font("fonts/пр.ttf", 30)
    for i in range(len(lst)):
        background.blit(load_image(f'tokens/{lst[i]}_pow.png', color_key=(0, 0, 0)), (1825, 45 + i * 80))
        background.blit(font.render(f"{astra_dict[lst[i]]}", True, (220, 220, 220)), (1880, 50 + i * 80))
    background.blit(pygame.font.Font("fonts/пр.ttf", 10).render("Дома", True, (220, 220, 220)), (1850, 955))
    background.blit(pygame.font.Font("fonts/пр.ttf", 8).render("Снабжение", True, (220, 220, 220)), (1840, 860))
    if window_barrel:
        create_barrel(background)
    if window_house:
        create_houses(background)
    if message_flag:
        show_army = False
        show_message(background)
    for i in king_tokens:
        if i.place == 1:
            if i.scale == 'throne':
                throne_army = i.fraction
            if i.scale == 'sword':
                sword_army = i.fraction
            if i.scale == 'crow':
                crow_army = i.fraction
    if MY_ARMY == crow_army:
        background.blit(load_image('crow.png', color_key=(0, 0, 0)), (1610, 910))
    elif MY_ARMY == throne_army:
        background.blit(load_image('throne.png', color_key=(0, 0, 0)), (1610, 910))
    elif MY_ARMY == sword_army:
        background.blit(load_image('sword.png', color_key=(0, 0, 0)), (1610, 910))
    if abandoned_orders:
        for i in abandoned_orders:
            background.blit(load_image(f'tokens/{DICT[i[0]]}_pow.png', color_key=(0, 0, 0)), TERRITORY_DICT[i[1]])


def window_b(n):
    global window_barrel, window_house
    if n == 'b':
        window_barrel = not window_barrel
        window_house = False
    else:
        window_house = not window_house
        window_barrel = False


def blit_pil_image(screen, img, position, r='RGBA'):
    if r == 'RGBA':
        pygame_image = pygame.image.fromstring(img.tobytes(), img.size, "RGBA")
    else:
        pygame_image = pygame.image.fromstring(img.tobytes(), img.size, "RGB")
    screen.blit(pygame_image, position)


def create_barrel(background):
    screen.fill((30, 30, 38), pygame.Rect(500, 300, 850, 650))
    list_barrels = os.listdir('image/barrels')
    for i in range(len(list_barrels)):
        background.blit(load_image(f'barrels/{list_barrels[i]}', color_key=(0, 0, 0)), (580 + i * 100, 320))
        n_barrel = supply_tokens(dictionary[list_barrels[i].split('_')[0]])
        background.blit(pygame.font.Font("fonts/пр.ttf", 24).render(f"{str(n_barrel)}", True, (220, 220, 220)),
                        (645 + i * 100, 330))
        list_barrels[i] = list_barrels[i].split('_')[0]
        screen.fill(dict_colors[list_barrels[i].split('_')[0]], pygame.Rect(500, 400 + i * 70, 850, 35))
        background.blit(pygame.font.Font("fonts/пр.ttf", 14).render(f"{dictionary[list_barrels[i].split('_')[0]]}",
                                                                    True, (220, 220, 220)), (520, 410 + i * 70))
        font = pygame.font.Font(None, 32)
        for j in range(len(army_supply(n_barrel))):
            background.blit(load_image(f'flag.png'), (700 + j * 60, 400 + i * 70))
            background.blit(font.render(f"{str(army_supply(n_barrel)[j])}", True, (255, 255, 255)),
                            (710 + j * 60, 410 + i * 70))
    barrel_quit.listen(pygame.event.get())
    barrel_quit.draw()


def create_houses(screen):
    screen.fill((30, 30, 36), pygame.Rect(400, 50, 980, 950))
    lst = sorted(list(astra_dict.keys()))
    for i in range(len(lst)):
        screen.fill(dict_colors[lst[i]], pygame.Rect(400, 60 + i * 130, 980, 35))
        heroes = os.listdir(f'image/cards/{lst[i]}')
        for j in heroes:
            if 'bg' in j:
                del heroes[heroes.index(j)]
        screen.blit(pygame.font.Font("fonts/пр.ttf", 16).render(f"{dictionary[lst[i]]}",
                                                                True, (220, 220, 220)), (430, 70 + i * 130))
        for j in range(len(heroes)):
            img = Image.open(f'image/cards/{lst[i]}/{heroes[j]}')
            img = img.crop((0, 70, 193, 200))
            img.thumbnail((140, 102))
            if lst[i] == 'blue':
                blit_pil_image(screen, img, (400 + j * 140, 95 + i * 130), 'RGB')
            else:
                blit_pil_image(screen, img, (400 + j * 140, 95 + i * 130), 'RGBA')
            screen.blit(pygame.font.Font(None, 16).render(f"{HEROES_DICT[heroes[j].split('_')[0]]}",
                                                          True, (255, 255, 255)), (410 + j * 140, 170 + i * 130))


def long_game():
    Army('white.png', 'Винтерфелл', ['knights', 'heavy_swordsmen', 'direwolves', 'spearmen'])
    Army('white.png', 'Белая гавань', ['swordsmen', 'hunters'])
    Army('white.png', 'Дрожащее море', ['galley', 'galley'])
    Army('yellow.png', 'Драконий камень', ['knights', 'heavy_swordsmen', 'crossbowmen', 'spearmen'])
    Army('yellow.png', 'Королевский лес', ['swordsmen', 'swordsmen'])
    Army('yellow.png', 'Губительные валы', ['great_ship', 'galley', 'galley', 'akat'])
    Army('red.png', 'Ланниспорт', ['reiksguard', 'knights', 'swordsmen', 'spearmen'])
    Army('red.png', 'Каменная септа', ['heavy_swordsmen', 'crossbowmen'])
    Army('red.png', 'Порт Ланниспорта', ['great_ship', 'galley'])
    Army('red.png', 'Золотой пролив', ['galley', 'galley'])
    Army('blue.png', 'Орлиное гнездо', ['reiksguard', 'knights', 'knights', 'knights'])
    Army('blue.png', 'Долина Аррен', ['knights', 'swordsmen'])
    Army('blue.png', 'Порт Орлиного гнезда', ['galley', 'akat'])
    Army('black.png', 'Пайк', ['robbers_berserkers', 'knights', 'robbers', 'robbers', 'robbers_dart', 'spearmen'])
    Army('black.png', 'Порт Пайка', ['great_ship', 'akat'])
    Army('black.png', 'Залив Железных Людей', ['galley', 'akat'])
    Army('black.png', 'Сероводье', ['robbers', 'robbers_dart'])
    Army('green.png', 'Пролив Редвин', ['galley', 'great_ship'])
    Army('green.png', 'Хайгарден', ['reiksguard', 'knights', 'swordsmen', 'spearmen_shield'])
    Army('green.png', 'Дорнские марки', ['heavy_swordsmen', 'archers'])
    Army('orange.png', 'Солнечное копьё', ['knights_dorn', 'knights_dorn', 'heavy_swordsmen', 'spearmen'])
    Army('orange.png', 'Солёный берег', ['swordsmen', 'archers_dorn'])
    Army('orange.png', 'Дорнийское море', ['galley', 'akat'])
    Win_token('blue_win.png', victory_points('Аррен'))
    Win_token('red_win.png', victory_points('Ланнистер'))
    Win_token('white_win.png', victory_points('Старк'))
    Win_token('black_win.png', victory_points('Гренджой'))
    Win_token('green_win.png', victory_points('Тирелл'))
    Win_token('yellow_win.png', victory_points('Баратеон'))
    Win_token('orange_win.png', victory_points('Мартелл'))


def show_message(screen):
    screen.blit(load_image('fon_notice.png', color_key=(0, 0, 0)), (500, 400))
    font = pygame.font.Font("fonts/пр.ttf", 18)
    screen.blit(font.render('Вы не отдали приказы', True, (50, 50, 50)), (660, 540))
    screen.blit(font.render('всем своим армиям.', True, (50, 50, 50)), (670, 560))
    message_quit.listen(pygame.event.get())
    message_quit.draw()


def new_game():
    global astra_fraction_dict
    creature_kings_token()
    superiority_tokens()
    for i in king_tokens:
        if i.scale == 'crow' and i.fraction not in astra_fraction_dict.keys():
            n_astra = i.astra
            astra_fraction_dict[i.fraction] = n_astra
    for i in ['white', 'blue', 'green', 'black', 'red', 'orange', 'yellow', 'kings_port']:
        Garrisons(i)
    if l_games:
        long_game()


def supply_tokens(fract):
    n = 0
    for i in all_sprites:
        if i.fraction == fract:
            if ALL_TERRITORIES[i.territory] in BARREL_TERRITORIES:
                n += BARREL_TERRITORIES[ALL_TERRITORIES[i.territory]]
    return n


def army_supply(n_barrels):
    lst = [6, 6]
    for i in range(n_barrels):
        if i % 2 == 1:
            lst.append(6)
        else:
            if lst.count(lst[0]) == 2:
                for j in lst:
                    if j < 10:
                        lst[lst.index(j)] += 2
                        break
            else:
                lst[1] += 2
    return lst


def artificial_intelligence(fraction):
    if time.value == 1:
        if fraction in ['Ланнистер', 'red']:
            for i in all_sprites:
                if i.fraction == 'Ланнистер':
                    if ALL_TERRITORIES[i.territory] == 4:
                        i.order = 'protection_a.png'
                    elif ALL_TERRITORIES[i.territory] == 58:
                        i.order = 'power.png'
                    elif ALL_TERRITORIES[i.territory] == 31:
                        i.order = 'hike_a.png'
                    elif ALL_TERRITORIES[i.territory] == 32:
                        i.order = 'power.png'
                if 'orders' not in i.order:
                    i.order = 'orders/' + i.order
        elif fraction in ['Гренджой', 'black']:
            for i in all_sprites:
                if i.fraction == 'Гренджой':
                    if ALL_TERRITORIES[i.territory] == 26:
                        i.order = 'hike_0.png'
                    elif ALL_TERRITORIES[i.territory] == 28:
                        i.order = 'power.png'
                    elif ALL_TERRITORIES[i.territory] == 55:
                        i.order = 'power.png'
                    elif ALL_TERRITORIES[i.territory] == 3:
                        i.order = 'help.png'
                if 'orders' not in i.order:
                    i.order = 'orders/' + i.order
        elif fraction in ['Старк', 'white']:
            for i in all_sprites:
                if i.fraction == 'Старк':
                    if ALL_TERRITORIES[i.territory] == 16:
                        i.order = 'power_a.png'
                    elif ALL_TERRITORIES[i.territory] == 13:
                        i.order = 'hike_a.png'
                    elif ALL_TERRITORIES[i.territory] == 18:
                        i.order = 'hike_0.png'
                if 'orders' not in i.order:
                    i.order = 'orders/' + i.order
        elif fraction in ['Аррен', 'blue']:
            for i in all_sprites:
                if i.fraction == 'Аррен':
                    if ALL_TERRITORIES[i.territory] == 25:
                        i.order = 'hike_m1.png'
                    elif ALL_TERRITORIES[i.territory] == 24:
                        i.order = 'power.png'
                    elif ALL_TERRITORIES[i.territory] == 56:
                        i.order = 'hike_0.png'
                if 'orders' not in i.order:
                    i.order = 'orders/' + i.order
        elif fraction in ['Баратеон', 'yellow']:
            for i in all_sprites:
                if i.fraction == 'Баратеон':
                    if ALL_TERRITORIES[i.territory] == 51:
                        i.order = 'hike_0.png'
                    elif ALL_TERRITORIES[i.territory] == 9:
                        i.order = 'hike_m1.png'
                    elif ALL_TERRITORIES[i.territory] == 48:
                        i.order = 'power.png'
                if 'orders' not in i.order:
                    i.order = 'orders/' + i.order
        elif fraction in ['Тирелл', 'green']:
            for i in all_sprites:
                if i.fraction == 'Тирелл':
                    if ALL_TERRITORIES[i.territory] == 36:
                        i.order = 'hike_0.png'
                    elif ALL_TERRITORIES[i.territory] == 6:
                        i.order = 'hike_m1.png'
                    elif ALL_TERRITORIES[i.territory] == 38:
                        i.order = 'power_a.png'
                if 'orders' not in i.order:
                    i.order = 'orders/' + i.order
        elif fraction in ['Мартелл', 'orange']:
            for i in all_sprites:
                if i.fraction == 'Мартелл':
                    if ALL_TERRITORIES[i.territory] == 44:
                        i.order = 'hike_0.png'
                    elif ALL_TERRITORIES[i.territory] == 43:
                        i.order = 'power_a.png'
                    elif ALL_TERRITORIES[i.territory] == 8:
                        i.order = 'hike_a.png'
                if 'orders' not in i.order:
                    i.order = 'orders/' + i.order


def power(territory):
    for i in all_sprites:
        if i.territory == territory:
            if i.order == 'orders/power.png':
                if ALL_TERRITORIES[i.territory] in ASTRA_TERRITORIES:
                    astra_dict[DICT[i.fraction]] += ASTRA_TERRITORIES[ALL_TERRITORIES[i.territory]]
                astra_dict[DICT[i.fraction]] += 1
            elif i.order == 'orders/power_a.png':
                if ALL_TERRITORIES[i.territory] not in CASTLE_TERRITORIES:
                    if ALL_TERRITORIES[i.territory] in ASTRA_TERRITORIES:
                        astra_dict[DICT[i.fraction]] += ASTRA_TERRITORIES[ALL_TERRITORIES[i.territory]]
                    astra_dict[DICT[i.fraction]] += 1
                else:
                    if ALL_TERRITORIES[i.territory] == 16:
                        n = Army(f'{DICT[i.fraction]}.png', 'Ледовый залив', ['galley', 'galley', 'great_ship'])
                        n.order = i.order


def hike(territory):
    global m_army, m_ter, m_lst
    if time.value == 1:
        for i in all_sprites:
            if i.fraction != MY_ARMY:
                if i.territory == territory and territory == 'Белая гавань':
                    i.movement(['Ров Кейлин'])
                if i.territory == territory and territory == 'Дрожащее море':
                    move_flag = True
                    i.movement(['Узское море'])
                if i.territory == territory and territory == 'Дорнийское море':
                    move_flag = True
                    i.movement(['Восточное летнее море'])
                if i.territory == territory and territory == 'Пролив Редвин':
                    move_flag = True
                    i.movement(['Западное летнее море'])
                if i.territory == territory and territory == 'Хайгарден':
                    move_flag = True
                    i.movement(['Старомест', 'Простор'], [['swordsmen']])
                if i.territory == territory and territory == 'Орлиное гнездо':
                    move_flag = True
                    i.movement(['Персты', 'Лунные горы'], [['knights']])
                if i.territory == territory and territory == 'Драконий камень':
                    move_flag = True
                    i.movement(['Клешня'])
                if i.territory == territory and territory == 'Солнечное копьё':
                    move_flag = True
                    i.movement(['Звездопад', 'Айронвуд'], [['knights_dorn', 'heavy_swordsmen']])
                if i.territory == territory and territory == 'Пайк':
                    move_flag = True
                    i.movement(['Кремень', 'Сигард'], [['robbers', 'robbers']])
                if i.territory == territory and territory == 'Ланниспорт':
                    move_flag = True
                    i.movement(['Риверран', 'Ланниспорт'], [['reiksguard', 'knights', 'spearmen']])


def execution_move():
    move_dict = {}
    for i in king_tokens:
        if i.scale == 'throne':
            move_dict[i.place] = i.fraction
    move_lst = []
    lst = list(move_dict.keys())
    for i in sorted(lst):
        move_lst.append(move_dict[i])
    lst_plaque = []
    lst_hike = []
    lst_power = []
    for i in move_lst:
        for j in all_sprites:
            if j.fraction == i:
                if j.order.split('/')[1] in ['plaque.png', 'plaque_a.png']:
                    lst_plaque.append(j.territory)
                elif j.order.split('/')[1] in ['hike_m1.png', 'hike_a.png', 'hike_0.png']:
                    lst_hike.append(j.territory)
                elif j.order.split('/')[1] in ['power.png', 'power_a.png']:
                    lst_power.append(j.territory)
    if lst_plaque:
        for i in lst_plaque:
            pass
    if lst_hike:
        for i in lst_hike:
            hike(i)
    if lst_power:
        for i in lst_power:
            power(i)


def move():
    global message_flag, move_flag
    flag = False
    for i in all_sprites:
        if i.fraction == MY_ARMY:
            if 'shirt' in i.order:
                flag = True
    if flag:
        message_flag = True
    else:
        move_flag = True
        dictionary = list(fraction_dict.values())
        del dictionary[dictionary.index(MY_ARMY)]
        for i in dictionary:
            artificial_intelligence(i)
        execution_move()


left = Small_things(['arrow_l.png'])
right = Small_things(['arrow_r.png'])
time = Small_things(['time_token.png', 1])
wildling = Small_things(['wildling_token.png', 2])


def main():
    global show_army, army, MY_ARMY
    running = True
    image = pygame.image.load('image/fulls.png')
    cursor_sprite = pygame.sprite.Group()
    cursor_image = load_image('cursor2.png')
    cursor_image.set_colorkey((0, 0, 0))
    cursor = pygame.sprite.Sprite(cursor_sprite)
    cursor.image = cursor_image
    cursor.rect = cursor.image.get_rect()
    pygame.mouse.set_visible(False)
    MY_ARMY = start_screen()
    new_game()
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEMOTION:
                cursor.rect.topleft = event.pos
            if event.type == pygame.MOUSEBUTTONDOWN:
                flag = False
                if left.rect.collidepoint(event.pos) and show_army:
                    for i in all_sprites:
                        if army.detachment == i.detachment and army.fraction == i.fraction:
                            i.order_sprite.get_event(event, 1)
                            army = i
                if right.rect.collidepoint(event.pos) and show_army:
                    for i in all_sprites:
                        if army.detachment == i.detachment and army.fraction == i.fraction:
                            i.order_sprite.get_event(event, -1)
                            army = i
                for spr in all_sprites:
                    f = spr.get_event(event)
                    if f:
                        flag = True
                if show_army:
                    for i in all_sprites:
                        if army.detachment == i.detachment and army.fraction == i.fraction:
                            i.order_sprite.get_event(event)
                            i.order_sprite.draw(screen)
                            army = i
                if 500 < event.pos[0] < 1050 and 350 < event.pos[1] < 700:
                    flag = True
                if not flag:
                    show_army = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT and show_army and army.fraction == MY_ARMY:
                    army.order_sprite.get_event(event, 1)
                elif event.key == pygame.K_LEFT and show_army and army.fraction == MY_ARMY:
                    army.order_sprite.get_event(event, -1)
                if event.key == pygame.K_RETURN and show_army and army.fraction == MY_ARMY:
                    for i in all_sprites:
                        if army.detachment == i.detachment and army.fraction == i.fraction:
                            i.order = f'orders/{i.order_sprite.image_text}'
                            army = i
            screen.fill((47, 79, 79))

            screen.blit(image, (0, 0, 1500, 998))
            if pygame.mouse.get_focused():
                all_sprites.draw(screen)
            show_tokens(screen)
            cursor_sprite.draw(screen)
            pygame.display.flip()
            clock.tick(FPS)
    connect.close()
    pygame.quit()


if __name__ == '__main__':
    main()


def sea_territories(start, end):
    dictin = {}
    start_ship, end_ship = False, False
    for i in all_sprites:
        if i.fraction == MY_ARMY and ALL_TERRITORIES[i.territory] < 14:
            if ALL_TERRITORIES[i.territory] in NEIGHBORING_TERRITORIES[start]:
                start_ship = True
            if ALL_TERRITORIES[i.territory] in NEIGHBORING_TERRITORIES[end]:
                end_ship = True
    if not start_ship or not end_ship:
        return 'Ошибочка'
    for key, value in TERRITORY_DICT.items():
        dictin[value] = key
    for k in NEIGHBORING_TERRITORIES[start]:
        if k > 13:
            break
        if k in NEIGHBORING_TERRITORIES[end]:
            return 'Поплыли через одно море'
        for j in NEIGHBORING_TERRITORIES[k]:
            if j > 13:
                break
            if j in NEIGHBORING_TERRITORIES[end]:
                return 'Поплыли через два моря'
            for g in NEIGHBORING_TERRITORIES[j]:
                if g > 13:
                    break
                if g in NEIGHBORING_TERRITORIES[end]:
                    return 'Поплыли через три моря'
    # for i in all_sprites:
    #    print(ALL_TERRITORIES[i.territory], NEIGHBORING_TERRITORIES[start])
    #    if i.fraction == MY_ARMY and ALL_TERRITORIES[i.territory] < 14:  # and ALL_TERRITORIES[i.territory] == end#
    #        if ALL_TERRITORIES[i.territory] in NEIGHBORING_TERRITORIES[start]:
    #            return
    #        for j in NEIGHBORING_TERRITORIES[ALL_TERRITORIES[i.territory]]:
    #            print(ALL_TERRITORIES[i.territory], NEIGHBORING_TERRITORIES[j])
    #            if ALL_TERRITORIES[i.territory] in NEIGHBORING_TERRITORIES[j]:
    #                return 'Поплыли через два море'
    #        # if end in NEIGHBORING_TERRITORIES[ALL_TERRITORIES[dictin[i.rect]]]:


def definition(start, end):
    f_1, f_2 = False, False
    if ALL_TERRITORIES[start] in SEAS and ALL_TERRITORIES[end] in SEAS:
        if ALL_TERRITORIES[end] in NEIGHBORING_TERRITORIES[ALL_TERRITORIES[start]]:
            return [TERRITORY_DICT[ALL_TERRITORIES[start]], TERRITORY_DICT[ALL_TERRITORIES[start]]]
        else:
            return 'Не поплывём'
    if ALL_TERRITORIES[start] in SEAS or ALL_TERRITORIES[end] in SEAS:
        return 'Ошибочка'
    if ALL_TERRITORIES[end] in NEIGHBORING_TERRITORIES[ALL_TERRITORIES[start]]:
        return [TERRITORY_DICT[ALL_TERRITORIES[start]], TERRITORY_DICT[ALL_TERRITORIES[start]]]
    else:
        for i in NEIGHBORING_TERRITORIES[ALL_TERRITORIES[start]]:
            if i in SEAS:
                f_1 = True
        for i in NEIGHBORING_TERRITORIES[ALL_TERRITORIES[end]]:
            if i in SEAS:
                f_2 = True
        if f_1 and f_2:
            return sea_territories(ALL_TERRITORIES[start], ALL_TERRITORIES[end])
        else:
            return 'Ошибочка'

# print(definition('Ледовый залив', 'Винтерфелл'))
