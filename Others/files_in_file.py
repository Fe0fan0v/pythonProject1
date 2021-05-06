import pygame
import pygame_gui

pygame.init()
pygame.display.toggle_fullscreen

pygame.display.set_caption('MainWind')
window_surface = pygame.display.set_mode((1920, 1080))
bg = pygame.image.load("image/fon.png")

background = pygame.Surface((1920, 1080))
manager = pygame_gui.UIManager((1920, 1080))
background.fill(pygame.Color('white'))

ng_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((460, 375), (1000, 50)),
                                         text='Новая игра', manager=manager)

cont_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((460, 435), (1000, 50)),
                                           text='Продолжить', manager=manager)

ex_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((460, 495), (1000, 50)),
                                         text='Выход', manager=manager)

clock = pygame.time.Clock()
is_running = True

while is_running:
    time_delta = clock.tick(60) / 1000.0
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            is_running = False

        if event.type == pygame.USEREVENT:
            if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == ex_button:
                    is_running = False

    manager.process_events(event)

    manager.update(time_delta)

    window_surface.blit(bg, (0, 0))
    manager.draw_ui(window_surface)

    pygame.display.update()
