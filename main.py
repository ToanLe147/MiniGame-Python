import pygame, asyncio
from pygame.locals import *
from settings import *
from start_scene import StartScene
from game import *

START_SCENE = StartScene()
START_SCENE.clock = clock
START_SCENE.name = "start_scene"

SETTINGS = Settings()
SETTINGS.name = "settings"
SETTINGS_CHANGEKEYS = ChangeKeysScene()
SETTINGS_CHANGEKEYS.name = "change_keys"

GAME_MULTI = GameMulti()
GAME_MULTI.name = "game_multi"

SCENES = {
    START_SCENE.name: START_SCENE,
    SETTINGS.name: SETTINGS,
    SETTINGS_CHANGEKEYS.name: SETTINGS_CHANGEKEYS,
    GAME_MULTI.name: GAME_MULTI,
}

START_SCENE.list_of_scenes = SCENES
SETTINGS.list_of_scenes = SCENES
SETTINGS_CHANGEKEYS.list_of_scenes = SCENES
GAME_MULTI.list_of_scenes = SCENES

async def main(starting_scene):    
    screen = pygame.display.set_mode((WIDTH, HEIGHT))            
    active_scene = starting_scene
    pygame.display.set_caption("BUM BUM CHIU")

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
        await asyncio.sleep(0)

if __name__ == '__main__':
    asyncio.run(main(START_SCENE))