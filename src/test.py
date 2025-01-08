import pygame
import sys 
import os 

pygame.init() 
if not pygame.get_init():
    print("failed init") 
    sys.exit()

screen = pygame.display.set_mode((500, 500)) 
if not pygame.display.get_init():
    print('Failed to init pygame display')
    sys.exit()

print(os.environ)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((0, 40, 100))

    pygame.display.flip() # updates display

pygame.quit()
sys.exit()