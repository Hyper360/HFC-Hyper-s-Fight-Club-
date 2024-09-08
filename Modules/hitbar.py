import pygame
import random



class Target():
    def __init__(self,screen, x, y, swidth, sheight):
        self.screen = screen
        self.HEIGHT = sheight
        self.WIDTH = swidth
        self.x  = x
        self.y = y
        self.height = 50
        self.width_general = 100
        self.delete_sig = False
        self.green = pygame.rect.Rect(self.x - 50, self.y, 50, self.height)
        self.yellow_rect_1 = pygame.rect.Rect(self.green.left - self.width_general, self.y, self.width_general, self.height)
        self.red_rect_1 = pygame.rect.Rect(0, self.y, self.WIDTH - (self.WIDTH - self.yellow_rect_1.left), self.height)
        self.yellow_rect_2 = pygame.rect.Rect(self.green.right, self.y, self.width_general, self.height)
        self.red_rect_2 = pygame.rect.Rect(self.yellow_rect_2.right, self.y, self.WIDTH - (self.WIDTH - self.yellow_rect_2.right), self.height)
        self.rects = [self.green, self.red_rect_1, self.red_rect_2, self.yellow_rect_1, self.yellow_rect_2]
        self.collideonce = False

        for rect in self.rects:
            rect.centery = self.y
    
    def draw(self):
        pygame.draw.rect(self.screen, (100, 0, 0), self.red_rect_1)
        pygame.draw.rect(self.screen, (100, 100, 0), self.yellow_rect_1)
        pygame.draw.rect(self.screen, (0, 100, 0), self.green)
        pygame.draw.rect(self.screen, (100, 100, 0), self.yellow_rect_2)
        pygame.draw.rect(self.screen, (100, 0, 0), self.red_rect_2)
        if self.delete_sig == True:
            del self
    
class Slider():
    def __init__(self,screen, vel, targetlist, height):
        self.screen = screen
        self.width = 20
        self.height = height
        self.targetlist = targetlist
        self.vel = random.randint(vel, vel*2)
        self.x = random.choice([1, self.width])
        self.rect = pygame.rect.Rect(self.x, 20, self.width, self.height)
        self.space = False
        self.delete_sig = False
        self.green = False
        self.yellow = False
        self.red = False
    
    def exit(self):
        if self.rect.x >= pygame.display.get_window_size()[0] + self.rect.width or self.rect.x <= 0 - self.rect.width:
            self.delete_sig = True
        elif self.space == True:
            if self.rect.height <= 0:
                self.delete_sig = True
            else:
                self.rect.height -= 50
    
    def return_collision(self):
        if self.vel == 0:
            if self.rect.colliderect(self.targetlist.green):
                self.green = True
                return 'green'
            if self.rect.colliderect(self.targetlist.yellow_rect_1) or self.rect.colliderect(self.targetlist.yellow_rect_2):
                self.yellow = True
                return 'yellow'
            if self.rect.colliderect(self.targetlist.red_rect_1) or self.rect.colliderect(self.targetlist.red_rect_2):
                self.red = True
                return 'red'
        elif self.delete_sig == True:
            self.space = True
            return 'delete'
        
    def draw(self):
        self.exit()
        self.return_collision()
        self.rect.x += self.vel
        
        key = pygame.key.get_pressed()
        if key[pygame.K_SPACE]:
            self.vel = 0
            self.space = True
        
        self.rect.centery = self.height/2
        pygame.draw.rect(self.screen, (255, 255, 255), self.rect)

# How to setup:
# targets = [Target(screen, WIDTH/2, HEIGHT/2, WIDTH, HEIGHT)]
# sliderlist = [Slider(screen, 30, targets[0], 900)]

# while True:
#     curr_time = pygame.time.get_ticks()
#     screen.fill((0,0,0))
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             pygame.quit()

#     for target in targets:
#         target.draw()
#         if target.delete_sig:
#             targets.remove(target)
#     for slider in sliderlist:
#         slider.draw()
#         if slider.delete_sig:
#             sliderlist.remove(slider)
#             targets.remove(target)
#     if len(sliderlist) <= 0:
#         sliderlist.append(Slider(screen, 15, target, HEIGHT))

    
#     pygame.display.flip()
#     clock.tick(30)