import sys, pygame
from game import *

# Initialize
pygame.init()

# Main
screen = pygame.display.set_mode((800, 600))
screen.fill((255, 255, 255))
pygame.display.flip()

clock = pygame.time.Clock()

mouse_pressed = False

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

                # Handle mousedown
        elif event.type == pygame.MOUSEBUTTONUP:
            mouse_pressed = False

            # Handle mouseup
        elif event.type == pygame.MOUSEMOTION:
            # Handle mouse movements
            pass

    clock.tick_busy_loop()