import pygame
from pygame.locals import *
from settings import *
from start_scene import StartScene
from game import *

pygame.init()
clock = pygame.time.Clock()

START_SCENE = StartScene()
START_SCENE.clock = clock
SETTINGS = Settings()
GAME_MULTI = GameMulti()

SCENES = {
    "start_scene": START_SCENE,
    "settings": SETTINGS,
    "game_multi": GAME_MULTI,
}

START_SCENE.list_of_scenes = SCENES
SETTINGS.list_of_scenes = SCENES
GAME_MULTI.list_of_scenes = SCENES

def main(starting_scene):        
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("BUM BUM CHIU")        
    active_scene = starting_scene

    while active_scene != None:
        pressed_keys = pygame.key.get_pressed()
        
        # Event filtering
        filtered_events = []
        for event in pygame.event.get():
            quit_attempt = False
            if event.type == pygame.QUIT:
                quit_attempt = True
            elif event.type == pygame.KEYDOWN:
                alt_pressed = pressed_keys[pygame.K_LALT] or \
                              pressed_keys[pygame.K_RALT]                
                if event.key == pygame.K_F4 and alt_pressed:
                    quit_attempt = True
            
            if quit_attempt:
                active_scene.Terminate()
            else:
                filtered_events.append(event)
        
        active_scene.ProcessInput(filtered_events, pressed_keys)
        active_scene.Update()
        active_scene.Render(screen)
        
        active_scene = active_scene.next
        
        pygame.display.flip()
        clock.tick(FPS)

if __name__ == '__main__':
    main(GAME_MULTI)