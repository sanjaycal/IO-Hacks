import pygame
import time
import sys
pygame.init()
FPS = 30
air_resistance = 0.97
dx = 640
dy = 480
display = pygame.display.set_mode((dx, dy))
clock = pygame.time.Clock()
ox = 36
oy = 36
xc = 100
yc = 0
s = 35
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
    pygame.draw.rect(display, pygame.Color(255,255,255),pygame.Rect(0,0,dx,dy))
    ox+=xc
    oy+=yc
    yc+=9.81/FPS
    xc = air_resistance * xc
    yc = air_resistance * yc
    pygame.draw.circle(display, pygame.Color(255,0,0), [int(ox),int(oy)], s)
    if ox >= dx-s or ox<= 0+s:
        xc = xc*-1
    if oy >= dy-s or oy<= 0+s:
        yc = yc * -1
    pygame.display.update()
    clock.tick(FPS)