import pyautogui
import time
import threading
from pynput import mouse
import keyboard
import configparser


print("\n███    ███  █████  ██████  ███████     ██████  ██    ██     ██████   █████  ███    ███ ██       ██████  ██    ██ \n████  ████ ██   ██ ██   ██ ██          ██   ██  ██  ██      ██   ██ ██   ██ ████  ████ ██      ██    ██ ██    ██ \n██ ████ ██ ███████ ██   ██ █████       ██████    ████       ██████  ███████ ██ ████ ██ ██      ██    ██ ██    ██ \n██  ██  ██ ██   ██ ██   ██ ██          ██   ██    ██        ██   ██ ██   ██ ██  ██  ██ ██      ██    ██  ██  ██  \n██      ██ ██   ██ ██████  ███████     ██████     ██        ██   ██ ██   ██ ██      ██ ███████  ██████    ████   ")

print("                                  https://github.com/Ramlov")

run_again = True
first_run = True
x_positions = []
y_positions = []

craft = ""
stacks = 0

def on_mouse_press(x, y, button, pressed):
    if pressed:
        x_positions.append(x)
        y_positions.append(y)
        print(f"Cursor location: x={x}, y={y}")
        print(x_positions)
        if len(x_positions) == 3:
            return False

def save_cursor_location():
    with mouse.Listener(on_click=on_mouse_press) as listener:
        print("Press the mouse button to save cursor location.\n 1. Press the text field. \n 2. Press the recipe. \n 3. Press the product.")

        listener.join()
    config = configparser.ConfigParser()
    config['CursorLocations'] = {'x1': str(x_positions[0]), 'y1': str(y_positions[0]),
                                 'x2': str(x_positions[1]), 'y2': str(y_positions[1]),
                                 'x3': str(x_positions[2]), 'y3': str(y_positions[2])}
    config['Inputs'] = {'craft': str(craft), 'stacks': int(stacks)}

    with open('config.ini', 'w') as configfile:
        config.write(configfile)

    print("Cursor locations saved to config.ini.")

if input("Configure? (T/F)") == "T":
    craft = input("What do you want to craft? ")
    stacks = input("How many stacks? (INT)")
    save_cursor_location()

config = configparser.ConfigParser()
config.read('config.ini')


x_positions = [
    int(config['CursorLocations']['x1']),
    int(config['CursorLocations']['x2']),
    int(config['CursorLocations']['x3'])
]

y_positions = [
    int(config['CursorLocations']['y1']),
    int(config['CursorLocations']['y2']),
    int(config['CursorLocations']['y3'])
]

craft = config['Inputs']['craft']
stacks = int(config['Inputs']['stacks'])




while run_again:
    if first_run:
        first_run = False
        input("Set inventory up now! \n Ready (Write when ready)? ")
        x_text, y_text = x_positions[0], y_positions[0]

        pyautogui.moveTo(x_text, y_text)
        pyautogui.click()

        time.sleep(0.5)
        pyautogui.typewrite(craft)

    def move_cursor():
        x_start, y_start = x_positions[1], y_positions[1]
        x_end, y_end = x_positions[2], y_positions[2]
        interval = 0.1

        for i in range(int(stacks)):
            pyautogui.moveTo(x_start, y_start)
            pyautogui.mouseDown()
            pyautogui.mouseUp()
            pyautogui.moveTo(x_end, y_end)
            pyautogui.mouseDown()
            pyautogui.mouseUp()

            time.sleep(interval)

    def activate_shift():
        while cursor_thread.is_alive():
            keyboard.press("shift")
            time.sleep(0.05)

    cursor_thread = threading.Thread(target=move_cursor)
    shift_thread = threading.Thread(target=activate_shift)

    cursor_thread.start()
    shift_thread.start()

    cursor_thread.join()
    shift_thread.join()

    answer = input("Run again? (Y/N): ")
    if answer.lower() not in ["y", "yes"]:
        run_again = False
