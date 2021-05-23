# simulate.py

import pygame
import numpy as np 
from game import *
pygame.init()

# pygame
window = pygame.display.set_mode((window_width, window_height))
window.fill((0, 0, 0))
pygame.display.set_caption("Genetic Movement")
fps = 30
fps_clock = pygame.time.Clock()

# game
cars = [Car() for _ in range(population_size)]

run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    keys_pressed = pygame.key.get_pressed()

    pygame.display.update()
    fps_clock.tick()
