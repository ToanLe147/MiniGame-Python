import sys, os
import pygame
from button import Button
from test_pygame import WIDTH

class Settings():
    def __init__(self, screen) -> None:
        self.setting_bg = pygame.transform.scale(pygame.image.load(os.path.join("Assets","Setting_BG.jpg")), (screen.get_width(), screen.get_height())).convert()        
        
        self.start_pos = (screen.get_width()//2, screen.get_height())        
        self.button_width = 200
        self.button_height = 40
        self.button_elevation = 5
        
        self.button_list = {}
        self.button_list['Game Sound'] = Button(screen, 'Game Sound', self.game_sound)
        self.button_list['Effect Sound'] = Button(screen, 'Effect Sound', self.effect_sound)
        self.button_list['Exit'] = Button(screen, 'Exit', self.exit)

        self.offset = (self.start_pos[1] - (len(self.button_list) * self.button_height)) // (len(self.button_list) + 1)
                

    def show_setting_menu(self):
        index = 1
        x = self.start_pos[0] - (self.button_width // 2)
        for button in self.button_list:            
            button_pos = (x, index * self.offset)
            self.button_list[button].draw(self.button_width, self.button_height, button_pos, self.button_elevation)
            index += 1
    
    def game_sound(self):
        print("Sound settings")
    
    def effect_sound(self):
        print("Help settings")
    
    def exit(self):
        pygame.quit()
        sys.exit()