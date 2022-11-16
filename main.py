import sys, pygame
from game import Game

# Initialize
pygame.init()

# Pygame
pygame.display.set_caption("Game")
screen = pygame.display.set_mode((800, 600))
screen.fill((255, 255, 255))
pygame.display.flip()

clock = pygame.time.Clock()

game = Game(screen)
game.load_level("template")
game.redraw()

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
                game.on_mousedown(event)
        elif event.type == pygame.MOUSEBUTTONUP:
            mouse_pressed = False
            position = pygame.mouse.get_pos()
            game.on_mouseup(event)
        elif event.type == pygame.MOUSEMOTION:
            if mouse_pressed:
                position = pygame.mouse.get_pos()
                game.on_mousemove(event)
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_z:
                print("Zoom out")
            elif event.key == pygame.K_i:
                print("Zoom in")

    clock.tick_busy_loop()