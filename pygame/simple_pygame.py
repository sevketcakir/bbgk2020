import pygame

pygame.init()

screen = pygame.display.set_mode((640,480))
color = [(0,0,0), (255,255,255)]
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            color[1], color[0] = color[0], color[1]

    screen.fill(color[0])
    pygame.draw.circle(screen, color[1],(320,240), 50)
    pygame.display.flip()
