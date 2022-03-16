import pygame, os
from pygame.locals import *
from settings import Button, SceneBase, WIDTH, HEIGHT, VisualBar
from debug import debug

pygame.font.init()
pygame.mixer.init()

# Sound effects
FIRE_SOUND = pygame.mixer.Sound(os.path.join("Assets/Sounds","Gun+Silencer.mp3"))
EXPLOSION_SOUND = pygame.mixer.Sound(os.path.join("Assets/Sounds","Grenade+1.mp3"))

# Color variables
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREY = "#808080"
DARKBLUE = "#054569"
OATYELLOW = "#f1e3bc"

class GameMulti(SceneBase):
    def __init__(self):
        SceneBase.__init__(self)        
        self.game_bg = pygame.transform.scale(pygame.image.load(os.path.join("Assets","space.png")), (WIDTH, HEIGHT))
        self.game_border = pygame.Rect(WIDTH//2 - 5, 0, 10, HEIGHT)

        self.players = pygame.sprite.Group()
        self.effects = pygame.sprite.Group()
        self.infos = pygame.sprite.Group()

        self.initilaization = False         

    def InitPlayer(self):
        self.player_1_init = Initialize("LEFT")
        # self.player_2_init = Initialize("RIGHT")
        self.SwitchToScene(self.player_1_init)
        self.initilaization = True

    def ProcessInput(self, events, pressed_keys):
        for event in events:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:                
                self.SwitchToScene(self.list_of_scenes["settings"])
    
    def Update(self):
        if not self.initilaization:
            self.InitPlayer()
        
    def Render(self, screen):        
        screen.blit(self.game_bg, (0,0))
        pygame.draw.rect(screen, WHITE, self.game_border)
        self.players.update()
        self.effects.update()
        self.infos.update()              

class Initialize(SceneBase):
    def __init__(self, side):
        SceneBase.__init__(self)
        self.side = side  # LEFT or RIGHT
        self.scene_logo = pygame.transform.scale(pygame.image.load(os.path.join("Assets", "SpaceFactory-square.png")), (300,148))
        self.scene_logo_pos = (50, 50)
        self.shipList_logo = pygame.transform.scale(pygame.image.load(os.path.join("Assets", "spaceshipList-blue.png")), (200,52))
        self.shipList_logo_pos = (400, 100)        
        self.nameSection_logo = pygame.transform.scale(pygame.image.load(os.path.join("Assets", "name-section.png")), (150,67.5))
        self.nameSection_logo_pos = (125, 240)        
        
        # ============ EDIT NAME SECTION ==================
        self.edit_name_trigger = False
        self.name_confirm = False        
        self.name_rect_pos = (100, 300)                
        self.name_rect_size = (200, 40)               
        self.name_rect = pygame.Rect(self.name_rect_pos, self.name_rect_size)
        self.name = ""
        self.name_font = pygame.font.Font(None, 30)
        self.name_color = DARKBLUE
        self.name_surface = self.name_font.render(self.name, True, self.name_color)
        self.name_text_rect = self.name_surface.get_rect(center=self.name_rect.center) 

        self.name_btn = {}
        self.name_btn_pos = (100, 400)
        self.name_btn_size = (200, 40)
        self.name_btn_offset = 100
        self.name_btn_elevation = 5
        self.name_btn["Edit"] = Button("Edit Name", cb=self.EditName)
        self.name_btn["Confirm"] = Button("Confirm Name", cb=self.ConfirmName)
        self.name_btn["Aceept"] = Button("Accept Spaceship", btn_color="#ff0101", btn_highlight="#ffec5f", btn_shadow="#480113")

        # ============ SELECT SPACESHIP SECTION ===========
        self.ship_btn = {}
        self.ship_btn_pos = (400, 200)
        self.ship_btn_size = (200, 40)
        self.ship_btn_offset = 100
        self.ship_btn_elevation = 5
        self.ship_btn["Alien_Spaceship"] = Button("Alien Spaceship")
        self.ship_btn["Fighter_Jet"] = Button("Fighter Jet")
        self.ship_btn["Space_Shuttle"] = Button("Space Shuttle")
        self.ship_btn["Star_War_Ship"] = Button("Star War Ship")
        self.ship_btn["UFO"] = Button("UFO")                

        # ============ INFORMATION SECTION =================
        self.preview_rect_pos = (750, 90)  # 700, 100 minus padding 5
        self.preview_rect_size = (310, 310)        
        self.preview_rect = pygame.Rect(self.preview_rect_pos, self.preview_rect_size)
        self.preview_spaceship = SpaceShip()
        self.preview_img = self.GetPreview()
        self.preview_img_rect = self.preview_img.get_rect(center=self.preview_rect.center)        

        self.previewBar_pos = (850, 450)
        self.previewBar_size = (104, 24)        
    
    def ProcessInput(self, events, pressed_keys):        
        for event in events:                                      
            if event.type == pygame.KEYDOWN:
                self.InputName(event)
                if event.key == K_ESCAPE:
                    print("Press ESC")
                    self.Terminate()    
    
    def Update(self):
        pass
    
    def Render(self, screen):
        screen.fill(OATYELLOW)
        screen.blit(self.scene_logo, self.scene_logo_pos)
        screen.blit(self.shipList_logo, self.shipList_logo_pos)
        screen.blit(self.nameSection_logo, self.nameSection_logo_pos)
        pygame.draw.rect(screen, WHITE if self.edit_name_trigger else GREY, self.name_rect, border_radius=5)
        pygame.draw.rect(screen, DARKBLUE, self.preview_rect, border_radius=5)
        screen.blit(self.preview_img, self.preview_img_rect)
        self.name_surface = self.name_font.render(self.name, True, self.name_color)
        self.name_text_rect = self.name_surface.get_rect(center=self.name_rect.center)       
        screen.blit(self.name_surface, self.name_text_rect)
        self.DrawButton(screen, self.name_btn, self.name_btn_pos, self.name_btn_size, self.name_btn_elevation, self.name_btn_offset)
        self.DrawButton(screen, self.ship_btn, self.ship_btn_pos, self.ship_btn_size, self.ship_btn_elevation, self.ship_btn_offset)
        self.DrawPreviewInfo(screen)
        debug(f"{pygame.mouse.get_pos()}", pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1])

    ### ============ EDIT NAME SECTION ==================        
    def InputName(self, event):
        print(f"{self.name.__len__()}")
        if self.name.__len__() >= 16:
            self.edit_name_trigger = False                                
            print("Name too long now")
            return                    
        if self.edit_name_trigger and not self.name_confirm:            
            if event.key == K_BACKSPACE:
                self.name = self.name[:-1]
            elif event.key == K_RETURN:                
                self.name_confirm = True
                self.edit_name_trigger = False
                print("Press Enter")
                print(f"{self.name}")
            else:
                self.name += event.unicode                

    def EditName(self):
        self.edit_name_trigger = True
        self.name_confirm = False
        print("Can edit name now")
    
    def ConfirmName(self):
        self.name_confirm = True
        self.edit_name_trigger = False
        print("Click Confirm")
        print(f"{self.name}")
    
    ### ============ SELECT SPACESHIP SECTION ==================
    # def CheckEditName(self):
    #     mouse_pos = pygame.mouse.get_pos()
    #     if self.name_rect.collidepoint(mouse_pos):            
    #         if pygame.mouse.get_pressed()[0]:
    #             self.edit_name_trigger = True
    #             print("Can edit name now")

    ### ============ INFORMATION SECTION =================
    def GetPreview(self):
        img = pygame.transform.scale(pygame.image.load(self.preview_spaceship.spaceship_image_path), (self.preview_rect_size[0]-10,self.preview_rect_size[1]-10))
        return img

    ### ============ UTILITY =================
    def DrawButton(self, screen, button_list, start_pos, button_size, elevation, offset):
        index = 0
        x = start_pos[0]
        for button in button_list:
            new_button_pos = (x, start_pos[1] + index * offset)
            button_list[button].draw(screen, button_size[0], button_size[1], new_button_pos, elevation)
            index += 1
    
    def DrawPreviewInfo(self, screen):
        offset = 30
        self.preview_HP = VisualBar(self.previewBar_pos, self.previewBar_size, self.preview_spaceship.HP, self.preview_spaceship.org_HP)                   
        self.preview_HP.draw(screen, self.preview_spaceship.HP)

class Explosion(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        # Explosion
        self.explosion_index = 0
        self.explosion_list = [ pygame.image.load(os.path.join("Assets/Explosion",f"exp{i}.png")) for i in range(1,6) ]
        self.explosion = self.explosion_list[self.explosion_index]        

    def update(self):
        pass

    def destroy(self):
        pass

class SpaceShip(pygame.sprite.Sprite):
    def __init__(self, type="basic"):
        super().__init__()
        self.side = "LEFT"  # LEFT or RIGHT
        
        # Basic attributes
        self.org_HP = 100
        self.bullets = []
        self.org_maxBullets = 10
        self.org_bulletDamage = 15
        self.org_bulletVel = 10        
        self.org_shipVel = 5

        if type == "basic":
            self.BasicPrototype()
        elif type == "alien":
            self.AlienSpaceShip()
    
    def update(self):
        pass
    
    def player_input(self):
        pass

    def shooting(self):
        pass
    
    def got_hit(self, damage):
        pass

    def BasicPrototype(self):
        # Special attributes
        self.name = "Unknown"
        self.type = "Basic Prototype"
        self.shipSize = (60,60)
        self.spaceship_image_path = os.path.join("Assets/Spaceships", "basicprototype.png")
        self.image = pygame.transform.scale(pygame.image.load(self.spaceship_image_path), self.shipSize)        
        # Basic attributes
        self.HP = self.org_HP // 2       
        self.maxBullets = self.org_maxBullets // 2
        self.bulletDamage = self.org_bulletDamage // 2
        self.bulletVel = self.org_bulletVel // 2     
        self.shipVel = self.org_shipVel // 2
    
    def AlienSpaceShip(self):        
        # Special attributes
        self.name = "Streiv'kx"
        self.type = "Alien Spaceship"
        self.shipSize = (60,60)
        self.spaceship_image_path = os.path.join("Assets/Spaceships", "alien-spaceship.png")        
        self.image = pygame.transform.scale(pygame.image.load(self.spaceship_image_path), self.shipSize)        
        # Basic attributes
        self.HP = self.org_HP        
        self.maxBullets = self.org_maxBullets - 7
        self.bulletDamage = self.org_bulletDamage - 3
        self.bulletVel = self.org_bulletVel - 5        
        self.shipVel = self.org_shipVel - 4.5
    
