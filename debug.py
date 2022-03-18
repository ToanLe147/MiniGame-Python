import pygame

pygame.init()
font = pygame.font.Font(None, 30)

def debug(info, x=10, y=10):
    display_surf = pygame.display.get_surface()
    debug_surf = font.render(str(info), True, "Red")
    debug_rect = debug_surf.get_rect(topleft=(x,y))
    pygame.draw.rect(display_surf, "Black", debug_rect)
    display_surf.blit(debug_surf, debug_rect)

def debugImg(img, x=10, y=10):
    display_surf = pygame.display.get_surface()
    if img:
        debug_surf = img
        debug_rect = debug_surf.get_rect(topleft=(x,y))
    else:
        debug_rect = pygame.Rect((x,y), (60,60))
        pygame.draw.rect(display_surf, "Black", debug_rect)        
    display_surf.blit(debug_surf, debug_rect)