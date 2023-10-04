import pyautogui as pya
import time 

def get_mouse_position(interval:int=1):
    try:
        while True:
            x, y = pya.position()
            print(f"x:{x}, y:{y}")
            time.sleep(interval)
    except KeyboardInterrupt:
        print("Exit")

if __name__ == "__main__":
    get_mouse_position()