import pygame, os
from pygame.locals import *
from settings import *
from debug import *

class Initialize(SceneBase):
    def __init__(self, side):        
        SceneBase.__init__(self)
        self.side = side  # LEFT or RIGHT
        self.scene_bg = pygame.transform.scale(pygame.image.load(os.path.join("Assets/Backgrounds", "shipyard_bg.jpg")), (WIDTH, HEIGHT))        
        self.scene_logo = pygame.transform.scale(pygame.image.load(os.path.join("Assets/Icons", "SpaceFactory.png")), (300,148))
        self.scene_logo_pos = (50, 50)
        self.shipList_logo = pygame.transform.scale(pygame.image.load(os.path.join("Assets/Icons", "spaceshipList-blue.png")), (250,52))
        self.shipList_logo_pos = (400, 100)        
        self.nameSection_logo = pygame.transform.scale(pygame.image.load(os.path.join("Assets/Icons", "name-section1.png")), (150,50))
        self.nameSection_logo_pos = (125, 240)        
        print(f"Player {side}")
        
        # ============ EDIT NAME SECTION ==================
        self.edit_name_trigger = False
        self.stop_input_name = False
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
        self.name_btn["Aceept"] = Button("Accept Spaceship", btn_color="#ff0101", btn_highlight="#ffec5f", btn_shadow="#480113", cb=self.AcceptSpaceship)

        # ============ SELECT SPACESHIP SECTION ===========
        self.ship_btn = {}
        self.ship_btn_pos = (400, 200)
        self.ship_btn_size = (250, 40)
        self.ship_btn_offset = 100
        self.ship_btn_elevation = 5
        self.ship_btn["Alien_Spaceship"] = Button("Alien Battlecruiser", cb=self.SelectAlienShip)
        self.ship_btn["Fighter_Jet"] = Button("Earth Battlecruiser", cb=self.SelectFighterJet)
        self.ship_btn["Space_Shuttle"] = Button("STS Spacecraft", cb=self.SelectSpaceShuttle)
        self.ship_btn["Star_War_Ship"] = Button("Earth Battleship", cb=self.SelectStarWarShip)
        self.ship_btn["UFO"] = Button("Alien Battleship", cb=self.SelectUFO)                

        # ============ INFORMATION SECTION =================
        self.preview_rect_pos = (750, 90)  # 700, 100 minus padding 5
        self.preview_rect_size = (310, 310)        
        self.preview_rect = pygame.Rect(self.preview_rect_pos, self.preview_rect_size)
        self.preview_spaceship = SpaceShip()
        self.GetPreview()

        self.previewBar_pos = (800, 450)
        self.previewBar_size = (254, 24)
        self.previewBar_title_pos = (750, 445)        
        self.previewBar_title_size = (30,30)
        
        # ============ FINAL SELECTION =====================
        self.spaceship = None
        # ----------------------------------------------------------------------------
    
    def ProcessInput(self, events, pressed_keys):        
        for event in events:                                      
            if event.type == pygame.KEYDOWN:
                self.InputName(event)                   
    
    def Update(self):
        pass
    
    def Render(self, screen):
        # screen.fill(OATYELLOW)
        screen.blit(self.scene_bg, (0,0))
        screen.blit(self.scene_logo, self.scene_logo_pos)
        screen.blit(self.shipList_logo, self.shipList_logo_pos)
        screen.blit(self.nameSection_logo, self.nameSection_logo_pos)
        pygame.draw.rect(screen, WHITE if self.edit_name_trigger else GREY, self.name_rect, border_radius=5)
        pygame.draw.rect(screen, DARKBLUE, self.preview_rect, border_radius=5)
        self.preview_img_rect = self.preview_img.get_rect(center=self.preview_rect.center)
        screen.blit(self.preview_img, self.preview_img_rect)
        self.name_surface = self.name_font.render(self.name, True, self.name_color)
        self.name_text_rect = self.name_surface.get_rect(center=self.name_rect.center)       
        screen.blit(self.name_surface, self.name_text_rect)
        self.DrawButton(screen, self.name_btn, self.name_btn_pos, self.name_btn_size, self.name_btn_elevation, self.name_btn_offset)
        self.DrawButton(screen, self.ship_btn, self.ship_btn_pos, self.ship_btn_size, self.ship_btn_elevation, self.ship_btn_offset)
        self.DrawPreviewInfo(screen)
        # debug(f"{pygame.mouse.get_pos()}", pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1])
        # debugImg(self.preview_spaceship.image, pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1])

    ### ============ EDIT NAME SECTION ==================        
    def InputName(self, event):                                               
        if self.edit_name_trigger and not self.name_confirm:            
            if event.key == K_BACKSPACE:
                self.name = self.name[:-1]
            elif event.key == K_RETURN:                
                self.name_confirm = True
                self.edit_name_trigger = False
                print("Press Enter")
                print(f"{self.name}")
            elif not self.stop_input_name:
                self.name += event.unicode                
        if self.name.__len__() >= 16:                                            
            self.stop_input_name = True                                
            print("Name too long now")
        else:
            self.stop_input_name = False                                            

    def EditName(self):
        self.edit_name_trigger = True
        self.name_confirm = False
        print("Can edit name now")
    
    def ConfirmName(self):
        self.name_confirm = True
        self.edit_name_trigger = False
        print("Click Confirm")
        print(f"{self.name}")
    
    def AcceptSpaceship(self):        
        self.preview_spaceship.name = self.name
        self.preview_spaceship.side = self.side
        self.preview_spaceship.Ready()        
        self.spaceship = self.preview_spaceship
        if self.spaceship.type != "basic" and self.spaceship.ready:
            self.SwitchToScene(self.previous)
    
    ### ============ SELECT SPACESHIP SECTION ==================
    def SelectAlienShip(self):
        self.preview_spaceship = SpaceShip("alien")
        self.GetPreview()
    
    def SelectFighterJet(self):
        self.preview_spaceship = SpaceShip("jet")
        self.GetPreview()

    def SelectSpaceShuttle(self):
        self.preview_spaceship = SpaceShip("shuttle")
        self.GetPreview()

    def SelectStarWarShip(self):
        self.preview_spaceship = SpaceShip("SWship")
        self.GetPreview()

    def SelectUFO(self):
        self.preview_spaceship = SpaceShip("ufo")
        self.GetPreview()

    ### ============ INFORMATION SECTION =================
    def GetPreview(self):        
        img = pygame.image.load(self.preview_spaceship.spaceship_image_path).convert_alpha()
        size = (self.preview_rect_size[0]-10,self.preview_rect_size[1]-10)
        if img.get_width() > img.get_height():
            ratio = img.get_height() / img.get_width()
            size = (self.preview_rect_size[0]-10,self.preview_rect_size[1]*ratio-10)
        elif img.get_width() < img.get_height():
            ratio = img.get_width() / img.get_height()
            size = (self.preview_rect_size[0]*ratio-10,self.preview_rect_size[1]-10)            
        self.preview_img = pygame.transform.scale(img, size)
        self.name = self.preview_spaceship.name        

    ### ============ UTILITY =================
    def DrawButton(self, screen, button_list, start_pos, button_size, elevation, offset):
        DrawButton(screen, button_list, start_pos, button_size, elevation, offset)    
    
    def DrawPreviewInfo(self, screen):
        offset = 45
        # Preview Titles
        HP_icon = pygame.transform.scale(pygame.image.load(os.path.join("Assets/Icons", "hp.png")), self.previewBar_title_size)
        screen.blit(HP_icon, self.previewBar_title_pos)
        shipVel_icon = pygame.transform.scale(pygame.image.load(os.path.join("Assets/Icons", "shipVel.png")), self.previewBar_title_size)
        screen.blit(shipVel_icon, (self.previewBar_title_pos[0], self.previewBar_title_pos[1] + offset*1))
        bulMax_icon = pygame.transform.scale(pygame.image.load(os.path.join("Assets/Icons", "bulMax.png")), self.previewBar_title_size)
        screen.blit(bulMax_icon, (self.previewBar_title_pos[0], self.previewBar_title_pos[1] + offset*2))
        bulDam_icon = pygame.transform.scale(pygame.image.load(os.path.join("Assets/Icons", "bulDam.png")), self.previewBar_title_size)
        screen.blit(bulDam_icon, (self.previewBar_title_pos[0], self.previewBar_title_pos[1] + offset*3))  
        bulVel_icon = pygame.transform.scale(pygame.image.load(os.path.join("Assets/Icons", "bulVel.png")), self.previewBar_title_size)
        screen.blit(bulVel_icon, (self.previewBar_title_pos[0], self.previewBar_title_pos[1] + offset*4))                      
        # Preview Bars
        preview_HP = VisualBar((self.previewBar_pos[0], self.previewBar_pos[1] + offset*0), self.previewBar_size, self.preview_spaceship.HP, self.preview_spaceship.org_HP)
        preview_HP.draw(screen, self.preview_spaceship.HP)
        preview_shipVel = VisualBar((self.previewBar_pos[0], self.previewBar_pos[1] + offset*1), self.previewBar_size, self.preview_spaceship.shipVel, self.preview_spaceship.org_shipVel)                   
        preview_shipVel.draw(screen, self.preview_spaceship.shipVel)
        preview_maxBullets = VisualBar((self.previewBar_pos[0], self.previewBar_pos[1] + offset*2), self.previewBar_size, self.preview_spaceship.maxBullets, self.preview_spaceship.org_maxBullets)                   
        preview_maxBullets.draw(screen, self.preview_spaceship.maxBullets)
        preview_bulletDamage = VisualBar((self.previewBar_pos[0], self.previewBar_pos[1] + offset*3), self.previewBar_size, self.preview_spaceship.bulletDamage, self.preview_spaceship.org_bulletDamage)                   
        preview_bulletDamage.draw(screen, self.preview_spaceship.bulletDamage)
        preview_bulletVel = VisualBar((self.previewBar_pos[0], self.previewBar_pos[1] + offset*4), self.previewBar_size, self.preview_spaceship.bulletVel, self.preview_spaceship.org_bulletVel)                   
        preview_bulletVel.draw(screen, self.preview_spaceship.bulletVel)        
    
class Effect():
    def __init__(self, side, type, size=None, effect="bullet", stop=False):
        self.SelectEffect(effect)                
        self.max_frame = len( next(os.walk(os.path.join(f"Assets/{self.img_str[0]}", f"{type}")))[2] )
        self.clock = clock
        self.img_index = 0.0
        self.animation_speed = 1 / self.max_frame                
        self.img_list = self.AddImg(type, self.max_frame, side, size)
        self.img = self.img_list[int(self.img_index)]        
        self.img_rect = self.img.get_rect()
        self.stop_animation = stop
    
    def StopAnimation(self):
        if not self.stop_animation:
            if self.img_index >= len(self.img_list):
                self.img_index = 0
            return False
        else:
            if self.img_index >= len(self.img_list):                
                return True
    
    def draw(self, screen):        
        if not self.StopAnimation():
            self.img = self.img_list[int(self.img_index)]                
            screen.blit(self.img, self.img_rect)
            self.img_index += self.animation_speed
            self.StopAnimation()
    
    def SelectEffect(self, effect):
        self.img_str = ["Bullets", "bul"]  # [effect folder, effect prefix]
        if effect == "bullet":
            self.img_str = ["Bullets", "bul"]
        if effect == "explosion":
            self.img_str = ["Explosion", "exp"]
        # if effect == "bullet":
        #     self.img_str = ["Bullets", "bul"]
        # if effect == "bullet":
        #     self.img_str = ["Bullets", "bul"]        

    def EffectSize(self, img, size_unit):                
        size = (size_unit, size_unit)
        if img.get_width() > img.get_height():
            ratio = img.get_height() / img.get_width()
            size = (size_unit, size_unit*ratio)
        elif img.get_width() < img.get_height():
            ratio = img.get_width() / img.get_height()
            size = (size_unit*ratio, size_unit)            
        return size
    
    def AddImg(self, type, max_frame, side, size):
        img_list = []        
        for i in range(1,max_frame+1):
            img = pygame.image.load(os.path.join(f"Assets/{self.img_str[0]}/{type}",f"{self.img_str[1]}{i}.png"))
            if size:
                img_size = self.EffectSize(img, size)
                img = pygame.transform.scale(img, img_size)            
            if side != "LEFT":            
                img_list.append(pygame.transform.flip(img, True, False))
            else:
                img_list.append(img)
        return img_list

    def SequenceEffect(self):
        pass

class SpaceShip(pygame.sprite.Sprite):
    def __init__(self, type="basic"):
        super().__init__()
        self.side = "LEFT"  # LEFT or RIGHT
        self.ready = False
        self.position = [0,0]
        self.name_font = pygame.font.Font(None, 30)   
        self.HP_bar_size = (250, 20)   
        self.HP_bar_pos = (0, 0)
        self.explosions = []        
        self.explosion_sound = EXPLOSION_SOUND 
        self.explosion_effect = 3
        
        # Basic attributes
        self.org_HP = 100
        self.bullets = []
        self.org_maxBullets = 10
        self.org_bulletDamage = 15
        self.org_bulletVel = 10        
        self.org_shipVel = 10
        self.size_unit = 100                

        if type == "basic":
            self.BasicPrototype()
        elif type == "alien":
            self.AlienSpaceShip()
        elif type == "jet":
            self.FighterJet()
        elif type == "shuttle":
            self.SpaceShuttle()
        elif type == "SWship":
            self.StarWarShip()
        elif type == "ufo":
            self.UFO()
    
    def control(self, key_pressed):        
        if self.side == "LEFT":             
            if key_pressed[K_a] and self.rect.left - self.shipVel > 0:
                self.position[0] -= self.shipVel                
            if key_pressed[K_d] and self.rect.right + self.shipVel < WIDTH/2:
                self.position[0] += self.shipVel            
            if key_pressed[K_s] and self.rect.bottom + self.shipVel < HEIGHT:
                self.position[1] += self.shipVel
            if key_pressed[K_w] and self.rect.top - self.shipVel > 0:                
                self.position[1] -= self.shipVel            
        else:        
            if key_pressed[K_LEFT] and self.rect.left - self.shipVel > WIDTH/2:
                self.position[0] -= self.shipVel
            if key_pressed[K_RIGHT] and self.rect.right + self.shipVel < WIDTH:
                self.position[0] += self.shipVel            
            if key_pressed[K_DOWN] and self.rect.bottom + self.shipVel < HEIGHT:
                self.position[1] += self.shipVel
            if key_pressed[K_UP] and self.rect.top - self.shipVel > 0:
                self.position[1] -= self.shipVel            

    def update(self):
        self.rect.center = tuple(self.position)
        self.HP_bar = VisualBar(self.HP_bar_pos, self.HP_bar_size, self.HP, self.HP_max)                        

    def got_hit(self, damage):        
        EXPLOSION = Effect(self.side, f"exp{self.explosion_effect}", 100, effect="explosion", stop=True)        
        self.explosion_sound.play()        
        self.explosions.append(EXPLOSION)                    
        self.HP -= damage  

    def shooting(self):
        self.shooting_sound.play()
        BULLET = Effect(self.side, self.bullet[0], self.bullet[1])        
        BULLET.img_rect.center = self.rect.center
        if self.bullets.__len__() < self.maxBullets:
            self.bullets.append(BULLET)            

    def aim_target(self, screen, opponent):
        for explosion in self.explosions:        
            if explosion.StopAnimation():
                self.explosions.remove(explosion)
                continue
            explosion.img_rect.center = self.rect.center
            explosion.draw(screen)
        for bullet in self.bullets:            
            if self.side == "LEFT":                                
                bullet.img_rect.x += self.bulletVel                                                
                if opponent.rect.colliderect(bullet.img_rect):                                                            
                    opponent.got_hit(self.bulletDamage)                    
                    self.bullets.remove(bullet)
                elif bullet.img_rect.x > WIDTH:            
                    self.bullets.remove(bullet)
                bullet.draw(screen)
            else:                
                bullet.img_rect.x -= self.bulletVel                                
                if opponent.rect.colliderect(bullet.img_rect):                    
                    opponent.got_hit(self.bulletDamage)
                    self.bullets.remove(bullet)
                elif bullet.img_rect.x < 0:            
                    self.bullets.remove(bullet)                    
                bullet.draw(screen)
        
    def Ready(self):        
        if self.type != "Basic Prototype":            
            self.name_surface = self.name_font.render(self.name, True, OATYELLOW)                                    
            if self.HP != self.HP_max:
                self.HP = self.HP_max
            if self.side == "LEFT":
                if not self.ready:            
                    self.image = pygame.transform.rotate(self.image, 270)
                    self.rect = self.image.get_rect()
                    self.ready = True                                    
                self.name_text_rect = self.name_surface.get_rect(topleft=(0,5))
                self.HP_bar_pos = (self.name_text_rect.right + 5, 5)                                        
                self.position = [WIDTH/4, HEIGHT/2]                                                                        
            elif self.side == "RIGHT":
                if not self.ready:
                    self.image = pygame.transform.rotate(self.image, 90)
                    self.rect = self.image.get_rect()
                    self.ready = True                    
                self.name_text_rect = self.name_surface.get_rect(topright=(WIDTH,5))
                self.HP_bar_pos = (self.name_text_rect.left - self.HP_bar_size[0] - 5, 5)
                self.position = [WIDTH/4*3, HEIGHT/2]                
            else:
                pass                                        

    def GetSpaceShipSize(self, delta_unit=0):
        img = pygame.image.load(self.spaceship_image_path).convert_alpha()
        size_unit = self.size_unit - delta_unit
        size = (size_unit, size_unit)
        if img.get_width() > img.get_height():
            ratio = img.get_height() / img.get_width()
            size = (size_unit, size_unit*ratio)
        elif img.get_width() < img.get_height():
            ratio = img.get_width() / img.get_height()
            size = (size_unit*ratio, size_unit)            
        return pygame.transform.scale(img, size), size

    def BasicPrototype(self):
        # Special attributes
        self.name = "Unknown"
        self.type = "Basic Prototype"        
        self.spaceship_image_path = os.path.join("Assets/Spaceships", "basicprototype.png")
        self.image, self.shipSize = self.GetSpaceShipSize()
        self.rect = self.image.get_rect()
        # Basic attributes
        self.HP = self.org_HP / 2       
        self.HP_max = self.HP
        self.maxBullets = self.org_maxBullets / 2
        self.bulletDamage = self.org_bulletDamage / 2
        self.bulletVel = self.org_bulletVel / 2     
        self.shipVel = self.org_shipVel / 2
    
    def AlienSpaceShip(self):        
        # Special attributes
        self.name = "Streiv'kx"
        self.type = "Battlecruiser"        
        self.spaceship_image_path = os.path.join("Assets/Spaceships", "alien-spaceship.png")        
        self.image, self.shipSize = self.GetSpaceShipSize()
        self.rect = self.image.get_rect()
        self.shooting_sound = ALIEN_FIRE_SOUND
        self.bullet = ("bullet6", 70)                        
        # Basic attributes
        self.HP = self.org_HP - 40       
        self.HP_max = self.HP
        self.maxBullets = self.org_maxBullets - 5
        self.bulletDamage = self.org_bulletDamage - 8
        self.bulletVel = self.org_bulletVel - 4
        self.shipVel = self.org_shipVel - 3.5
    
    def FighterJet(self):        
        # Special attributes
        self.name = "BC Invictus"
        self.type = "Battlecruiser"        
        self.spaceship_image_path = os.path.join("Assets/Spaceships", "fighter-jet.png")        
        self.image, self.shipSize = self.GetSpaceShipSize(20)
        self.rect = self.image.get_rect()
        self.shooting_sound = EARTH_FIRE_SOUND
        self.bullet = ("bullet5", 70)
        # Basic attributes
        self.HP = self.org_HP - 40        
        self.HP_max = self.HP
        self.maxBullets = self.org_maxBullets - 4
        self.bulletDamage = self.org_bulletDamage - 9
        self.bulletVel = self.org_bulletVel - 3.5        
        self.shipVel = self.org_shipVel - 2.8
    
    def SpaceShuttle(self):        
        # Special attributes
        self.name = "STS Traveler"
        self.type = "Spaceship"        
        self.spaceship_image_path = os.path.join("Assets/Spaceships", "space-shuttle.png")        
        self.image, self.shipSize = self.GetSpaceShipSize(50)
        self.rect = self.image.get_rect()
        self.shooting_sound = SMALL_FIRE_SOUND
        self.bullet = ("bullet4", 50)
        # Basic attributes
        self.HP = self.org_HP - 65     
        self.HP_max = self.HP  
        self.maxBullets = self.org_maxBullets - 2
        self.bulletDamage = self.org_bulletDamage - 10.5
        self.bulletVel = self.org_bulletVel - 3        
        self.shipVel = self.org_shipVel - 2.5
    
    def StarWarShip(self):        
        # Special attributes
        self.name = "ISS Guardian"
        self.type = "Battleship"        
        self.spaceship_image_path = os.path.join("Assets/Spaceships", "star-war-spaceship.png")        
        self.image, self.shipSize = self.GetSpaceShipSize(-30)
        self.rect = self.image.get_rect()
        self.shooting_sound = EARTH_FIRE_SOUND
        self.bullet = ("bullet2", 80)
        # Basic attributes
        self.HP = self.org_HP - 15       
        self.HP_max = self.HP
        self.maxBullets = self.org_maxBullets - 5
        self.bulletDamage = self.org_bulletDamage - 5
        self.bulletVel = self.org_bulletVel - 5        
        self.shipVel = self.org_shipVel - 4.5
    
    def UFO(self):        
        # Special attributes
        self.name = "Naqok"
        self.type = "Battleship"
        self.ready = True        
        self.spaceship_image_path = os.path.join("Assets/Spaceships", "ufo.png")        
        self.image, self.shipSize = self.GetSpaceShipSize(-50)
        self.rect = self.image.get_rect()
        self.shooting_sound = ALIEN_FIRE_SOUND
        self.bullet = ("bullet3", 100)
        # Basic attributes
        self.HP = self.org_HP       
        self.HP_max = self.HP 
        self.maxBullets = self.org_maxBullets - 7
        self.bulletDamage = self.org_bulletDamage
        self.bulletVel = self.org_bulletVel - 5        
        self.shipVel = self.org_shipVel - 6