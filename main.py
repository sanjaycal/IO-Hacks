import pygame
import time
import sys
import random
import math

FPS = 120
air_resistance = 0.97
dx = 640
dy = 480

spread_distance = 10
time_until_spreader = 1440
time_until_immune = 2880
chance_of_infection = 50
store = [[random.randint(0,dx),random.randint(0,dy)],[random.randint(0,dx),random.randint(0,dy)]]
time = 0
time_needed_in_store = 60
chance_of_death = 5
s = 5

class person():
    def __init__(self, infected, dead, immune,x,y,store_start,which_store):
        self.infected = infected
        self.count = 0
        self.dead = dead
        self.immune = immune
        self.x = x
        self.y = y
        self.home = [x,y]
        self.infecting = False
        self.distance_to_store = math.sqrt((store[which_store][0]-self.home[0])*(store[which_store][0]-self.home[0])+(store[which_store][1]-self.home[1])*(store[which_store][1]-self.home[1]))
        self.store_start = store_start-self.distance_to_store
        self.store_end = store_start+time_needed_in_store
        self.store = which_store
    def infect(self,other_person):
        if random.randint(0,100)<chance_of_infection:
            other_person.infected = True
    def update(self):
        if self.infected == True:
            self.count = self.count+1
        if self.count >=time_until_spreader and self.infecting == False:
            self.infecting = True 
            self.count = 0
        if self.count >=time_until_immune  and self.infecting == True:
            self.infecting = False 
            self.infected = False
            self.immune = True
            self.count = 0
    def move(self,goal):
        if self.dead == False:
            d = math.sqrt((goal[0]-self.x)*(goal[0]-self.x)+(goal[1]-self.y)*(goal[1]-self.y))
            self.x = (goal[0]-self.x)/(d+1)+self.x
            self.y = (goal[1]-self.y)/(d+1)+self.y

def generate_people(num,num_infected, store_ditrobution):
    people = []
    for i in range(num):
        if i < store_ditrobution[0]:
            a = person(i < num_infected,False,False, random.randint(0,dx/10)*10, random.randint(0,dy/10)*10, random.randint(120,1440),0)
            people.append(a)
        if i >= store_ditrobution[0]:
            a = person(i < num_infected,False,False, random.randint(0,dx/10)*10, random.randint(0,dy/10)*10, random.randint(120,1440),1)
            people.append(a)
    return people


people = generate_people(100,2,[30])


pygame.init()

display = pygame.display.set_mode((dx, dy))
clock = pygame.time.Clock()

while True:
    time += 1
    print(time)
    if time>1440:
        time-=1440
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
    pygame.draw.rect(display, pygame.Color(255,255,255),pygame.Rect(0,0,int(dx),int(dy)))
    for person in people:
        if person.infected:
            if person.infecting:
                pygame.draw.circle(display, pygame.Color(100,0,0), [int(person.x),int(person.y)], spread_distance)
            pygame.draw.circle(display, pygame.Color(255,0,0), [int(person.x),int(person.y)], s)
        elif person.immune:
            if person.dead:
                pygame.draw.circle(display, pygame.Color(0,0,0), [int(person.x),int(person.y)], s)
            else:
                pygame.draw.circle(display, pygame.Color(0,0,255), [int(person.x),int(person.y)], s)
        else:
            pygame.draw.circle(display, pygame.Color(0,255,0), [int(person.x),int(person.y)], s)
        person.update()
        if person.infected == True:
            if random.randint(0,100) <= chance_of_death:
                if time> person.store_start-120 and time<person.store_start-115:
                    person.dead = True
                    person.infected = False
                    person.infecting = False
                    person.immune = True
        if person.immune == False and person.infected == False:
            for operson in people:
                if operson.infecting == True:
                    if (operson.x-person.x)*(operson.x-person.x)+(operson.y-person.y)*(operson.y-person.y)<spread_distance*spread_distance:
                        operson.infect(person)
        if time > person.store_start and time < person.store_end:
            person.move(store[person.store])
        else:
            person.move(person.home)
    pygame.draw.rect(display,pygame.Color(0,100,100), pygame.Rect(store[0][0]-5,store[0][1]-5,10,10))
    pygame.draw.rect(display,pygame.Color(0,100,100), pygame.Rect(store[1][0]-5,store[1][1]-5,10,10))
    pygame.display.update()
    clock.tick(FPS)