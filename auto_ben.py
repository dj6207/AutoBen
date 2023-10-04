import pyautogui as pya
import logging
import queue
import time
import os
import datetime

CHANGE_CONSTANT = 0.5
FREQUENCY = 0 # 0Hz
AMPLITUDE  = 0 # 0mV

COMMAND_LIST = [
    ("SINE", None),
    ("RA", None),
    ("AMPLITUDE_UP", 0), # 0mV
    ("FREQUENCY_UP", 2), # 0Hz - 2Hz
    ("RECORD_TIME", None),
    # ("WAIT", 60),
    ("WAIT", 1),
    ("LL", None),
    ("RECORD_TIME", None),
    ("WAIT", 1),
    ("V1", None),
    ("RECORD_TIME", None),
    ("WAIT", 1),
    ("RA", None),
    ("AMPLITUDE_UP", 2), # 0mV - 2mV

    ("RECORD_TIME",None),
    ("WAIT", 1),
    ("LL", None),
    ("RECORD_TIME",None),
    ("WAIT", 1),
    ("V1", None),
    ("RECORD_TIME",None),
    ("WAIT", 1),
    ("RA", None),

    ("FREQUENCY_UP", 10), # 2Hz - 10Hz
    ("RECORD_TIME",None),

    ("WAIT", 1),
    ("LL", None),
    ("RECORD_TIME",None),
    ("WAIT", 1),
    ("V1", None),
    ("RECORD_TIME",None),
    ("WAIT", 1),
    ("RA", None),

    ("FREQUENCY_DOWN", 5), # 10Hz - 5Hz
    ("WAIT", 1),
    ("PACING_AMPLITUDE_UP", 2),
    ("RECORD_TIME",None),
]

LOCATIONS = {
    "SINE": (10, 10),
    "RA": (10, 10),
    "AMPLITUDE_UP": (10, 10),
    "AMPLITUDE_DOWN": (10, 10),
    "PACING_AMPLITUDE_UP": (10, 10),
    "PACING_AMPLITUDE_DOWN": (10, 10),
    "FREQUENCY_UP": (10, 10),
    "FREQUENCY_DOWN": (10, 10),
    "LL": (10, 10),
    "V1":(10, 10),
}

class Command:
    def __init__(self, name, change):
        self.name = name
        self.change = change

    def execute(self, current_frequency, current_amplitude, current_pacing_amplitude):
        if self.name == "RECORD_TIME":
            print("Recording time")
            logging.info("Recording time")
        elif self.name == "WAIT":
            print(f"Sleeping for {self.change}")
            logging.info(f"Sleeping for {self.change}")
            time.sleep(self.change)
        else:
            button_press = 1
            if self.name.split("_")[0] == "AMPLITUDE":
                button_press = abs((self.change - current_amplitude))/CHANGE_CONSTANT if self.change else 1
                current_amplitude = self.change if self.change else current_amplitude
            elif self.name.split("_")[0] == "FREQUENCY":
                button_press = abs((self.change - current_frequency))/CHANGE_CONSTANT if self.change else 1
                current_frequency = self.change if self.change else current_frequency
            else:
                button_press = abs((self.change - current_pacing_amplitude))/CHANGE_CONSTANT if self.change else 1
                current_pacing_amplitude = self.change if self.change else current_pacing_amplitude
            location = LOCATIONS.get(self.name, None)
            if location is not None:
                for _ in range(int(button_press)):
                    pya.click(location)
                    print(f"Clicking {self.name} at {location}")
                    logging.info(f"Clicking {self.name} at {location}")
        return current_frequency, current_amplitude, current_pacing_amplitude

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
    timestamp_str = datetime.datetime.now().strftime("%m-%d-%Y_%H.%M.%S")
    return os.path.join(logs_folder_path, f"{timestamp_str}.log")

def main():
    frequency = 0
    amplitude = 0
    pacing_amplitude = 0
    logging.basicConfig(
        filename=initialize_logs(), 
        level=logging.INFO, 
        format='%(asctime)s: %(message)s',
        datefmt="%m-%d-%Y %H.%M.%S"
    )
    command_queue = initialize_queue()
    while not command_queue.empty():
        frequency, amplitude, pacing_amplitude = command_queue.get().execute(frequency, amplitude, pacing_amplitude)
        logging.info(f"Frequency: {frequency}, Amplitude: {amplitude}, Pacing Amplitude: {pacing_amplitude}")

if __name__ == "__main__":
    main()