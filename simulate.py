# simulate.py

import sys
import math
import random
import pygame
from globy import *
from game import MapBuilder, Arrow, Wall, StatusBoard
from learner import DNA, GenePool

# pygame
pygame.init()
window = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption("Genetic Pathfinding")

# fps [ fps = 60 ]
fps = 60
fps_clock = pygame.time.Clock()

# learner & map
map_builder = MapBuilder()

# game objects
goal = (goal_x, goal_y)
start = (start_x, start_y)
obstacle_map = None
obstacles = []
obstacle_colour = (138, 138, 138)
arrow_colour = (255, 255, 255)
goal_colour = (0, 255, 135)
status_board = StatusBoard(DNA().length, GenePool().population_size, 246, 18)

# main loop
interaction = True
simulation = True
while interaction or simulation:
    # interactive loop
    while interaction:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                interaction = False
                simulation = False
            if event.type == pygame.MOUSEBUTTONUP:
                map_builder.map_click(pygame.mouse.get_pos())
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    obstacles_map = map_builder.close()
                    interaction = False
                    simulation = True
        
        # render
        map_builder.render()
        window.fill((0, 0, 0))
        window.blit(map_builder.surface, map_builder.pos)
        pygame.draw.circle(window, goal_colour, (goal_x, int(goal_y)), goal_radius, 0)
        pygame.draw.circle(window, (255, 255, 255), (goal_x, int(goal_y)), goal_radius, 3)

        # pygame
        pygame.display.update()
        fps_clock.tick(60)

    # setup obstacles
    obstacles_present = False
    if obstacles_map != None:
        obstacles_present = True
        width = map_builder.x_increment

        for c, _ in enumerate(obstacles_map):
            height = 0
            x = map_builder.x + (c * map_builder.x_increment)
            y = map_builder.y
            current_wall = Wall(width, height, x, y)
            
            for r, box in enumerate(obstacles_map[c]):
                y += map_builder.y_increment
                if box:
                    height += map_builder.y_increment
                    current_wall.height = height

                if not box or r == len(obstacles_map[0]) - 1:
                    if current_wall.height != 0:
                        obstacles.append(current_wall)
                    current_wall = Wall(width, 0, x, y)
                    height = 0
                
    # gene pool
    gene_pool = GenePool()
    arrows = [Arrow(mid_length = 20, inner_angle = 120, dna = DNA()) for _ in range(gene_pool.population_size)]
    gene_pool.set_population(arrows)

    # simulation loop
    status_board.reset()
    current_frame = 0
    while simulation:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                interaction = False
                simulation = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    interaction = True
                    simulation = False
                    obstacles.clear()
        
        # render
        window.fill((0, 0, 0))
        for wall in obstacles:
            pygame.draw.rect(window, obstacle_colour, wall.rect())

        pygame.draw.circle(window, goal_colour, (goal_x, int(goal_y)), goal_radius, 0)
        pygame.draw.circle(window, (255, 255, 255), (goal_x, int(goal_y)), goal_radius, 3)

        # arrow steps
        for arrow in gene_pool.population:
            arrow.update(current_frame)
            arrow.check_death(obstacles, current_frame)
            pygame.draw.polygon(window, arrow_colour, arrow.poly_points())

        # status board
        status_board.update_time(current_frame + 1)
        render_objects = status_board.render_objects()
        pygame.draw.rect(window, status_board.rect_colour, render_objects[0])
        for pair in render_objects[1]:
            window.blit(pair[0], pair[1])

        # learner steps
        if current_frame == DNA().length - 1:
            gene_pool.natural_selection()
            for arrow in gene_pool.population:
                arrow.reset_movement()
            status_board.update(gene_pool.no_generations + 1, gene_pool.average_fitness, gene_pool.fastest_time, len(gene_pool.successful))

        # pygame
        pygame.display.update()
        fps_clock.tick(fps)
        current_frame += 1
        current_frame %= DNA().length
