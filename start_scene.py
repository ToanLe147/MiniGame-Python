import sys, os
import pygame
from button import Button
from game import game

SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 700
FPS = 60

class StartScene():
    def __init__(self, screen) -> None:
        self.startscene_bg = pygame.transform.scale(pygame.image.load(os.path.join("Assets","start_bg.jpg")), (screen.get_width(), screen.get_height())).convert()                
        
        self.start_pos = (SCREEN_WIDTH//6*5, SCREEN_HEIGHT)        
        self.button_width = 200
        self.button_height = 40
        self.button_elevation = 5
        
        self.button_list = {}
        # self.button_list['Campaign'] = Button(screen, 'Campaign', self.campagin_mode)
        self.button_list['Multiplayers'] = Button(screen, 'Multiplayers', self.multi_player_mode)
        # self.button_list['Settings'] = Button(screen, 'Settings', self.settings_scene)
        self.button_list['Exit'] = Button(screen, 'Exit', self.exit)

        self.offset = (self.start_pos[1] - (len(self.button_list) * self.button_height)) // (len(self.button_list) + 1)
                       

    def show_setting_menu(self):        
        index = 1
        x = self.start_pos[0] - (self.button_width // 2)
        for button in self.button_list:            
            button_pos = (x, index * self.offset)
            self.button_list[button].draw(self.button_width, self.button_height, button_pos, self.button_elevation)
            index += 1        
    
    # def campagin_mode(self):
        # print("Campaign mode")
    
    def multi_player_mode(self):        
        print("Multiplayer")
        game()    

    # def settings_scene(self):                
        # print("Settings")
    
    def exit(self):
        pygame.quit()
        sys.exit()