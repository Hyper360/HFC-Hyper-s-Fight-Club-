import pygame

fadeend = False
def fadetoblack(width, height, limit):
    global fadeend
    fade = pygame.Surface((width, height))
    fade.fill((0,0,0))
    screen = pygame.display.get_surface()
    for alpha in range(0, limit, 2):
        fade.set_alpha(alpha)
        screen.blit(fade, (0,0))
        if alpha >= limit:
            break
            
        pygame.display.flip()
        pygame.time.delay(10)
    fadeend = True
    pygame.mixer.music.stop()
    

    