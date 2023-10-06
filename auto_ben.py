import pyautogui as pya
import logging
import queue
import time
import os
import datetime
import winsound

VERSION = 1.0

# How much 
CHANGE_AMPLITUDE_CONSTANT = 0.1
CHANGE_PACING_AMPLITUDE_CONSTANT = 2
WAIT_TIME = 1
START_DELAY = 1

COMMAND_LIST = [
    ("SINE", None),
    ("AMPLITUDE_DOWN", 0), # 0mV
    ("FREQUENCY_UP", 2), # 0Hz - 2Hz
    ("RECORD_TIME", None),
    ("WAIT", WAIT_TIME),
    ("RA", None),
    ("LL", None),
    ("RECORD_TIME", None),
    ("WAIT", WAIT_TIME),
    ("LL", None),
    ("V1", None),
    ("RECORD_TIME", None),
    ("WAIT", WAIT_TIME),
    ("V1", None),
    ("RA", None),
    ("AMPLITUDE_UP", 2), # 0mV - 2mV

    ("RECORD_TIME",None),
    ("WAIT", WAIT_TIME),
    ("RA", None),
    ("LL", None),
    ("RECORD_TIME",None),
    ("WAIT", WAIT_TIME),
    ("LL", None),
    ("V1", None),
    ("RECORD_TIME",None),
    ("WAIT", WAIT_TIME),
    ("V1", None),
    ("RA", None),

    ("FREQUENCY_UP", 10), # 2Hz - 10Hz
    ("RECORD_TIME",None),

    ("WAIT", WAIT_TIME),
    ("RA", None),
    ("LL", None),
    ("RECORD_TIME",None),
    ("WAIT", WAIT_TIME),
    ("LL", None),
    ("V1", None),
    ("RECORD_TIME",None),
    ("WAIT", WAIT_TIME),
    ("V1", None),
    ("RA", None),

    ("FREQUENCY_DOWN", 5), # 10Hz - 5Hz
    ("WAIT", WAIT_TIME),
    ("PACING_AMPLITUDE_UP", 2),

    ("RECORD_TIME",None),
    ("WAIT", WAIT_TIME),
    ("RA", None),
    ("LL", None),
    ("RECORD_TIME",None),
    ("WAIT", WAIT_TIME),
    ("LL", None),
    ("V1", None),
    ("RECORD_TIME",None),
    ("WAIT", WAIT_TIME),
    ("V1", None),
    ("RA", None),
]

LOCATIONS = {
    "SINE": (457, 217),
    "RA": (955, 189),
    "AMPLITUDE_UP": (709, 204),
    "AMPLITUDE_DOWN": (708, 219),
    "PACING_AMPLITUDE_UP": (869, 486),
    "PACING_AMPLITUDE_DOWN": (870, 501),
    "FREQUENCY_UP": (706, 264),
    "FREQUENCY_DOWN": (707, 281),
    "LL": (950, 234),
    "V1":(953, 260),
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
            # Amplitude starts a 1mV and changesby 0.1
            if self.name.split("_")[0] == "AMPLITUDE":
                button_press = abs((self.change - current_amplitude))/CHANGE_AMPLITUDE_CONSTANT if self.change is not None else 1
                current_amplitude = self.change if self.change is not None else current_amplitude
            # Frequency starts at 1Hz and changes by 1
            elif self.name.split("_")[0] == "FREQUENCY":
                button_press = abs((self.change - current_frequency)) if self.change is not None else 1
                current_frequency = self.change if self.change is not None else current_frequency
            # Pacing amplitude starts at 0 and changes by 2
            else:
                button_press = abs((self.change - current_pacing_amplitude))/CHANGE_PACING_AMPLITUDE_CONSTANT if self.change is not None else 1
                current_pacing_amplitude = self.change if self.change is not None else current_pacing_amplitude
            location = LOCATIONS.get(self.name, None)
            if location is not None:
                logging.info(f"Pressed {int(button_press)} times")
                for _ in range(int(button_press)):
                    pya.click(location)
                    print(f"Clicking {self.name} at {location}")
                    logging.info(f"Clicking {self.name} at {location}")
        return current_frequency, current_amplitude, current_pacing_amplitude

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
    frequency = 1
    amplitude = 1
    pacing_amplitude = 0
    logging.basicConfig(
        filename=initialize_logs(), 
        level=logging.INFO, 
        format='%(asctime)s: %(message)s',
        datefmt="%m-%d-%Y %H.%M.%S"
    )
    command_queue = initialize_queue()
    print(f"Auto_Ben Version {VERSION}")
    logging.info(f"Auto_Ben Version {VERSION}")
    print(f"Script will Start in {START_DELAY} Seconds")
    time.sleep(START_DELAY)
    while not command_queue.empty():
        frequency, amplitude, pacing_amplitude = command_queue.get().execute(frequency, amplitude, pacing_amplitude)
        logging.info(f"Frequency: {frequency}, Amplitude: {amplitude}, Pacing Amplitude: {pacing_amplitude}")
    winsound.PlaySound("sound.wav", winsound.SND_FILENAME)

if __name__ == "__main__":
    main()