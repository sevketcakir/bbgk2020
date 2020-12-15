import pygame
from pygame.locals import *
pygame.init()

screen = pygame.display.set_mode((640,480))
color = [0,0,0]
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN and event.key == K_SPACE:
            color = [0,0,0]

    keys = pygame.key.get_pressed()
    if keys[K_UP]:
        color = [(rgb+1)%256 for rgb in color]

    screen.fill(color)
    pygame.display.flip()
