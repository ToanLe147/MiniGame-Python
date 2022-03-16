import pygame, os
from settings import Button, WIDTH, HEIGHT, SceneBase
class StartScene(SceneBase):
    def __init__(self):
        SceneBase.__init__(self)            
        self.setting_bg = pygame.transform.scale(pygame.image.load(os.path.join("Assets","start_bg.jpg")), (WIDTH, HEIGHT))
        self.logo = [ pygame.transform.scale(pygame.image.load(os.path.join("Assets/Game-logo",f"frame_{i}_delay-0.15s.png")), (600,100)) for i in range(6) ]
        self.logo_pos = (100, 300)
        self.logo_frame = 0
        self.clock = None

        self.start_pos = (WIDTH//6*5, HEIGHT)        
        self.button_width = 200
        self.button_height = 40
        self.button_elevation = 5        
        
        self.button_list = {}
        self.button_list['Campaign'] = Button('Campaign')
        self.button_list['1 vs 1'] = Button('1 vs 1', cb=self.GameMulti)
        self.button_list['Settings'] = Button('Settings', cb=self.Settings)
        self.button_list['Exit'] = Button('Exit', cb=self.Exit)

        self.offset = (self.start_pos[1] - (len(self.button_list) * self.button_height)) // (len(self.button_list) + 1)
    
    def ProcessInput(self, events, pressed_keys):
        for event in events:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                # Move to the next scene when the user pressed Enter
                print("Pressed ESC")
    
    def Update(self):        
        pass

    def draw_logo(self, screen):
        if self.clock:
            self.clock.tick(20)                    
        if self.logo_frame < self.logo.__len__():
            screen.blit(self.logo[self.logo_frame], self.logo_pos)
            self.logo_frame += 1
        else:
            self.logo_frame = 0
            screen.blit(self.logo[self.logo_frame], self.logo_pos)        
    
    def Render(self, screen):        
        screen.blit(self.setting_bg, (0,0))
        self.draw_logo(screen)
        index = 1
        x = self.start_pos[0] - (self.button_width // 2)
        for button in self.button_list:            
            button_pos = (x, index * self.offset)
            self.button_list[button].draw(screen, self.button_width, self.button_height, button_pos, self.button_elevation)
            index += 1  
    
    def Settings(self):
        self.SwitchToScene(self.list_of_scenes["settings"])        
    
    def Exit(self):
        self.Terminate()
    
    def GameMulti(self):
        self.SwitchToScene(self.list_of_scenes["game_multi"])