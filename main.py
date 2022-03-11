import pygame, sys
import chapters
from start_scene import *
from debug import debug
from pygame.locals import *

# Pygame setting up
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Bum Chiu Chiu")
clock = pygame.time.Clock()

LOGO = []
LOGO_SPEED = 5
LOGO_POS = (300, 300)
for i in range(6):
    img = pygame.image.load(os.path.join("Assets/Game-logo",f"frame_{i}_delay-0.15s.png")).convert()
    img = pygame.transform.scale(img, (600,100))
    LOGO.append(img)
def draw_logo(logo_frame):
    clock.tick(20)
    if logo_frame < LOGO.__len__():
        screen.blit(LOGO[logo_frame], LOGO_POS)
        logo_frame += 1
    else:
        logo_frame = 0
        screen.blit(LOGO[logo_frame], LOGO_POS)
    return logo_frame

# Parts
StartScene = StartScene(screen)

# Game loop
def main():
    print("Game is running")
    logo_frame = 0

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()                         

        screen.blit(StartScene.startscene_bg, (0,0))
        StartScene.show_setting_menu()
        logo_frame = draw_logo(logo_frame)

        # debug(f"{pygame.mouse.get_pos()}", pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1])         

        pygame.display.update()
        clock.tick(FPS)


if __name__ == "__main__":
    main()