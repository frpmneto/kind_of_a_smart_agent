from xmlrpc.client import boolean
import pygame
import random
import numpy as np
import math
import ctypes

class Agent:
    pos = (0,0)
    size = 0
    color = (0, 0, 0)
    speed = 1

    def __init__(self, pos, size, color, speed=1):
        self.pos = pos
        self.size = size
        self.color = color
        self.speed = speed

    def move(self, frutinha):
        x = (frutinha.pos[0] - self.pos[0]) / (((frutinha.pos[0] - self.pos[0])**2 + (frutinha.pos[1] - self.pos[1])**2)**(1/2))
        y = (frutinha.pos[1] - self.pos[1]) / (((frutinha.pos[0] - self.pos[0])**2 + (frutinha.pos[1] - self.pos[1])**2)**(1/2))
        
        self.pos = (self.pos[0]+(x*self.speed), self.pos[1]+(y*self.speed))

def generate_randon_pos(carinha, grid_size, comidinha_size):
    xmin = comidinha_size//2 + 10
    ymin = comidinha_size//2 + 10
    xmax = grid_size[0] - comidinha_size//2 - 10
    ymax = grid_size[1] - comidinha_size//2 - 10

    inside = 1
    while inside:
        x = random.randrange( xmin, xmax)
        if x < carinha.pos[0] - (carinha.size + 20 + comidinha_size) or x > carinha.pos[0] + (carinha.size + 20 + comidinha_size):
            inside=0
    inside = 1
    while inside:
        y = random.randrange( ymin, ymax)
        if y < carinha.pos[1] - (carinha.size + 20 + comidinha_size) or y > carinha.pos[1] + (carinha.size + 20 + comidinha_size):
            inside=0

    return (x,y)

def comidinha_cor():
    return (random.randrange(0,255), random.randrange(0,255), random.randrange(0,255))

def check_colision(a, b):
    if (((a.pos[0] - b.pos[0])**2 + (a.pos[1] - b.pos[1])**2)**(1/2)) <= a.size + b.size:
        return True
    return False

def printa_pac(screen, image, image_pos, angle):
    rotated_image = pygame.transform.rotate(image, angle)
    new_pos = rotated_image.get_rect(center = image.get_rect(topleft = image_pos).center)
    screen.blit(rotated_image, new_pos.topleft)

def get_angle(carinha, comidinha):
    dy = - comidinha.pos[1] + carinha.pos[1]
    dx = + comidinha.pos[0] - carinha.pos[0]
    if dx == 0:
        if dy > 0:
            rad = 3*math.pi/2
        else:
            rad = math.pi/2
    else:
        rad = np.arctan(dy/dx)
    deg = rad*180/math.pi

    if dx > 0:
        deg+=180

    return deg

user32 = ctypes.windll.user32
screensize = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)
pygame.init()
# screen_size = [800, 600]
screen_size = (screensize[0], screensize[1])
screen = pygame.display.set_mode(screen_size)
fps = 60
clock = pygame.time.Clock()
carinha = Agent((255,255), 40, (255, 255, 0))
is_alive = 0
comidinha_size = 20
dineros = 0

default_font = pygame.font.get_default_font()
font=pygame.font.SysFont(default_font, 32) 
text = font.render("", 1, (255,255,255))
text = font.render("Pontos: " + str(dineros), 1, (255,255,255))
retangulinho = text.get_rect()
retangulinho.center = (screen_size[0]//2, 20)



pac = pygame.image.load('files\cabinha.png')
pac_pos = pac.get_rect()
pac = pygame.transform.scale(pac, (50,50))
pac2 = pygame.image.load('files\cabinha2.png')
pac2_pos = pac2.get_rect()
pac2 = pygame.transform.scale(pac2, (50,50))
i=0

running = True
while running:
    i+=1
    clock.tick(fps)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
    background_color = (0, 0, 0)
    screen.fill(background_color)


    if not is_alive:
        pos =  generate_randon_pos(carinha, screen_size, comidinha_size)
        comidinha = Agent(pos, comidinha_size, comidinha_cor())
        is_alive = 1
    else:
        carinha.move(comidinha)
        if carinha.speed + 0.1 < carinha.size/2:
            carinha.speed+=0.1        
        if check_colision(carinha, comidinha):
            dineros+=1
            carinha.speed = 1
            is_alive = 0
            text = font.render("Pontos: " + str(dineros), 1, (255,255,255))
            
    
    if i<=10:
        printa_pac(screen, pac, (carinha.pos[0]-carinha.size/2, carinha.pos[1]-carinha.size/2), get_angle(carinha, comidinha))
    elif i>10 and i<20:
        printa_pac(screen, pac2, (carinha.pos[0]-carinha.size/2, carinha.pos[1]-carinha.size/2), get_angle(carinha, comidinha))
    else:
        printa_pac(screen, pac2, (carinha.pos[0]-carinha.size/2, carinha.pos[1]-carinha.size/2), get_angle(carinha, comidinha))
        i=0

    if is_alive:
        pygame.draw.circle(screen, comidinha.color, comidinha.pos, comidinha.size)
    screen.blit(text, retangulinho) 
    pygame.display.flip()

pygame.quit()
