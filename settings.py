import pygame, os

WIDTH = 1200
HEIGHT = 700

FPS = 60

class SceneBase:
    def __init__(self):
        self.list_of_scenes = {}
        self.next = self
        self.previous = self
    
    def ResetTrigger(self):
        self.next = self
        self.previous = self
    
    def ProcessInput(self, events, pressed_keys):
        print("uh-oh, you didn't override this in the child class")

    def Update(self):
        print("uh-oh, you didn't override this in the child class")

    def Render(self, screen):
        print("uh-oh, you didn't override this in the child class")

    def SwitchToScene(self, next_scene):        
        self.next = next_scene
        if next_scene:
            next_scene.ResetTrigger()
            next_scene.previous = self        
    
    def Terminate(self):
        self.SwitchToScene(None)

class Button:
    def __init__(self, text, btn_color="#ced7e0", btn_highlight="#9ccddc", btn_shadow="#054569", btn_textSize=30, btn_textColor="#062c43", cb=None):
        #Core attributes 
        self.btn_attributes = [btn_color, btn_highlight, btn_shadow]
        self.pressed = False		                                               
        self.gui_font = pygame.font.Font(None,btn_textSize)
        self.top_color = self.btn_attributes[0]        		
        self.bottom_color = self.btn_attributes[2]
        self.text = text
        self.callback = cb

        #text
        self.text_surf = self.gui_font.render(text,True,btn_textColor)

    def draw(self, screen, width, height, pos, elevation):
        # Okay
        self.elevation = elevation
        self.dynamic_elevation = elevation
        self.original_y_pos = pos[1]                		                

        # top rectangle 
        self.top_rect = pygame.Rect(pos, (width,height))
        self.text_rect = self.text_surf.get_rect(center = self.top_rect.center)

        # bottom rectangle 
        self.bottom_rect = pygame.Rect(pos, (width,height))		        

        # elevation logic 
        self.top_rect.y = self.original_y_pos - self.dynamic_elevation
        self.text_rect.center = self.top_rect.center 

        self.bottom_rect.midtop = self.top_rect.midtop
        self.bottom_rect.height = self.top_rect.height + self.dynamic_elevation

        pygame.draw.rect(screen,self.bottom_color, self.bottom_rect,border_radius = 12)
        pygame.draw.rect(screen,self.top_color, self.top_rect,border_radius = 12)
        screen.blit(self.text_surf, self.text_rect)
        self.check_click()               

    def check_click(self):
        mouse_pos = pygame.mouse.get_pos()
        if self.top_rect.collidepoint(mouse_pos):
            self.top_color = self.btn_attributes[1]			

            if pygame.mouse.get_pressed()[0]:
                self.dynamic_elevation = 0
                self.pressed = True                
            else:
                self.dynamic_elevation = self.elevation
                if self.pressed == True:					                                                          
                    if self.callback != None:
                        self.callback()                    
                    self.pressed = False                    
        else:
            self.dynamic_elevation = self.elevation
            self.top_color = self.btn_attributes[0]

class Settings(SceneBase):
    def __init__(self):
        SceneBase.__init__(self)                
        self.setting_bg = pygame.transform.scale(pygame.image.load(os.path.join("Assets","Setting_BG.jpg")), (WIDTH, HEIGHT))

        self.start_pos = (WIDTH//6*5, HEIGHT)        
        self.button_width = 200
        self.button_height = 40
        self.button_elevation = 5        
        
        self.button_list = {}
        self.button_list['Back'] = Button('Back', cb=self.Back)
        self.button_list['Game Sound'] = Button('Game Sound')                
        self.button_list['Exit'] = Button('Exit', cb=self.ExitSettings)

        self.offset = (self.start_pos[1] - (len(self.button_list) * self.button_height)) // (len(self.button_list) + 1)
    
    def ProcessInput(self, events, pressed_keys):
        for event in events:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:                
                self.Back()
    
    def Update(self):        
        pass
    
    def Render(self, screen):        
        screen.blit(self.setting_bg, (0,0))        
        index = 1
        x = self.start_pos[0] - (self.button_width // 2)
        for button in self.button_list:            
            button_pos = (x, index * self.offset)
            self.button_list[button].draw(screen, self.button_width, self.button_height, button_pos, self.button_elevation)
            index += 1            
    
    def Back(self):
        self.SwitchToScene(self.previous)
    
    def ExitSettings(self):
        self.SwitchToScene(self.list_of_scenes["start_scene"])