import pygame, os
from game_elements import *


class GameMulti(SceneBase):
    def __init__(self):
        SceneBase.__init__(self)        
        self.game_bg = pygame.transform.scale(pygame.image.load(os.path.join("Assets","space.png")), (WIDTH, HEIGHT))
        self.game_border = pygame.Rect(WIDTH//2 - 5, 0, 10, HEIGHT)

        self.stop_input = False

        self.players = pygame.sprite.Group()                

        self.initilaization = False
        self.setupSpaceship = False

        self.system_btn_list = {}
        self.system_btn_pos = (500, 450)
        self.system_btn_size = (200, 40)
        self.system_btn_offset = 100
        self.system_btn_elevation = 5
        self.system_btn_list["Restart"] = Button("Restart", cb=self.RestartGame)                         
        self.system_btn_list["Reset"] = Button("Reset", cb=self.ResetGame)                         

    def InitPlayer(self):                
        if not self.initilaization:
            self.player_1_init = Initialize("LEFT")
            self.player_1_init.previous = self
            self.player_2_init = Initialize("RIGHT")
            self.player_2_init.previous = self
            self.initilaization = True
        
        self.player_1 = self.player_1_init.spaceship
        self.player_2 = self.player_2_init.spaceship

        if not self.player_1:
            print("Setting up player 1")
            self.SwitchToScene(self.player_1_init)
        
        elif not self.player_2:
            print("Setting up player 2")
            self.SwitchToScene(self.player_2_init)                

        if self.player_1 and self.player_2:
            if self.player_1.type != "basic" and self.player_2.type != "basic":            
                self.players.add(self.player_1)
                self.players.add(self.player_2)
                self.setupSpaceship = True    

    def Winable(self, screen):
        WINNER_INFO = None
        if self.player_1.HP <= 0:
            WINNER_INFO = WINNER_FONT.render(f"{self.player_2.name} WIN!!!", 1, WHITE)
            self.stop_input = True            
        if self.player_2.HP <= 0:
            WINNER_INFO = WINNER_FONT.render(f"{self.player_1.name} WIN!!!", 1, WHITE)
            self.stop_input = True            
        if WINNER_INFO:
            screen.blit(WINNER_INFO, ((WIDTH - WINNER_INFO.get_width())//2, (HEIGHT - WINNER_INFO.get_height())//2))            
            self.DrawButton(screen, self.system_btn_list, self.system_btn_pos, self.system_btn_size, self.system_btn_elevation, self.system_btn_offset)            

    def ProcessInput(self, events, pressed_keys):        
        if self.setupSpaceship and not self.stop_input:
            self.player_1.control(pressed_keys)
            self.player_2.control(pressed_keys)
        for event in events:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:                
                self.SwitchToScene(self.list_of_scenes["settings"])
            if not self.stop_input:
                if event.type == pygame.KEYDOWN and event.key == pygame.K_KP0 and self.setupSpaceship:                
                    self.player_2.shooting()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_f and self.setupSpaceship:                
                    self.player_1.shooting()
    
    def Update(self):
        if not self.setupSpaceship:
            self.InitPlayer()
        self.players.update()                
        
    def Render(self, screen):        
        screen.blit(self.game_bg, (0,0))
        # debug(f"{pygame.mouse.get_pos()}", pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1])
        pygame.draw.rect(screen, WHITE, self.game_border)                
        if self.setupSpaceship:
            # pygame.draw.rect(screen, DARKBLUE, self.player_1.rect)
            # pygame.draw.rect(screen, DARKBLUE, self.player_2.rect)
            self.players.draw(screen)   
            self.player_1.aim_target(screen, self.player_2)
            self.player_2.aim_target(screen, self.player_1)            
            screen.blit(self.player_1.name_surface, self.player_1.name_text_rect)        
            screen.blit(self.player_2.name_surface, self.player_2.name_text_rect)
            self.player_1.HP_bar.draw(screen, self.player_1.HP)        
            self.player_2.HP_bar.draw(screen, self.player_2.HP)
            self.Winable(screen)                     
    
    def RestartGame(self):        
        self.player_1.RotateSpaceship()        
        self.player_2.RotateSpaceship()
        self.stop_input = False
    
    def ResetGame(self):
        self.initilaization = False
        self.setupSpaceship = False
        self.stop_input = False
        self.players.empty()       

    def DrawButton(self, screen, button_list, start_pos, button_size, elevation, offset):
        index = 0
        x = start_pos[0]
        for button in button_list:
            new_button_pos = (x, start_pos[1] + index * offset)
            button_list[button].draw(screen, button_size[0], button_size[1], new_button_pos, elevation)
            index += 1 
                