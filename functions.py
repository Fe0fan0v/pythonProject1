import pygame, time

pygame.init()
x, y = (200, 300)
pencere = pygame.display.set_mode((x, y))
pygame.display.set_caption("Click")

white = (255, 255, 255)
black = (0, 0, 0)
black2 = (30, 30, 30)


class Counter:
    count = 0

    def click(self):
        self.count += 1


number = Counter()


def text_objects(text, font, color):
    textSurface = font.render(text, True, color)
    return textSurface, textSurface.get_rect()


def button(msg, x, y, w, h, c, ic, action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    pygame.draw.rect(pencere, c, (x, y, w, h))

    smallText = pygame.font.Font("freesansbold.ttf", 20)
    textSurf, textRect = text_objects(msg, smallText, white)
    textRect.center = ((x + (w / 2)), (y + (h / 2)))
    pencere.blit(textSurf, textRect)

    if x + w > mouse[0] > x and y + h > mouse[1] > y:
        pygame.draw.rect(pencere, ic, (x, y, w, h))
        if click[0] == 1 != None:
            action()
        smallText = pygame.font.Font("freesansbold.ttf", 20)
        textSurf, textRect = text_objects(msg, smallText, white)
        textRect.center = ((x + (w / 2)), (y + (h / 2)))
        pencere.blit(textSurf, textRect)


def loop():
    cikis = False
    while not cikis:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                cikis = True
                pygame.quit()
                quit()
            pencere.fill(white)
            smallText = pygame.font.Font("freesansbold.ttf", 50)
            textSurf, textRect = text_objects(str(number.count), smallText, black)
            textRect.center = ((x / 2)), (30)
            pencere.blit(textSurf, textRect)
            button("Click", 0, 100, 200, 200, black, black2, number.click)
            pygame.display.update()


loop()
pygame.quit()
quit()
