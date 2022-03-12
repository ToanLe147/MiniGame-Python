import pygame
import os
from pygame.locals import *

# Initialize
pygame.init()
pygame.font.init()
pygame.mixer.init()

# Color variables
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

# Setup window
FPS = 60
WIDTH, HEIGHT = 1200, 700
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("VS Mode")
BACKGROUND = pygame.transform.scale(pygame.image.load(os.path.join("Assets","Setting_BG.jpg")), (WIDTH, HEIGHT)).convert()
BORDER = pygame.Rect(WIDTH//2 - 5, 0, 10, HEIGHT)

# Font variables
HP_FONT = pygame.font.SysFont("comicsans", 40)
INFO_FONT = pygame.font.SysFont("comicsans", 80)
WARN_FONT = pygame.font.SysFont("comicsans", 100)
WINNER_FONT = pygame.font.SysFont("comicsans", 100)

# Sound effects
FIRE_SOUND = pygame.mixer.Sound(os.path.join("Assets/Sounds","Gun+Silencer.mp3"))
EXPLOSION_SOUND = pygame.mixer.Sound(os.path.join("Assets/Sounds","Grenade+1.mp3"))

# Explosion effects
EXPLOSION_VISUAL = []
for i in range(1,6):
    img = pygame.image.load(os.path.join("Assets/Explosion",f"exp{i}.png"))
    img = pygame.transform.scale(img, (50,50))
    EXPLOSION_VISUAL.append(img)


# Objects
class SpaceShip():
    def __init__(self, name, color, position, image, health=10, bullets=3, bulletVel=10, vel=5, shipSize=(60,50)):
        self.name = name
        self.shipSize = shipSize   
        self.headDirection = (True if 0 < position[2] < 180 else False)                
        self.health = health
        self.position = list(position[:2])
        self.color = color
        self.spaceShip = self.build_spaceShip(image, position)
        self.spaceShipBox = self.spaceShip.get_bounding_rect()
        self.maxBullets = bullets
        self.bullets = []
        self.velocity = vel
        self.VisualUpdate = (self.spaceShip, self.position)  
        self.BulletVel = bulletVel        
        self.explosion_frame = 0

    def reset(self):
        self.bullets = []
                
    
    def build_spaceShip(self, imageName, position):
        SPACESHIP_IMAGE = pygame.transform.rotate(pygame.transform.scale(pygame.image.load(os.path.join("Assets", imageName)), self.shipSize), position[2])                
        return SPACESHIP_IMAGE                   

    def shooting(self):
        BULLET = pygame.Rect(
            self.position[0] + self.shipSize[0]//2, self.position[1] + self.shipSize[1]//2, 10, 5
        )        
        if len(self.bullets) < self.maxBullets:
            self.bullets.append(BULLET) 
            FIRE_SOUND.play()  

    def got_hit(self, damage):
        if not self.explosion_frame:
            self.explosion_frame = 1
        EXPLOSION_SOUND.play()                      
        self.health -= damage                

    def aim_target(self, opponent):
        for bullet in self.bullets:
            if self.headDirection:
                bullet.x += self.BulletVel
                if opponent.spaceShipBox.colliderect(bullet):
                    opponent.got_hit(1)
                    self.bullets.remove(bullet)
                elif bullet.x > WIDTH:            
                    self.bullets.remove(bullet)
            else:
                bullet.x -= self.BulletVel
                if opponent.spaceShipBox.colliderect(bullet):
                    opponent.got_hit(1)
                    self.bullets.remove(bullet)
                elif bullet.x < 0:            
                    self.bullets.remove(bullet)                

    def control(self, key_pressed):
        if self.headDirection:             
            if key_pressed[K_a] and self.position[0] - self.velocity > 10:
                self.position[0] -= self.velocity                
            if key_pressed[K_d] and self.position[0] + self.velocity < WIDTH//2 - self.shipSize[0] + 5:
                self.position[0] += self.velocity            
            if key_pressed[K_s] and self.position[1] + self.velocity < HEIGHT - self.shipSize[1] - 10:
                self.position[1] += self.velocity
            if key_pressed[K_w] and self.position[1] - self.velocity > 5:                
                self.position[1] -= self.velocity            
        else:        
            if key_pressed[K_LEFT] and self.position[0] - self.velocity > WIDTH//2 + 10:
                self.position[0] -= self.velocity
            if key_pressed[K_RIGHT] and self.position[0] + self.velocity < WIDTH - self.shipSize[0] + 5:
                self.position[0] += self.velocity            
            if key_pressed[K_DOWN] and self.position[1] + self.velocity < HEIGHT - self.shipSize[1] - 10:
                self.position[1] += self.velocity
            if key_pressed[K_UP] and self.position[1] - self.velocity > 5:
                self.position[1] -= self.velocity            
            
        self.spaceShipBox = pygame.Rect(tuple(self.position), self.shipSize)                
        
# Functions
def draw_objects(list_Objects=None, *StartExplosion):        
    WINDOW.blit(BACKGROUND, (0, 0))
    pygame.draw.rect(WINDOW, WHITE, BORDER)
    
    if list_Objects != None:        
        draw_bullet(list_Objects[0].bullets, RED)
        draw_bullet(list_Objects[1].bullets, YELLOW)

        WINDOW.blits((list_Objects[0].VisualUpdate, list_Objects[1].VisualUpdate))

        if list_Objects[0].explosion_frame:
            list_Objects[0].explosion_frame = draw_explosion(list_Objects[0].position, list_Objects[0].explosion_frame)            
        if list_Objects[1].explosion_frame:
            list_Objects[1].explosion_frame = draw_explosion(list_Objects[1].position, list_Objects[1].explosion_frame)

        draw_info(list_Objects)        
    pygame.display.update()

def draw_info(list_InfoUpdate=None):    
    if list_InfoUpdate != None:
        if 0 in [list_InfoUpdate[0].health, list_InfoUpdate[1].health]:
            if list_InfoUpdate[0].health == 0:                 
                list_InfoUpdate[0].reset()                
                list_InfoUpdate[1].reset()
                WINNER_INFO = WINNER_FONT.render( f"{list_InfoUpdate[1].name} WIN!!!", 1, WHITE)                                
            else:                
                list_InfoUpdate[0].reset()                
                list_InfoUpdate[1].reset()
                WINNER_INFO = WINNER_FONT.render( f"{list_InfoUpdate[0].name} WIN!!!", 1, WHITE )                                                
            WINDOW.blit(WINNER_INFO, ((WIDTH - WINNER_INFO.get_width())//2, (HEIGHT - WINNER_INFO.get_height())//2))                        

        else:                        
            HEALTH_INFO_1 = HP_FONT.render( f"{list_InfoUpdate[0].name}: {list_InfoUpdate[0].health}", 1, WHITE )
            HEALTH_INFO_2 = HP_FONT.render( f"{list_InfoUpdate[1].name}: {list_InfoUpdate[1].health}", 1, WHITE )                                
            WINDOW.blit(HEALTH_INFO_1, (10, 10))
            WINDOW.blit(HEALTH_INFO_2, (WIDTH - HEALTH_INFO_2.get_width(), 10))            

def draw_bullet(bullets, color):
    for bullet in bullets:
        pygame.draw.rect(WINDOW, color, bullet)

def draw_explosion(position, frame):    
    if frame >= len(EXPLOSION_VISUAL):
        return 0
    WINDOW.blit(EXPLOSION_VISUAL[frame-1], position)
    update_frame = frame + 1
    return update_frame

# Main loop
def game():
    # Setup new game
    clock = pygame.time.Clock()
    run = True    
    RedSpaceShip = SpaceShip("Anh Map", RED, (100, 250, 90), "spaceship_red.png", health=20, bullets=5)  # (100, 250, 90) => x = 100, y = 250, rotation angle = 90 degree
    RedSpaceShip.damaged_event = pygame.USEREVENT + 1
    YellowSpaceShip = SpaceShip("Em", YELLOW, (700, 250, 270), "spaceship_yellow.png", health=20, bullets=5)    
    YellowSpaceShip.damaged_event = pygame.USEREVENT + 2
    VisualUpdates = (RedSpaceShip, YellowSpaceShip)    

    # Run game
    while run:
        clock.tick(FPS)                                   
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

            if event.type == pygame.KEYDOWN:
                if event.key == K_f:
                    RedSpaceShip.shooting()
                if event.key == K_KP_0:
                    YellowSpaceShip.shooting()
                if event.key == pygame.K_ESCAPE:
                    run = False
                    return
                                    
        RedSpaceShip.aim_target(YellowSpaceShip)
        YellowSpaceShip.aim_target(RedSpaceShip)

        keypressed = pygame.key.get_pressed()
        RedSpaceShip.control(keypressed)
        YellowSpaceShip.control(keypressed)        
        
        draw_objects(VisualUpdates)
        InfoUpdates = [RedSpaceShip.health, YellowSpaceShip.health]
        if 0 in InfoUpdates:
            pygame.time.wait(2000)
            break        

    game()

if __name__ == "__main__":
    game()