# globy.py

import sys
import math
import random

# constants
window_width = 1280
window_height = 720
goal_x = window_width - 50
goal_y = window_height / 2
goal_radius = 25
goal_left = goal_x - goal_radius
goal_right = goal_x + goal_radius
goal_bottom = goal_y + goal_radius
goal_top = goal_y - goal_radius
start_x = 40
start_y = window_height / 2

# map list index
def map_to_index(x1, y1, x2, y2):
    return (int(x2 / x1), int(y2 / y1))

# radians conversion
def get_radians(degrees):
    return degrees * (math.pi/180)

# degrees conversion
def get_degrees(radians):
    return radians * (180/math.pi)

# integer tuple
def int_tuple(a, b):
    return (int(a), int(b))

# quadrant of point
def get_quadrant(x, y):
    if x < 0:
        if y < 0:
            return 3
        else:
            return 2
    else:
        if  y < 0:
            return 4
        else:
            return 1

# euclidean distance
def euclidean_distance(x1, y1, x2, y2):
    return math.sqrt( (math.pow(y2 - y1, 2) + math.pow(x2 - x1, 2)) )

# scale distance [0, 1]
def scale_distance(min_distance, max_distance, distance):
    return (distance - min_distance) / max_distance

# vector [ 2D ]
class Vector:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return ((self.x == other.x) and (self.y == other.y))

    def __str__(self):
        return "Vector({}, {})".format(self.x, self.y)
        
    def __add__(self, other):
        x = self.x + other.x
        y = self.y + other.y

        return Vector(x, y)

    def __mul__(self, scalar):
        x = self.x * scalar
        y = self.y * scalar

        return Vector(x, y)
    
    def __rmul__(self, scalar):
        x = self.x * scalar
        y = self.y * scalar

        return Vector(x, y)

    def __truediv__(self, scalar):
        x = self.x / scalar
        y = self.x / scalar

        return Vector(x, y)

    def __floordiv__(self, scalar):
        x = self.x // scalar
        y = self.y // scalar

        return Vector(x, y)


