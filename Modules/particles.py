import pygame
import random

snowparticles = []
rainparticles = []
class SnowParticle():
    def __init__(self, x, y, xvel, yvel, radius, color = (255, 255, 255), gravity = None):
        self.x = x
        self.y = y
        self.xvel = xvel
        self.yvel = yvel
        self.radius = radius
        self.color = color
        self.gravity = gravity

    def render(self, screen):
        self.x += self.xvel
        self.y += self.yvel
        if self.gravity != None:
            self.yvel += self.gravity
        self.radius -= 0.02
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.radius)

class RainParticle():
    def __init__(self, x, y, xvel, yvel, width, color = (192,225,228), gravity = None):
        self.x = x
        self.y = y
        self.xvel = xvel
        self.yvel = yvel
        self.width = width
        self.color = color
        self.gravity = gravity

    def render(self, screen):
        self.x += self.xvel
        self.y += self.yvel
        self.height = 50
        if self.gravity != None:
            self.yvel += self.gravity
        self.width -= 0.05
        self.height -= 0.05
        rectting = pygame.Rect(self.x, self.y, self.width, self.height)
        pygame.draw.rect(screen, self.color, rectting)

def DrawRainParticles(screen):
    for particle in rainparticles:
        particle.render(screen)
        if particle.height <= 0:
            rainparticles.remove(particle)
        elif particle.width <= 0:
            rainparticles.remove(particle)

def DrawSnowParticles(screen):
    for particle in snowparticles:
        particle.render(screen)
        if particle.radius <= 0:
            snowparticles.remove(particle)



# for x in range(random.randint(15, 25)):
#     particle = Particle(pos[0], pos[1], random.randint(0, 20)/10, random.randint(-3, -1), random.randint(2, 5), random.choice(colors), 0.5)
#     particles.append(particle)

#     DrawParticles()
