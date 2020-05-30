import pygame
import time
import sys
class person():
    def __init__(self, infected, dead, immune,x,y):
        self.infected = infected
        self.dead = dead
        self.immune = immune
        self.x = x
        self.y = y

bob = person(True, False, False,36,82)
Steve = person(False, False, False,82,36)
people = [bob,Steve]


pygame.init()
FPS = 30
air_resistance = 0.97
dx = 640
dy = 480
display = pygame.display.set_mode((dx, dy))
clock = pygame.time.Clock()
s = 5
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
    pygame.draw.rect(display, pygame.Color(255,255,255),pygame.Rect(0,0,dx,dy))
    for person in people:
        pygame.draw.circle(display, pygame.Color(255,0,0), [int(person.x),int(person.y)], s)
    pygame.display.update()
    clock.tick(FPS)