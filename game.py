# game.py

import sys
import math
import pygame
import random
from globy import *

# map builder
class MapBuilder:
    # boundaries
    x_bounds = [window_width / 3, 2 * (window_width / 3)]
    y_bounds = [0, window_height]
    grid_dimensions = [7, 10]

    # measurements
    height = y_bounds[1] - y_bounds[0]
    width = x_bounds[1] - x_bounds[0]
    x, y = x_bounds[0], y_bounds[0]
    pos = (x, y)
    line_width = 2

    # line increments
    x_increment = width / grid_dimensions[0]
    y_increment = height / grid_dimensions[1]
    box_dims = (x_increment, y_increment)

    def __init__(self):
        self.surface = pygame.Surface((self.width, self.height))
        self.surface.fill((0, 0, 0))
        self.map = [[False for _ in range(self.grid_dimensions[1])] for _ in range(self.grid_dimensions[0])]

    def render(self):
        colour = (138, 138, 138)

        # boxes
        for c, _ in enumerate(self.map):
            for r, __ in enumerate(self.map[c]):
                if self.map[c][r]: 
                    pygame.draw.rect(self.surface, colour, (c * self.x_increment + self.line_width, r * self.y_increment + self.line_width, *self.box_dims))
                else:
                    line_width = self.line_width
                    pygame.draw.rect(self.surface, (0,0,0), (c * self.x_increment + line_width, r * self.y_increment + line_width, self.x_increment - line_width, self.y_increment - line_width))

        # vertical lines
        pygame.draw.line(self.surface, colour, (0, 0), (0, self.height), self.line_width)
        for i in range(self.grid_dimensions[0] - 1):
            x = self.x_increment * (i + 1)
            pygame.draw.line(self.surface, colour, (x, 0), (x, self.height), self.line_width)
        pygame.draw.line(self.surface, colour, (self.width - self.line_width, 0), (self.width - self.line_width, self.height), self.line_width)

        # horizontal lines
        pygame.draw.line(self.surface, colour, (0,0), (self.width, 0), self.line_width)
        for i in range(self.grid_dimensions[1] - 1):
            y = self.y_increment * (i + 1)
            pygame.draw.line(self.surface, colour, (0, y), (self.width, y), self.line_width)
        pygame.draw.line(self.surface, colour, (0, self.height - self.line_width), (self.width, self.height - self.line_width), self.line_width)

    def map_click(self, point):
        # check for in bounds
        if point[0] <= self.x_bounds[0] or point[0] >= self.x_bounds[1] or point[1] <= self.y_bounds[0] or point[1] >= self.y_bounds[1]:
            return
        
        point = (point[0] - self.x_bounds[0], point[1] - self.y_bounds[0])
        index = map_to_index(*self.box_dims, *point)

        if self.map[index[0]][index[1]]:
            self.map[index[0]][index[1]] = False
        else:
            self.map[index[0]][index[1]] = True

    def close(self):
        return self.map

# arrow
class Arrow:
    def __init__(self, mid_length, inner_angle, dna):
        # position
        self.x = start_x
        self.y = start_y
        self.dead = False
        self.reached = False
        self.time_taken = None

        # angles
        self.inner_angle_left = inner_angle
        self.inner_angle_right = self.inner_angle_left + (360 - (2 * self.inner_angle_left))

        # points
        self.mid_length = mid_length
        self.inner_length = mid_length / 2
        self.top_x = self.x + self.mid_length
        self.top_y = self.y
        self.left_x = self.x + (self.inner_length * math.cos(get_radians(self.inner_angle_left)))
        self.left_y = self.y - (self.inner_length * math.sin(get_radians(self.inner_angle_left)))
        self.right_x = self.x + (self.inner_length * math.cos(get_radians(self.inner_angle_right)))
        self.right_y = self.y - (self.inner_length * math.sin(get_radians(self.inner_angle_right)))

        # velocity
        self.velocity = Vector(0,0)
        self.acceleration = Vector(0,0)
        self.max_velocity = Vector(6,6)

        # learner
        self.dna = dna

    def reset_movement(self):
        self.velocity = Vector(0,0)
        self.acceleration = Vector(0,0)
        self.x = start_x
        self.y = start_y
        self.dead = False
        self.reached = False
        self.time_taken = None

    def check_death(self, obstacles, current_frame):
        if not self.dead:
            if self.top_x <= 0 or self.top_x >= window_width or self.top_y <= 0 or self.top_y >= window_height:
                self.dead = True
                return

            if (goal_left <= self.top_x <= goal_right) and (goal_top <= self.top_y <= goal_bottom):
                self.reached = True
                self.time_taken = current_frame
                self.dead = True
                return

            for obstacle in obstacles:
                if obstacle.check_collision(self.top_x, self.top_y):
                    self.dead = True
                    break

    def update(self, current_frame):
        if not self.dead:
            # accelerate
            self.acceleration = self.dna.points[current_frame]
            self.velocity += self.acceleration

            # velocity limits
            if self.velocity.x > self.max_velocity.x and self.acceleration.x > 0:
                self.velocity.x = self.max_velocity.x

            if self.velocity.x < -1 * self.max_velocity.x and self.acceleration.x < 0:
                self.velocity.x = -1 * self.max_velocity.x

            if self.velocity.y > self.max_velocity.y and self.acceleration.y > 0:
                self.velocity.y = self.max_velocity.y

            if self.velocity.y < -1 * self.max_velocity.y and self.acceleration.y < 0:
                self.velocity.y = -1 * self.max_velocity.y

            velx = self.velocity.x
            vely = self.velocity.y

            # center
            self.x += velx
            self.y -= vely

            # get angle
            quadrant = get_quadrant(velx, vely)
            if velx == 0:
                angle = (math.pi / 2) if vely > 0 else -1 * (math.pi / 2)
            elif vely == 0:
                angle = 0 if velx > 0 else math.pi
            else:
                angle = math.atan(-vely/velx)
                if quadrant == 1:
                    angle = abs(angle)
                elif quadrant == 2:
                    angle = math.pi - abs(angle)
                elif quadrant == 3:
                    angle = math.pi + abs(angle)
                else:
                    angle = (2 * math.pi) - abs(angle)

            # update points
            self.top_x = self.x + (self.mid_length * math.cos(angle))
            self.top_y = self.y - (self.mid_length * math.sin(angle))
            self.left_x = self.x + (self.inner_length * math.cos(angle + get_radians(self.inner_angle_left)))
            self.left_y = self.y - (self.inner_length * math.sin(angle + get_radians(self.inner_angle_left)))
            self.right_x = self.x + (self.inner_length * math.cos(angle + get_radians(self.inner_angle_right)))
            self.right_y = self.y - (self.inner_length * math.sin(angle + get_radians(self.inner_angle_right)))

    def fitness(self):
        distance = euclidean_distance(self.top_x, self.top_y, goal_x, goal_y)
        return  1 - scale_distance(0, window_width, distance) if not self.reached else 1
    
    def left(self, integer = False):
        return (self.left_x, self.left_y) if not integer else int_tuple(self.left_x, self.left_y)

    def right(self, integer = False):
        return (self.right_x, self.right_y) if not integer else int_tuple(self.right_x, self.right_y)

    def center(self, integer = False):
        return (self.x, self.y) if not integer else int_tuple(self.x, self.y)

    def top(self, integer = False):
        return (self.top_x, self.top_y) if not integer else int_tuple(self.top_x, self.top_y)

    def poly_points(self):
        return [self.left(), self.center(), self.right(), self.top()]

# wall
class Wall:
    def __init__(self, width, height, x, y):
        self.height = height
        self.width = width
        self.x = x
        self.y = y
        self.pos = (x, y)

    def __str__(self):
        return "Wall([width = {}, height = {}, pos = ({}, {})])".format(self.width, self.height, self.x, self.y)

    def rect(self):
        return (self.x, self.y, self.width, self.height)

    def check_collision(self, x, y):
        return ((self.x <= x <= (self.x + self.width)) and (self.y <= y <= (self.y + self.height)))

# status display
class StatusBoard:
    # colours
    rect_colour = (90, 90, 90)
    text_colour = (240, 240, 210)
    increase_colour = (91, 255, 36)
    decrease_colour = (255, 69, 69)
    def __init__(self, max_time, population_size, width, font_size):
        # time & generation
        self.max_time = max_time
        self.current_frame = 1
        self.generation = 1

        # average fitness
        self.average_fitness = None
        self.delta_average_fitness = 0

        # fastest time
        self.fastest_time = None
        self.delta_fastest_time = 0

        # successful
        self.successful = 0
        self.delta_successful = 0

        # font & position
        self.font = pygame.font.SysFont('timesnewroman.ttf', font_size)
        self.x = 10
        self.y = 10
        self.w = width
        self.space_between_text = 4
        self.y_space = 8
        self.x_space = 8

        # measurements
        sample = self.font.render("sample", True, (0, 0, 0))
        sample = sample.get_rect()
        self.h = (sample.height * 4) + (self.space_between_text * 3) + (self.y_space * 2)
        self.single_height = sample.height
        del sample

    def reset(self):
        # time & generation
        self.current_frame = 1
        self.generation = 1

        # average fitness
        self.average_fitness = None
        self.delta_average_fitness = 0

        # fastest time
        self.fastest_time = None
        self.delta_fastest_time = 0

        # successful
        self.successful = 0
        self.delta_successful = 0

    def update(self, generation, average_fitness, fastest_time, successful):
        # generation
        self.generation = generation

        # average fitness
        self.delta_average_fitness = average_fitness - self.average_fitness if self.average_fitness != None else average_fitness
        self.average_fitness = average_fitness
        self.delta_average_fitness = round(self.delta_average_fitness, 4)
        self.average_fitness = round(self.average_fitness, 4)

        # fastest time
        self.delta_fastest_time = fastest_time - self.fastest_time if self.fastest_time != None else fastest_time
        self.fastest_time = fastest_time

        # successful
        self.delta_successful = successful - self.successful
        self.successful = successful

    def update_time(self, current_frame):
        # time
        self.current_frame = current_frame

    def render_objects(self):
        text_rects = []

        # surrounding rect
        surrounding = pygame.Rect(self.x, self.y, self.w, self.h)

        # time
        text = self.font.render("Time: {}/{}".format(str(self.current_frame).ljust(3), str(self.max_time).ljust(3)), True, self.text_colour)
        rect = text.get_rect()
        rect.x += self.x + self.x_space
        rect.y = self.y + self.y_space
        text_rects.append((text, rect))

        # generation
        text = self.font.render("Generation: {}".format(self.generation), True, self.text_colour)
        rect = text.get_rect()
        rect.x += self.x + self.x_space
        rect.y = self.y + self.space_between_text + self.single_height + self.y_space
        text_rects.append((text, rect))

        # average fitness
        sign = "+" if self.delta_average_fitness >= 0 else ""
        colour = self.increase_colour if sign == "+" else self.decrease_colour
        colour = self.text_colour if self.delta_average_fitness == 0 else colour
        text = self.font.render("Avg. Fitness: {} [{}]".format(self.average_fitness, str(sign) + str(self.delta_average_fitness)), True, colour)
        rect = text.get_rect()
        rect.x += self.x + self.x_space
        rect.y = self.y + (2 * self.space_between_text) + (2 * self.single_height) + self.y_space
        text_rects.append((text, rect))

        # successful
        sign = "+" if self.delta_successful >= 0 else ""
        colour = self.increase_colour if sign == "+" else self.decrease_colour
        colour = self.text_colour if self.delta_successful == 0 else colour
        text = self.font.render("Successful: {} [{}]".format(self.successful, str(sign) + str(self.delta_successful)), True, colour)
        rect = text.get_rect()
        rect.x += self.x + self.x_space
        rect.y = self.y + (3 * self.space_between_text) + (3 * self.single_height) + self.y_space
        text_rects.append((text, rect))

        return (surrounding, text_rects)

