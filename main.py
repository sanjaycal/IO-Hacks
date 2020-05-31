import pygame
import time
import sys
import random
import math


#define pygame variables
FPS = 120
dx = 640
dy = 480
s = 5

#import image
background = pygame.image.load('Grid.jpeg')


#define simulation variables
spread_distance = 1
social_diststancing_distance = 1
time_until_spreader = 1440
time_until_immune = 2880
chance_of_infection = 50
time = 0
time_needed_in_store = 60
chance_of_death = 5
community_size_x = 100
community_size_y = 100
chance_of_going_to_other_community = 50
speed = 1
social_distancing_factor_scale = 1
communities = []
store = []
live_toll = 100
dead_toll = 0

#define classes that are being used

#defining the community class, so we can create a list of communities easier
class community():
    def __init__(self,tl_corner,width, height):
        self.tl_corner = tl_corner
        self.width = width
        self.height = height

#defining the person class, to make it easier to deal with the cariables we need to assign to a person
class person():
    # in init, we define all of the variables that a person nneds in order to work in the simulation
    def __init__(self, infected, dead, immune,x,y,store_start,which_store,social_distancing_factor):
        self.infected = infected
        self.count = 0
        self.dead = dead
        self.immune = immune
        self.vulnerable = random.randint(1,3)
        self.x = x
        self.y = y
        self.home = [x,y]
        self.infecting = False
        self.distance_to_store = math.sqrt((store[which_store][0]-self.home[0])*(store[which_store][0]-self.home[0])+(store[which_store][1]-self.home[1])*(store[which_store][1]-self.home[1]))
        self.store_start = store_start-self.distance_to_store
        self.store_end = store_start+time_needed_in_store
        self.store = which_store
        self.social_distancing_factor = social_distancing_factor
        self.num = 0

    #we use this to infect the other person. If this person is infected, it can infect others.
    def infect(self,other_person):
        if other_person.vulnerable == 3:
            if random.randint(0,60)<chance_of_infection:
                other_person.infected = True
        else:
            if random.randint(0,100)<chance_of_infection:
                other_person.infected = True

    #this updated the inbuilt counter in eacch person to deal with changes from infected to immune
    def update(self):
        if self.vulnerable == 3:
            self.chance_of_death = chance_of_death * 2
            self.time_until_immune = time_until_immune * 2
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

    #moves the person to a goal
    def move(self,goal):
        if self.dead == False:
            d = math.sqrt((goal[0]-self.x)*(goal[0]-self.x)+(goal[1]-self.y)*(goal[1]-self.y))
            self.x = (speed*goal[0]-self.x)/(d+1)+self.x
            self.y = (speed*goal[1]-self.y)/(d+1)+self.y

    #moves the person away from an object
    def move_away_from(self,object,distance):
        if self.dead == False:
            d = math.sqrt((object[0]-self.x)*(object[0]-self.x)+(object[1]-self.y)*(object[1]-self.y))
            if d<distance:
                self.x = (-(speed*object[0]-self.x)/(d+1))+self.x
                self.y = (-(speed*object[1]-self.y)/(d+1))+self.y


#this is a function that generates people for the start of the simulation
def generate_people(num,num_infected, community_ditrobution, num_communities):
    people = []
    for i in range(num_communities):
        a = community([random.randint(0,dx-community_size_x),random.randint(0,dy-community_size_y)],community_size_x,community_size_y)
        communities.append(a)
        store.append([random.randint(a.tl_corner[0],a.tl_corner[0]+community_size_x), random.randint(a.tl_corner[1],a.tl_corner[1]+community_size_y)])
    for i in range(num):
        if i < community_ditrobution[0]:
            a = person(i < num_infected,False,False, random.randint(communities[0].tl_corner[0],communities[0].tl_corner[0]+community_size_x), random.randint(communities[0].tl_corner[1],communities[0].tl_corner[1]+community_size_y), random.randint(120,1440),0,(random.random())*social_distancing_factor_scale+(2-social_distancing_factor_scale)/2)
            people.append(a)
        if i >= community_ditrobution[0]:
            a = person(i < num_infected,False,False, random.randint(communities[1].tl_corner[0],communities[1].tl_corner[0]+community_size_x), random.randint(communities[1].tl_corner[1],communities[1].tl_corner[1]+community_size_y), random.randint(120,1440),1,(random.random())*social_distancing_factor_scale+(2-social_distancing_factor_scale)/2)
            people.append(a)
    return people

#this is where we call the function that generates people
people = generate_people(100,2,[30],2)

#we set up the boilerplate for pygame here
pygame.init()
display = pygame.display.set_mode((dx, dy))
pygame.display.set_caption("Pandemic Simulator")
clock = pygame.time.Clock()


#this is the main loop for the simulation that does the simulating
while True:
    #keeps track of the time, so we can have the peole be on a schedule
    time += 1
    if time>1440:
        time-=1440

    #deals with all of the pygame events, eg quitting, and button pressing 
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                social_diststancing_distance +=1
            if event.key == pygame.K_a:
                social_diststancing_distance -=1
            if event.key == pygame.K_w:
                spread_distance +=1
            if event.key == pygame.K_s:
                spread_distance -=1
            if event.key == pygame.K_e:
                chance_of_infection +=1
            if event.key == pygame.K_d:
                chance_of_infection -=1

    #draws the background
    display.blit(background, (0,0))
    # this is the loop where we do all of the computations for every person
    for person in people:
        # this code draws the person and any areas of effect they have(e.g. social distancing distance, infection spread distance etc.)
        if person.dead:
            live_toll = live_toll - 1
            dead_toll = dead_toll + 1
        if person.infected:
            if person.infecting != True :
                pygame.draw.circle(display, pygame.Color(0,100,0), [int(person.x),int(person.y)], int((social_diststancing_distance*person.social_distancing_factor-s)/2)+s)
            if person.infecting:
                if spread_distance> ((social_diststancing_distance-s)/2)+s:
                    pygame.draw.circle(display, pygame.Color(100,0,0), [int(person.x),int(person.y)], spread_distance)
                    pygame.draw.circle(display, pygame.Color(0,100,0), [int(person.x),int(person.y)], int((social_diststancing_distance*person.social_distancing_factor-s)/2)+s)
                else:
                    pygame.draw.circle(display, pygame.Color(0,100,0), [int(person.x),int(person.y)], int((social_diststancing_distance*person.social_distancing_factor-s)/2)+s)
                    pygame.draw.circle(display, pygame.Color(100,0,0), [int(person.x),int(person.y)], spread_distance)
            pygame.draw.circle(display, pygame.Color(255,0,0), [int(person.x),int(person.y)], s)
            if person.vulnerable == 3:
                pygame.draw.circle(display, pygame.Color(255,125,255), [int(person.x),int(person.y)], s)
        elif person.immune:
            if person.dead:
                pygame.draw.circle(display, pygame.Color(0,0,0), [int(person.x),int(person.y)], s)
            else:
                pygame.draw.circle(display, pygame.Color(0,0,255), [int(person.x),int(person.y)], s)
        elif person.vulnerable == 3:
            if person.dead:
                pygame.draw.circle(display, pygame.Color(0,0,0), [int(person.x),int(person.y)], s)
            else:
                pygame.draw.circle(display, pygame.Color(50,0,50), [int(person.x),int(person.y)], int((social_diststancing_distance*person.social_distancing_factor-s)/2)+s)
                pygame.draw.circle(display, pygame.Color(125,0,255), [int(person.x),int(person.y)], s)
        else:
            pygame.draw.circle(display, pygame.Color(0,100,0), [int(person.x),int(person.y)], int((social_diststancing_distance*person.social_distancing_factor-s)/2)+s)
            pygame.draw.circle(display, pygame.Color(0,255,0), [int(person.x),int(person.y)], s)
        
        #this updates the inbuilt counter in every person
        person.update()

        #this code handles the killing of people
        if person.infected == True:
            if random.randint(0,100) <= chance_of_death:
                if time> person.store_start-120 and time<person.store_start-115:
                    person.dead = True
                    person.infected = False
                    person.infecting = False
                    person.immune = True

        #this code handles the infecting of new people by the disease
        if person.immune == False and person.infected == False:
            for operson in people:
                if operson.infecting == True:
                    if (operson.x-person.x)*(operson.x-person.x)+(operson.y-person.y)*(operson.y-person.y)<spread_distance*spread_distance:
                        operson.infect(person)
        
        #this code is so that randomness doesnt change every minute, and the person doesnt become a spazzy mess
        if time >5 and time<10:
            person.num = random.randint(0,100)

        #this code moves the person
        #This code moves people to the store at certain times of day
        if time > person.store_start and time < person.store_end:
            if person.num< chance_of_going_to_other_community:
                person.move(store[person.store])
            else:
                person.move(store[person.store-1])
            for persond in people:
                person.move_away_from([persond.x,persond.y],social_diststancing_distance*person.social_distancing_factor)
        #this code move people home every other time of day 
        else:
            person.move(person.home)
            if person.x == person.home[0] and person.y == person.home[1]:
                for persond in people:
                    if persond.x != persond.home[0] and persond.y != persond.home[1]:
                        person.move_away_from([persond.x,persond.y],social_diststancing_distance*person.social_distancing_factor)

    #this code draws the stores
    pygame.draw.rect(display,pygame.Color(0,100,100), pygame.Rect(store[0][0]-5,store[0][1]-5,10,10))
    pygame.draw.rect(display,pygame.Color(0,100,100), pygame.Rect(store[1][0]-5,store[1][1]-5,10,10))

    #this code draws the UI
    pygame.draw.circle(display, pygame.Color(0,100,0), [30,30], int((social_diststancing_distance-s)/2)+s)
    pygame.draw.circle(display, pygame.Color(100,0,0), [90,30], spread_distance)

    #this code is to make pygame execute on all of the changes we have made
    pygame.display.update()
    clock.tick(FPS)
