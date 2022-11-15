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

    #check if obj is on grid?
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if pygame.display.get_active():
                mouse_pressed = True
                position = pygame.mouse.get_pos()
                game.on_mousedown(position)
            if event.button == 1:
                print("drag connected pieces")
            elif event.button == 3:
                print("drag single piece")
        elif event.type == pygame.MOUSEBUTTONUP:
            mouse_pressed = False
            position = pygame.mouse.get_pos()
            game.on_mouseup(position)
        elif event.type == pygame.MOUSEMOTION:
            if mouse_pressed:
                position = pygame.mouse.get_pos()
                game.on_mousemove(position)
                if event.rel[0] > 0:
                    print("Drag object to the right")
                elif event.rel[1] > 0:
                    print("Drag object down")
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_z:
                print("Zoom out")
            elif event.key == pygame.K_i:
                print("Zoom in")

    clock.tick_busy_loop()