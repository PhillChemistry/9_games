''' tests why there's an issue with blitting'''
import pygame

background = pygame.Surface((100, 100))
background.fill('blue')
symbol = pygame.Surface((10, 10))
symbol.fill('red')
screen = pygame.display.set_mode(size=(100, 100))

pygame.init()
running = True
while running:
    current_img = screen.blit(background, (0,0, 100, 100))
    print(current_img)