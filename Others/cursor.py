import pygame
from pygame_widgets import Button

pygame.init()
win = pygame.display.set_mode((200, 200))


def button_pressed():
    print('Изо')


button = Button(
    win, 100, 100, 81,
    81,
    image=pygame.image.load('image/tokens/time_button.png'), inactiveColour=(0, 0, 0),
    onRelease=lambda: print('li'))

run = True
while run:
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            pygame.quit()
            run = False
            quit()

    win.fill((255, 255, 255))

    button.listen(events)
    button.draw()

    pygame.display.update()
