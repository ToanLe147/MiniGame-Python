import pygame, os

pygame.init()
pygame.font.init()
pygame.mixer.init()
clock = pygame.time.Clock()

# Game Window
WIDTH = 1368
HEIGHT = 720
FPS = 60

# Color variables
WHITE = (255, 255, 255)
RED = (255, 0, 0)
DARKRED = "#480113"
BLACK = (0, 0, 0)
GREY = "#808080"
DARKBLUE = "#054569"
LIGHTBLUE = "#8ecae6"
MIDBLUE = "#219ebc"
OATYELLOW = "#f1e3bc"
HONEYYELLOW = "#ffb703"
ORANGE = "#fb8500"


# System Messages
WINNER_FONT = pygame.font.SysFont("comicsans", 100)

cwd = os.getcwd()
# Sound effects
EARTH_FIRE_SOUND = pygame.mixer.Sound(os.path.join(cwd, "Assets","Sounds","shoot-medium_10.wav"))
ALIEN_FIRE_SOUND = pygame.mixer.Sound(os.path.join(cwd, "Assets","Sounds","shoot-large_4.wav"))
SMALL_FIRE_SOUND = pygame.mixer.Sound(os.path.join(cwd, "Assets","Sounds","shoot-small_1.wav"))
EXPLOSION_SOUND = pygame.mixer.Sound(os.path.join(cwd, "Assets","Sounds","Grenade+1.wav"))


# Player controls
class P1Ctrl:
    left = pygame.K_a
    right = pygame.K_d
    up = pygame.K_w
    down = pygame.K_s
    shoot = pygame.K_f
    
    @classmethod
    def reset(cls):
        cls.left = pygame.K_a
        cls.right = pygame.K_d
        cls.up = pygame.K_w
        cls.down = pygame.K_s
        cls.shoot = pygame.K_f

class P2Ctrl:
    left = pygame.K_LEFT
    right = pygame.K_RIGHT
    up = pygame.K_UP
    down = pygame.K_DOWN
    shoot = pygame.K_RCTRL
    
    @classmethod
    def reset(cls):
        cls.left = pygame.K_LEFT
        cls.right = pygame.K_RIGHT
        cls.up = pygame.K_UP
        cls.down = pygame.K_DOWN
        cls.shoot = pygame.K_RCTRL


class SoundControl(pygame.mixer.Sound):
    def __init__(self):
        super.__init__()
        # TODO: how to manage sound in setting menu


def DrawButton(screen, button_list, start_pos, button_size, elevation, offset):
    index = 0
    x = start_pos[0]
    for button in button_list:
        new_button_pos = (x, start_pos[1] + index * offset)
        button_list[button].draw(screen, button_size[0], button_size[1], new_button_pos, elevation)
        index += 1
        
class SceneBase:
    def __init__(self):
        self.list_of_scenes = {}
        self.name = ""
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

    def SwitchToScene(self, next_scene, FixedPrevious=None):
        self.next = next_scene
        if next_scene:
            next_scene.ResetTrigger()
            next_scene.previous = self
            if FixedPrevious:
                next_scene.previous = FixedPrevious
    
    def Terminate(self):
        self.SwitchToScene(None)

class VisualBar():
    def __init__(self, pos, size, num, max_num, border_cl="#000000", remain_cl="#00FF00", lost_cl="#480113", border_size=2):
        self.x = pos[0]
        self.y = pos[1]
        self.size_x = size[0]
        self.size_y = size[1]
        self.border_color = border_cl
        self.border_size = border_size
        self.remain_color = remain_cl
        self.lost_color = lost_cl
        self.num = num
        self.max_num = max_num

    def draw(self, screen, num):
        self.num = num
        ratio = self.num / self.max_num
        remain = self.size_x - self.border_size*2
        pygame.draw.rect(screen, self.border_color, (self.x - self.border_size, self.y - self.border_size, self.size_x, self.size_y))
        pygame.draw.rect(screen, self.lost_color, (self.x, self.y, self.size_x - self.border_size*2, self.size_y - self.border_size*2))
        pygame.draw.rect(screen, self.remain_color, (self.x, self.y, remain*ratio, self.size_y - self.border_size*2))

class Button:
    def __init__(self, text, btn_color="#ced7e0", btn_highlight="#9ccddc", btn_shadow="#054569", btn_textSize=30, btn_textColor="#062c43", cb=None):
        #Core attributes 
        self.btn_attributes = [btn_color, btn_highlight, btn_shadow]
        self.pressed = False		                                               
        # self.gui_font = pygame.font.Font(os.path.join(os.getcwd(), "Assets", "Fonts", "monogram.ttf"), btn_textSize)
        self.gui_font = pygame.font.SysFont("monaco", btn_textSize)
        self.top_color = self.btn_attributes[0]        		
        self.bottom_color = self.btn_attributes[2]
        self.text = text
        self.callback = cb

        #text
        self.text_surf = self.gui_font.render(text,True,btn_textColor)

    def draw(self, screen, width, height, pos, elevation, disable=False):
        # Okay
        self.elevation = elevation        
        self.original_y_pos = pos[1]                		                

        # top rectangle 
        self.top_rect = pygame.Rect(pos, (width,height))
        self.text_rect = self.text_surf.get_rect(center = self.top_rect.center)

        # bottom rectangle 
        self.bottom_rect = pygame.Rect(pos, (width,height))		        

        # elevation logic 
        self.top_rect.y = self.original_y_pos - self.elevation         

        self.bottom_rect.midtop = self.top_rect.midtop        
        self.bottom_rect.y = self.original_y_pos        
        self.check_click(screen, disable)

    def check_click(self, screen, disable=False):
        mouse_pos = pygame.mouse.get_pos()
        if not disable:
            if self.top_rect.collidepoint(mouse_pos):
                self.top_color = self.btn_attributes[1]			

                if pygame.mouse.get_pressed()[0]:                
                    self.top_rect.y = self.original_y_pos
                    self.pressed = True                
                else:            
                    self.top_rect.y = self.original_y_pos - self.elevation
                    if self.pressed == True:					                                                          
                        if isinstance(self.callback, list) and self.callback != []:
                            if len(self.callback) > 1:
                                self.callback[0](*self.callback[1:])
                            else:
                                self.callback[0]()
                        else:
                            self.callback()
                        self.pressed = False                    
            else:            
                self.top_rect.y = self.original_y_pos - self.elevation
                self.top_color = self.btn_attributes[0]
        self.text_rect.center = self.top_rect.center
        pygame.draw.rect(screen,self.bottom_color, self.bottom_rect,border_radius = 12)
        pygame.draw.rect(screen,self.top_color, self.top_rect,border_radius = 12)
        screen.blit(self.text_surf, self.text_rect)

class Settings(SceneBase):
    def __init__(self):
        SceneBase.__init__(self)                
        self.setting_bg = pygame.transform.scale(pygame.image.load(os.path.join("Assets/Backgrounds","Setting_BG.jpg")), (WIDTH, HEIGHT))        

        self.start_pos = (WIDTH/5*4, HEIGHT)        
        self.button_width = 250
        self.button_height = 40
        self.button_elevation = 5        
        
        self.button_list = {}        
        self.button_list['Back'] = Button('Back', cb=self.Back)
        self.button_list['Restart Game'] = Button('Restart Game', cb=self.RestartGameMulti)
        self.button_list['Reset Game'] = Button('Reset Game', cb=self.ResetGameMulti)        
        self.button_list['Change Background'] = Button('Change Background', cb=self.ChangeBackground)
        self.button_list['Change Keys'] = Button('Change Keys', cb=self.ChangeKeys)
        self.button_list['Main Menu'] = Button('Main Menu', cb=self.ExitSettings)        

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
            if button == 'Reset Game':                                    
                if self.previous.name == "game_multi":
                    self.button_list[button].draw(screen, self.button_width, self.button_height, button_pos, self.button_elevation)
                    index += 1
            elif button == 'Change Background':
                if self.previous.name == "game_multi":
                    self.button_list[button].draw(screen, self.button_width, self.button_height, button_pos, self.button_elevation)
                    index += 1
            elif button == 'Restart Game':
                if self.previous.name == "game_multi":
                    self.button_list[button].draw(screen, self.button_width, self.button_height, button_pos, self.button_elevation)
                    index += 1
            else:                
                self.button_list[button].draw(screen, self.button_width, self.button_height, button_pos, self.button_elevation)
                index += 1            
    
    def Back(self):
        self.SwitchToScene(self.previous)
    
    def ExitSettings(self):
        self.SwitchToScene(self.list_of_scenes["start_scene"])
    
    def ResetGameMulti(self):
        self.list_of_scenes[self.previous.name].ResetGame()
        self.SwitchToScene(self.previous)

    def RestartGameMulti(self):
        self.list_of_scenes[self.previous.name].RestartGame()
        self.SwitchToScene(self.previous)
    
    def ChangeBackground(self):
        self.list_of_scenes[self.previous.name].ChangeBG()
        self.SwitchToScene(self.previous)
    
    def ChangeKeys(self):
        self.SwitchToScene(self.list_of_scenes["change_keys"], FixedPrevious=self.previous)

class ChangeKeysScene(SceneBase):
    def __init__(self):
        SceneBase.__init__(self)
        self.change_key_signal = False
        self.change_key_list = None
        self.change_key_name = None
        self.setting_bg = pygame.transform.scale(pygame.image.load(os.path.join("Assets/Backgrounds","Setting_BG.jpg")), (WIDTH, HEIGHT))                        
        self.back_button = Button('Resume', cb=self.Back)

        self.start_pos = (WIDTH//6, HEIGHT)
        self.start_pos1 = (WIDTH//6*3, HEIGHT)
        self.start_pos2 = (WIDTH//6*4, HEIGHT)
        self.button_width = 200
        self.button_height = 40
        self.button_elevation = 5        
        
        self.button_list = {}
        self.button_list['Action'] = Button('Action', OATYELLOW, btn_textColor=BLACK)
        self.button_list['left'] = Button('Move left', GREY, btn_textColor=WHITE)
        self.button_list['right'] = Button('Move right', GREY, btn_textColor=WHITE)
        self.button_list['up'] = Button('Move up', GREY, btn_textColor=WHITE)
        self.button_list['down'] = Button('Move down', GREY, btn_textColor=WHITE)
        self.button_list['shoot'] = Button('Shoot', GREY, btn_textColor=WHITE)
        self.button_list['reset'] = Button('Reset to Deafult', GREY, btn_textColor=WHITE)
        self.offset = (self.start_pos[1] - (len(self.button_list) * self.button_height)) // (len(self.button_list) + 1)
        
        self.button_list1 = {}
        self.button_list1['Player'] = Button('Player 1', OATYELLOW, btn_textColor=BLACK)
        self.button_list1['left'] = Button(f'{pygame.key.name(P1Ctrl.left)}', cb=[self.UpdateKeys, 1, 'left'])
        self.button_list1['right'] = Button(f'{pygame.key.name(P1Ctrl.right)}', cb=[self.UpdateKeys, 1, 'right'])
        self.button_list1['up'] = Button(f'{pygame.key.name(P1Ctrl.up)}', cb=[self.UpdateKeys, 1, 'up'])
        self.button_list1['down'] = Button(f'{pygame.key.name(P1Ctrl.down)}', cb=[self.UpdateKeys, 1, 'down'])
        self.button_list1['shoot'] = Button(f'{pygame.key.name(P1Ctrl.shoot)}', cb=[self.UpdateKeys, 1, 'shoot'])
        self.button_list1['default'] = Button('Reset', cb=[self.ResetKey, 1])
        self.offset1 = (self.start_pos1[1] - (len(self.button_list1) * self.button_height)) // (len(self.button_list1) + 1)
        
        self.button_list2 = {}     
        self.button_list2['Player'] = Button('Player 2', OATYELLOW, btn_textColor=BLACK)
        self.button_list2['left'] = Button(f'{pygame.key.name(P2Ctrl.left)}', cb=[self.UpdateKeys, 2, 'left'])
        self.button_list2['right'] = Button(f'{pygame.key.name(P2Ctrl.right)}', cb=[self.UpdateKeys, 2, 'right'])
        self.button_list2['up'] = Button(f'{pygame.key.name(P2Ctrl.up)}', cb=[self.UpdateKeys, 2, 'up'])
        self.button_list2['down'] = Button(f'{pygame.key.name(P2Ctrl.down)}', cb=[self.UpdateKeys, 2, 'down'])
        self.button_list2['shoot'] = Button(f'{pygame.key.name(P2Ctrl.shoot)}', cb=[self.UpdateKeys, 2, 'shoot'])
        self.button_list2['default'] = Button('Reset', cb=[self.ResetKey, 2])
        self.offset2 = (self.start_pos2[1] - (len(self.button_list2) * self.button_height)) // (len(self.button_list2) + 1)
    
    def ProcessInput(self, events, pressed_keys):
        for event in events:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                # Move to the next scene when the user pressed Enter
                print("Pressed ESC")
            if event.type == pygame.KEYDOWN:
                if self.change_key_name and self.change_key_signal and self.change_key_list:                                        
                    if self.change_key_list == 1:
                        if self.change_key_name == 'left':
                            P1Ctrl.left = event.key
                        if self.change_key_name == 'right':
                            P1Ctrl.right = event.key
                        if self.change_key_name == 'up':
                            P1Ctrl.up = event.key
                        if self.change_key_name == 'down':
                            P1Ctrl.down = event.key
                        if self.change_key_name == 'shoot':
                            P1Ctrl.shoot = event.key
                        self.button_list1[self.change_key_name] = Button(f'{pygame.key.name(event.key)}', cb=[self.UpdateKeys, 1, self.change_key_name])                      
                    
                    if self.change_key_list == 2:
                        if self.change_key_name == 'left':
                            P2Ctrl.left = event.key
                        if self.change_key_name == 'right':
                            P2Ctrl.right = event.key
                        if self.change_key_name == 'up':
                            P2Ctrl.up = event.key
                        if self.change_key_name == 'down':
                            P2Ctrl.down = event.key
                        if self.change_key_name == 'shoot':
                            P2Ctrl.shoot = event.key
                        self.button_list2[self.change_key_name] = Button(f'{pygame.key.name(event.key)}', cb=[self.UpdateKeys, 2, self.change_key_name])
                    # print(pygame.key.name(event.key))
                        
                    self.change_key_signal = False
                    self.change_key_list = None
                    self.change_key_name = None
    
    def Update(self):
        pass     
    
    def Render(self, screen):        
        screen.blit(self.setting_bg, (0,0))        
        self.back_button.draw(screen, self.button_width, self.button_height, (WIDTH//6*5, HEIGHT//5*4), self.button_elevation)
        index = 1
        index1 = 1
        index2 = 1
        x = self.start_pos[0] - (self.button_width // 2)
        x1 = self.start_pos1[0] - (self.button_width // 2)
        x2 = self.start_pos2[0] - (self.button_width // 2)
        
        for button in self.button_list:            
            button_pos = (x, index * self.offset)            
            self.button_list[button].draw(screen, self.button_width, self.button_height, button_pos, 0, disable=True)            
            index += 1
        
        for button in self.button_list1:            
            button_pos = (x1, index1 * self.offset1)
            if button == "Player":
                self.button_list1[button].draw(screen, self.button_width, self.button_height, button_pos, 0, disable=True)
            else:
                self.button_list1[button].draw(screen, self.button_width, self.button_height, button_pos, self.button_elevation)
            index1 += 1
        
        for button in self.button_list2:            
            button_pos = (x2, index2 * self.offset2)                        
            if button == "Player":
                self.button_list2[button].draw(screen, self.button_width, self.button_height, button_pos, 0, disable=True)
            else:
                self.button_list2[button].draw(screen, self.button_width, self.button_height, button_pos, self.button_elevation)            
            index2 += 1
    
    def Back(self):
        self.SwitchToScene(self.previous)
    
    def ResetKey(self, control):
        if control == 1:
            P1Ctrl.reset()
            self.button_list1['left'] = Button(f'{pygame.key.name(P1Ctrl.left)}', cb=[self.UpdateKeys, 1, 'left'])
            self.button_list1['right'] = Button(f'{pygame.key.name(P1Ctrl.right)}', cb=[self.UpdateKeys, 1, 'right'])
            self.button_list1['up'] = Button(f'{pygame.key.name(P1Ctrl.up)}', cb=[self.UpdateKeys, 1, 'up'])
            self.button_list1['down'] = Button(f'{pygame.key.name(P1Ctrl.down)}', cb=[self.UpdateKeys, 1, 'down'])
            self.button_list1['shoot'] = Button(f'{pygame.key.name(P1Ctrl.shoot)}', cb=[self.UpdateKeys, 1, 'shoot'])
        else:
            P2Ctrl.reset()
            self.button_list2['left'] = Button(f'{pygame.key.name(P2Ctrl.left)}', cb=[self.UpdateKeys, 2, 'left'])
            self.button_list2['right'] = Button(f'{pygame.key.name(P2Ctrl.right)}', cb=[self.UpdateKeys, 2, 'right'])
            self.button_list2['up'] = Button(f'{pygame.key.name(P2Ctrl.up)}', cb=[self.UpdateKeys, 2, 'up'])
            self.button_list2['down'] = Button(f'{pygame.key.name(P2Ctrl.down)}', cb=[self.UpdateKeys, 2, 'down'])
            self.button_list2['shoot'] = Button(f'{pygame.key.name(P2Ctrl.shoot)}', cb=[self.UpdateKeys, 2, 'shoot'])
        
    
    def UpdateKeys(self, button_list, button_name):
        
        if button_list == 1:
            self.button_list1[button_name] = Button("Press any key", cb=[self.UpdateKeys, button_list, button_name])
        else:
            self.button_list2[button_name] = Button("Press any key", cb=[self.UpdateKeys, button_list, button_name])
        
        self.change_key_signal = True        
        self.change_key_list = button_list
        self.change_key_name = button_name