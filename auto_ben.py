import pyautogui as pya
import logging
import queue

# Clicking - Hashmap with all the known locations 
# The name of the location will be the keys and the location in x, y coordinates will be the values
# Wrapper function that returns the coordinates of the location name
# Queue that will queue up the list of commands
# Class for commands
# Writing the recorded time into a file

CHANGE_CONSTANT = 0.5

LOCATIONS = {
    "SINE": (0, 0),
    "RA": (0, 0),
    "AMPLITUDE_UP": (0, 0),
    "AMPLITUDE_DOWN": (0, 0),
    "FREQUENCY_UP": (0, 0),
    "FREQUENCY_DOWN": (0, 0),
    "LL": (0, 0),
    "V1":(0, 0),
}

class Command:
    def __init__(self, name, change):
        self.name = name
        self.change = change

    def execute(self):
        button_press = self.change/CHANGE_CONSTANT
        location = LOCATIONS.get(self.name, None)
        if location is not None:
            for _ in button_press:
                pya.click(location)

def initialize_queue():
    
    return

def main():
    initialize_queue()

if __name__ == "__main__":
    main()