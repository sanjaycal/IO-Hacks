import pygame
import time
import sys
import random

spread_distance = 600
time_until_spreader = 50
chance_of_infection = 0.5
class person():
    def __init__(self, infected, dead, immune,x,y):
        self.infected = infected
        self.count = 0
        self.dead = dead
        self.immune = immune
        self.x = x
        self.y = y
        self.infecting = False
    def infect(self,other_person):
        if self.infecting and random.randint(0,100)<chance_of_infection:
            other_person.infected = True
    def update(self):
        if self.infected == True:
            if self.infecting == False:
                self.count = self.count+1
        if self.count >=time_until_spreader:
            self.infecting = True 

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
        pygame.draw.circle(display, pygame.Color(255*person.infected,255-255*person.infected,255-255*person.infected), [int(person.x),int(person.y)], s)
        person.update()
        if person.immune == False and person.infected == False:
            for operson in people:
                if operson.infecting == True:
                    if (operson.x-person.x)^2+(operson.y-person.y)^2<spread_distance^2:
                        operson.infect(person)
    pygame.display.update()
    clock.tick(FPS)