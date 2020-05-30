import pygame
import time
import sys
pygame.init()
dx = 640
dy = 480
display = pygame.display.set_mode((dx, dy))
clock = pygame.time.Clock()
ox = 36
oy = 36
xc = 1
yc = 1
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
    pygame.draw.rect(display, pygame.Color(255,255,255),pygame.Rect(0,0,dx,dy))
    ox+=xc
    oy+=yc
    pygame.draw.circle(display, pygame.Color(255,0,0), [ox,oy], 35)
    if ox >= dx-35 or ox<= 0+35:
        xc = xc*-1
    if oy >= dy-35 or oy<= 0+35:
        yc = yc * -1
    pygame.display.update()
    clock.tick(120)