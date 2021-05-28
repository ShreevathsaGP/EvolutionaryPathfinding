import pygame
import random
import math

pygame.init()

window_width = 1280
window_height = 720
window = pygame.display.set_mode((window_width, window_height))
colour = (255, 255, 255)

fps = 60
fps_clock = pygame.time.Clock()

# globals
running = True

class StatusBoard:
    # colours
    rect_colour = (90, 90, 90)
    text_colour = (240, 240, 210)
    def __init__(self, max_time, population_size, width, font_size):
        # time & generation
        self.max_time = max_time
        self.current_frame = 0
        self.generation = 0

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

    def set(self, current_frame, generation, average_fitness, fastest_time, successful):
        # time & generation
        self.current_frame = current_frame
        self.generation = generation
        
        # average fitness
        self.delta_average_fitness = average_fitness - self.average_fitness if self.average_fitness != None else average_fitness
        self.average_fitness = average_fitness

        # fastest time
        self.delta_fastest_time = fastest_time - self.fastest_time 
        self.fastest_time = fastest_time

        # successful
        self.delta_successful = successful - self.successful
        self.successful = successful

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
        sign = "+" if self.delta_average_fitness >= 0 else "-"
        text = self.font.render("Avg. Fitness: {} [{}]".format(self.average_fitness, str(sign) + str(self.delta_average_fitness)), True, self.text_colour)
        rect = text.get_rect()
        rect.x += self.x + self.x_space
        rect.y = self.y + (2 * self.space_between_text) + (2 * self.single_height) + self.y_space
        text_rects.append((text, rect))

        # successful
        sign = "+" if self.delta_successful >= 0 else "-"
        text = self.font.render("Successful: {} [{}]".format(self.successful, str(sign) + str(self.delta_successful)), True, self.text_colour)
        rect = text.get_rect()
        rect.x += self.x + self.x_space
        rect.y = self.y + (3 * self.space_between_text) + (3 * self.single_height) + self.y_space
        text_rects.append((text, rect))

        return (surrounding, text_rects)


sample_board = StatusBoard(500, 500, 300, 18)

# main loop
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    window.fill((0,0,0))

    render_objects = sample_board.render_objects()
    pygame.draw.rect(window, sample_board.rect_colour, render_objects[0])
    for pair in render_objects[1]:
        window.blit(pair[0], pair[1])

    pygame.display.update()
    fps_clock.tick(fps)

pygame.quit()
