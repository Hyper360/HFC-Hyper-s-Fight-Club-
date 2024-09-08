import pygame
class Button():
    def __init__(self, screen, x, y, width, height, color, file = None):
        self.screen = screen
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.pressed = False
        self.prev_mouse_pressed = None
        self.rect = pygame.rect.Rect(self.x, self.y, self.width, self.height)

        # Image
        if file != None:
            self.file = pygame.image.load(file)
            self.file_rect = self.file.get_rect()
        else:
            self.file = None
    
    def get_pressed(self):
        mouse_pressed = pygame.mouse.get_pressed()[0]
        mouse_pos = pygame.mouse.get_pos()

        if self.rect.collidepoint(mouse_pos[0], mouse_pos[1]):
            if mouse_pressed == True and not self.prev_mouse_pressed:
                self.pressed = True
            else:
                self.pressed = False
        else:
            self.pressed = False
        
        self.prev_mouse_pressed = mouse_pressed

        return self.pressed
    def draw(self):
        self.get_pressed()
        pygame.draw.rect(self.screen, (255, 0, 0), self.rect, border_radius=4)
        if self.file != None:
            self.file_rect.center = self.rect.center
            self.screen.blit(self.file, self.file_rect)