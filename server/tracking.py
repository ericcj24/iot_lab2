from collections import namedtuple
import math
import time
class State():
    def __init__(self, state, x, y) -> None:
        self.orientation = state
        self.x = x
        self.y = y

driveCommand = namedtuple('Command', ['orientation', 'direction', 'distance'])

class StateTracker():
    def __init__(self) -> None:
        self.state = State('Forward', 0, 0) # X is horizontal, Y is Vertical axis
        self.car_turn_length = 44
        self.car_turn_forward_length = 16
        self.forward_length = 22
    
    def update_state_position(self, direction: str):
        new_orientation = self.state.orientation
        new_x = self.state.x
        new_y = self.state.y
        if (self.state.orientation == 'Forward'):
            if direction == 'Forward':
                new_y += self.forward_length
            elif direction == 'Backward':
                new_y -= self.forward_length
            elif direction == 'Left':
                new_y += self.car_turn_forward_length
                new_x -= self.car_turn_length
                new_orientation = 'Left'
            elif direction == 'Right':
                new_y += self.car_turn_forward_length
                new_x += self.car_turn_length
                new_orientation = 'Right'
        elif self.state.orientation == 'Backward':
            if direction == 'Forward':
                new_y -= self.forward_length
            elif direction == 'Backward':
                new_y += self.forward_length
            elif direction == 'Left':
                new_y -= self.car_turn_forward_length
                new_x += self.car_turn_length
                new_orientation = 'Right'
            elif direction == 'Right':
                new_y -= self.car_turn_forward_length
                new_x -= self.car_turn_length
                new_orientation = 'Left'
        elif self.state.orientation == 'Left':
            if direction == 'Forward':
                new_x -= self.forward_length
            elif direction == 'Backward':
                new_x += self.forward_length
            elif direction == 'Left':
                new_x -= self.car_turn_forward_length
                new_y -= self.car_turn_length
                new_orientation = 'Backward'
            elif direction == 'Right':
                new_x -= self.car_turn_forward_length
                new_y += self.car_turn_length
                new_orientation = 'Forward'
        elif self.state.orientation == 'Right':
            if direction == 'Forward':
                new_x += self.forward_length
            elif direction == 'Backward':
                new_x -= self.forward_length
            elif direction == 'Left':
                new_x += self.car_turn_forward_length
                new_y += self.car_turn_length
                new_orientation = 'Forward'
            elif direction == 'Right':
                new_x += self.car_turn_forward_length
                new_y -= self.car_turn_length
                new_orientation = 'Backward'  
        self.state.orientation = new_orientation
        self.state.x = new_x
        self.state.y = new_y
    
    def get_distance_traveled(self):
        return str(round(math.sqrt(self.state.x**2 + self.state.y**2), 2)) + ' CM'