import pygame
import os
from pygame.locals import (
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_KP_0,
    K_f,
    K_a,
    K_s,
    K_d,
    K_w,
)

# Initialize
pygame.init()
pygame.font.init()

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

# Font variables
HP_FONT = pygame.font.SysFont("comicsans", 40)
INFO_FONT = pygame.font.SysFont("comicsans", 80)
WARN_FONT = pygame.font.SysFont("comicsans", 100)
WINNER_FONT = pygame.font.SysFont("comicsans", 100)

# Objects
class SpaceShip():
    def __init__(self, color, position, image, health=10, bullets=5, vel=5, shipSize=(60,50)):        
        self.shipSize = shipSize   
        self.headDirection = (True if 0 < position[2] < 180 else False)                
        self.health = health
        self.position = list(position[:2])
        self.color = color
        self.spaceShip = self.build_spaceShip(image, position)        
        self.maxBullets = bullets
        self.bullets = []
        self.velocity = vel
        self.VisualUpdate = (self.spaceShip, self.position)
        self.OpponentBulletVel = self.velocity*2
                
    
    def build_spaceShip(self, imageName, position):
        SPACESHIP_IMAGE = pygame.transform.rotate(pygame.transform.scale(pygame.image.load(os.path.join("Assets", imageName)), self.shipSize), position[2])                
        return SPACESHIP_IMAGE                   

    def shooting(self):
        BULLET = pygame.Rect(
            self.position[0] + self.shipSize[0], self.position[1] + self.shipSize[1]//2, 10, 5
        )        
        if len(self.bullets) < self.maxBullets:
            self.bullets.append(BULLET)                                    

    def got_hit(self, opponent_bullets):
        for bullet in opponent_bullets:
            if self.headDirection:
                bullet.x -= self.OpponentBulletVel
                if self.spaceShipBox.colliderect(bullet):
                    self.health -= 1
                    opponent_bullets.remove(bullet)
                elif bullet.x < 0:            
                    opponent_bullets.remove(bullet)
            else:
                bullet.x += self.OpponentBulletVel
                if self.spaceShipBox.colliderect(bullet):
                    self.health -= 1
                    opponent_bullets.remove(bullet)
                elif bullet.x > WIDTH:            
                    opponent_bullets.remove(bullet)                

    def control(self, key_pressed):
        if self.headDirection:             
            if key_pressed[K_a] and self.position[0] - self.velocity > 10:
                self.position[0] -= self.velocity                
            if key_pressed[K_d] and self.position[0] + self.velocity < WIDTH - self.shipSize[0] + 5:
                self.position[0] += self.velocity            
            if key_pressed[K_s] and self.position[1] + self.velocity < HEIGHT - self.shipSize[1] - 10:
                self.position[1] += self.velocity
            if key_pressed[K_w] and self.position[1] - self.velocity > 5:                
                self.position[1] -= self.velocity
            if key_pressed[K_f]:
                self.shooting
        else:        
            if key_pressed[K_LEFT] and self.position[0] - self.velocity > 10:
                self.position[0] -= self.velocity
            if key_pressed[K_RIGHT] and self.position[0] + self.velocity < WIDTH - self.shipSize[0] + 5:
                self.position[0] += self.velocity            
            if key_pressed[K_DOWN] and self.position[1] + self.velocity < HEIGHT - self.shipSize[1] - 10:
                self.position[1] += self.velocity
            if key_pressed[K_UP] and self.position[1] - self.velocity > 5:
                self.position[1] -= self.velocity
            if key_pressed[K_KP_0]:
                self.shooting
            
        self.spaceShipBox = pygame.Rect(tuple(self.position), self.shipSize)                
        
# Functions
def draw_objects(list_VisUpdate=None, list_InfoUpdate=None, list_EffectUpdate=None):    
    WINDOW.blit(BACKGROUND, (0, 0))
    if list_VisUpdate != None:        
        WINDOW.blits(list_VisUpdate)
    draw_info(list_InfoUpdate)
    draw_bullet(list_EffectUpdate[0], RED)
    draw_bullet(list_EffectUpdate[1], YELLOW)
    pygame.display.update()

def draw_info(list_InfoUpdate=None):    
    if list_InfoUpdate != None:
        HEALTH_INFO_1 = HP_FONT.render( f"HEALTH: {list_InfoUpdate[0]}", 1, WHITE )
        HEALTH_INFO_2 = HP_FONT.render( f"HEALTH: {list_InfoUpdate[1]}", 1, WHITE )        
        WINDOW.blit(HEALTH_INFO_1, (10, 10))
        WINDOW.blit(HEALTH_INFO_2, (WIDTH - HEALTH_INFO_2.get_width(), 10))

def draw_bullet(bullets, color):
    for bullet in bullets:
        pygame.draw.rect(WINDOW, color, bullet)

# Main loop
def main():
    # Setup new game
    clock = pygame.time.Clock()
    run = True    
    RedSpaceShip = SpaceShip(RED, (100, 250, 90), "spaceship_red.png", 8)  # (100, 250, 90) => x = 100, y = 250, rotation angle = 90 degree
    YellowSpaceShip = SpaceShip(YELLOW, (700, 250, 270), "spaceship_yellow.png")    
    VisualUpdates = (RedSpaceShip.VisualUpdate, YellowSpaceShip.VisualUpdate)    
    InfoUpdates = (RedSpaceShip.health, YellowSpaceShip.health)    
    EffectUpdates = (RedSpaceShip.bullets, YellowSpaceShip.bullets)

    # Run game
    while run:
        clock.tick(FPS)                
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()            

        RedSpaceShip.got_hit(YellowSpaceShip.bullets)
        YellowSpaceShip.got_hit(RedSpaceShip.bullets)

        keypressed = pygame.key.get_pressed()
        RedSpaceShip.control(keypressed)
        YellowSpaceShip.control(keypressed)
        
        draw_objects(VisualUpdates, InfoUpdates, EffectUpdates)        


if __name__ == "__main__":
    main()    
          