# game.py

# constants
window_width = 800
window_height = 500
velocity = 10

class Car:
    height = window_height / 15
    width = height
    def __init__(self):
        self.x = 10
        self.y = (window_height / 2) - (self.height / 2)

    def set_coords(self, x, y):
        self.x = x
        self.y = y
    
    def left(self):
        pass

    def right(self):
        pass

    def up(self):
        pass

    def down(self):
        pass

car = Car()

