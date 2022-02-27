from cgi import print_environ_usage
import pygame
import os
from pygame.locals import (
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_RCTRL,
    K_LCTRL,
    K_a,
    K_s,
    K_d,
    K_w,
)

# Initialize
pygame.init()

# Setup window
FPS = 60
WIDTH, HEIGHT = 900, 500
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
BACKGROUND = pygame.transform.scale(pygame.image.load(os.path.join("Assets","space.png")), (WIDTH, HEIGHT))

# Color variables
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

# Objects
class SpaceShip():
    def __init__(self, color, position, image, health=10, bullets=3, vel=5, shipSize=(60,50)):        
        self.shipSize = shipSize   
        self.headDirection = (True if 0 < position[2] < 180 else False)                
        self.health = health
        self.position = list(position[:2])
        self.color = color
        self.spaceShip = self.build_spaceShip(image, position)        
        self.maxBullets = bullets
        self.velocity = vel
        self.VisualUpdate = (self.spaceShip, self.position)                          
    
    def build_spaceShip(self, imageName, position):
        SPACESHIP_IMAGE = pygame.transform.rotate(pygame.transform.scale(pygame.image.load(os.path.join("Assets", imageName)), self.shipSize), position[2])
        self.spaceShipBox = SPACESHIP_IMAGE.get_rect()        
        return SPACESHIP_IMAGE                    

    def control(self, key_pressed):
        if self.headDirection:
            # if 0 < self.position[0] < WIDTH - self.shipSize[0]:                
            if key_pressed[K_a] and self.position[0] - self.velocity > 10:
                self.position[0] -= self.velocity
            if key_pressed[K_d] and self.position[0] + self.velocity < WIDTH - self.shipSize[0]:
                self.position[0] += self.velocity
            # if 0 < self.position[1] < HEIGHT - self.shipSize[1]:
            if key_pressed[K_s] and self.position[1] + self.velocity < HEIGHT - self.shipSize[1] + 10:
                self.position[1] += self.velocity
            if key_pressed[K_w] and self.position[1] - self.velocity > 10:                
                self.position[1] -= self.velocity
        else:
            # if 0 < self.position[0] < WIDTH - self.shipSize[0]:
            if key_pressed[K_LEFT] and self.position[0] - self.velocity > 10:
                self.position[0] -= self.velocity
            if key_pressed[K_RIGHT] and self.position[0] + self.velocity < WIDTH - self.shipSize[0]:
                self.position[0] += self.velocity
            # if 0 < self.position[1] < HEIGHT - self.shipSize[1]:
            if key_pressed[K_DOWN] and self.position[1] + self.velocity < HEIGHT - self.shipSize[1] + 10:
                self.position[1] += self.velocity
            if key_pressed[K_UP] and self.position[1] - self.velocity > 10:
                self.position[1] -= self.velocity
        
# Functions
def draw_objects(list_VisUpdate=None):    
    WINDOW.blit(BACKGROUND, (0, 0))
    if list_VisUpdate != None:
        WINDOW.blits(list_VisUpdate)
    pygame.display.update()

def draw_effects():
    pygame.display.update()

# Main loop
def main():
    # Setup new game
    clock = pygame.time.Clock()
    run = True    
    RedSpaceShip = SpaceShip(RED, (100, 250, 90), "spaceship_red.png")  # (100, 250, 90) => x = 100, y = 250, rotation angle = 90 degree
    YellowSpaceShip = SpaceShip(YELLOW, (700, 250, 270), "spaceship_yellow.png")    
    VisualUpdates = (RedSpaceShip.VisualUpdate, YellowSpaceShip.VisualUpdate)

    # Run game
    while run:
        clock.tick(FPS)                
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                        
        keypressed = pygame.key.get_pressed()
        RedSpaceShip.control(keypressed)
        YellowSpaceShip.control(keypressed)
        draw_objects(VisualUpdates)


if __name__ == "__main__":
    main()    
          