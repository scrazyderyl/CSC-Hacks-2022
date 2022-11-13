import sys, pygame
from game import *

# Initialize
pygame.init()

# Pygame
screen = pygame.display.set_mode((800, 600))
screen.fill((255, 255, 255))
pygame.display.flip()

clock = pygame.time.Clock()

mouse_pressed = False

game = Game()

# Loop
while True:
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if pygame.display.get_active():
                mouse_pressed = True
                position = pygame.mouse.get_pos()
                game.on_mousedown(position)
        elif event.type == pygame.MOUSEBUTTONUP:
            mouse_pressed = False
            position = pygame.mouse.get_pos()
            game.on_mouseup(position)
        elif event.type == pygame.MOUSEMOTION:
            if mouse_pressed:
                position = pygame.mouse.get_pos()
                game.on_mousemove(position)

    clock.tick_busy_loop()