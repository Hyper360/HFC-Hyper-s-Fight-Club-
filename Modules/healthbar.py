import pygame

class HealthBar():
    def __init__(self, screen : pygame.Surface, pos : tuple, health : int, width : int, thickness : int, name = '', showname = False, font = None, multiple_bars = 0):
        self.x = pos[0]
        self.y = pos[1]
        self.initialhealth = health
        self.health = health
        self.initialwidth = width
        self.width = width
        self.thickness = thickness
        self.screen = screen
        
        self.healthratio = self.initialhealth / self.width
        self.healthbar = pygame.rect.Rect(self.x, self.y, self.health / self.healthratio, 25)
        self.damagebar = pygame.rect.Rect(self.healthbar.x, self.healthbar.y, self.width, self.healthbar.height)
        # OPTIONAL
        self.name = name
        self.showname = showname
        self.armor = None
        self.armordmg = 0
        self.weapon = None
        self.weapondmg = 0

        if font != None:
            self.font = pygame.font.Font(font, 20)
        else:
            self.font = pygame.font.SysFont('Arial', 20)

        if multiple_bars <=0 :
            self.multiplebars = False
        else:
            y = self.y
            self.multiplebars = True
            self.bars = []
            for i in range(multiple_bars):
                self.bars.append(HealthBar(self.screen, (self.x, y), self.health, self.width, self.thickness, (self.name + ' (' + str(i + 1) + ')'), self.showname, font))
                y += self.thickness /2


    def GUI(self):
        red = (141, 100, 55)
        yellow = (200, 200, 0)
        green = (0, 255, 0)
        color = (0, 0, 0)
        if self.health > self.initialhealth * 0.8:
            color = green
        elif self.health > self.initialhealth * 0.5 and self.health < self.initialhealth * 0.8:
            color = yellow
        else:
            color = red
        self.nameSurface = self.font.render(self.name + ' ' + str(self.health) + "/" + str(self.initialhealth), False, color)
        self.nameRect = self.nameSurface.get_rect()
        self.nameRect.center = self.damagebar.center
        self.screen.blit(self.nameSurface, self.nameRect)

    
    def deduct_health(self, amount):
        if self.health - (amount - self.armordmg) < 0:
            self.health = 0
            self.width = 0
        else:
            self.health -= (amount - self.armordmg)
        
        self.healthbar = pygame.rect.Rect(self.x, self.y, self.health / self.healthratio, 25)
    
    def gain_health(self, amount):
        if self.health + amount > self.initialhealth:
            self.health = self.initialhealth
        else:
            self.health += amount
        
        self.healthbar = pygame.rect.Rect(self.x, self.y, self.health / self.healthratio, 25)
    
    def change_weapons(self, weapon, weapondmg):
        self.weapon = weapon
        self.weapondmg = weapondmg

    def change_armor(self, armor, armordmg):
        self.armor = armor
        self.armordmg = armordmg
    
    def multiple_bars(self):
        zero_health = True
        if self.multiplebars:
            for bar in self.bars:
                bar.draw()
        for bar in self.bars:
            if bar.health != 0:
                zero_health = False
                break
        if zero_health == True:
            self.health = 0
    
    def draw(self):
        pygame.draw.rect(self.screen, (255, 0, 0), self.damagebar)
        pygame.draw.rect(self.screen, (0, 200, 0), self.healthbar)
        if self.showname == True:
            self.GUI()