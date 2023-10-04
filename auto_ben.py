import pyautogui as pya
import logging
import queue
import time
import os
import datetime

SLEEP_TIME = 1

CHANGE_CONSTANT = 0.5

COMMAND_LIST = [
    ("SINE", None),
    ("AMPLITUDE_UP", 0),
    ("FREQUENCY_UP", 2),
    ("RECORD_TIME", None),
    ("WAIT", 1),
    ("LL", None),
    ("RECORD_TIME", None),
    ("WAIT", 1),
    ("V1", None),
    ("RECORD_TIME", None),
    ("WAIT", 1),
    ("RA", None),
    ("AMPLITUDE_UP", 2),
    ("RECORD_TIME",None),
]

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
        if self.name == "RECORD_TIME":
            print("Recording time")
            logging.info("Recording time")
        elif self.name == "WAIT":
            print(f"Sleeping for {SLEEP_TIME}")
            logging.info(f"Sleeping for {SLEEP_TIME}")
            time.sleep(SLEEP_TIME)
        else:
            button_press = self.change/CHANGE_CONSTANT if self.change else 1
            location = LOCATIONS.get(self.name, None)
            if location is not None:
                for _ in range(int(button_press)):
                    # pya.click(location)
                    print(f"Going to {location}")
                    logging.info(f"Going to {location}")

def print_queue(queue):
    while not queue.empty():
        print(queue.get().name)

def initialize_queue():
    command_queue = queue.Queue()
    for name, change in COMMAND_LIST:
        command_queue.put(Command(name, change))
    return command_queue

def initialize_logs():
    desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
    logs_folder_path = os.path.join(desktop_path, "logs")
    if not os.path.exists(logs_folder_path):
        os.makedirs(logs_folder_path)
    current_time = datetime.datetime.now()
    timestamp_str = current_time.strftime("%Y-%m-%d_%H-%M-%S")
    return os.path.join(logs_folder_path, f"log_{timestamp_str}.log")

def main():
    logging.basicConfig(
        filename=initialize_logs(), 
        level=logging.INFO, 
        format='%(asctime)s - %(message)s'
    )
    command_queue = initialize_queue()
    while not command_queue.empty():
        command_queue.get().execute()

if __name__ == "__main__":
    main()