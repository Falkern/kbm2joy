import pyautogui
import vgamepad as vg
import tkinter as tk
from tkinter import ttk
import threading
import time

gamepad = vg.VX360Gamepad()

sensitivity_x = 1.0
sensitivity_y = 1.0
deadzone_x = 0.1
deadzone_y = 0.1
emulation_active = False

root = tk.Tk()
root.title("Mouse to Joystick Converter")
root.geometry("400x300")
root.resizable(False, False)

def apply_deadzone(value, deadzone):
    return 0 if abs(value) < deadzone else value

def map_mouse_to_joystick():
    global emulation_active
    screen_width, screen_height = pyautogui.size()
    center_x, center_y = screen_width / 2, screen_height / 2

    pyautogui.moveTo(center_x, center_y)

    while emulation_active:
        mouse_x, mouse_y = pyautogui.position()
        dx = (mouse_x - center_x) / (screen_width / 2)
        dy = (mouse_y - center_y) / (screen_height / 2)

        dx = apply_deadzone(dx, deadzone_x) * sensitivity_x
        dy = apply_deadzone(dy, deadzone_y) * sensitivity_y

        joy_x = int(dx * 32767)
        joy_y = int(dy * 32767)

        gamepad.left_joystick(x_value=joy_x, y_value=-joy_y)
        gamepad.update()

        pyautogui.moveTo(center_x, center_y)
        time.sleep(0.01)

def toggle_emulation():
    global emulation_active
    emulation_active = not emulation_active

    if emulation_active:
        start_button.config(text="Stop Emulation")
        threading.Thread(target=map_mouse_to_joystick, daemon=True).start()
    else:
        start_button.config(text="Start Emulation")
        gamepad.reset()
        gamepad.update()

def update_sensitivity_x(value):
    global sensitivity_x
    sensitivity_x = float(value)

def update_sensitivity_y(value):
    global sensitivity_y
    sensitivity_y = float(value)

def update_deadzone_x(value):
    global deadzone_x
    deadzone_x = float(value)

def update_deadzone_y(value):
    global deadzone_y
    deadzone_y = float(value)

ttk.Label(root, text="Sensitivity X").pack()
sensitivity_x_slider = ttk.Scale(root, from_=0.1, to=2.0, orient="horizontal", command=update_sensitivity_x)
sensitivity_x_slider.set(sensitivity_x)
sensitivity_x_slider.pack()

ttk.Label(root, text="Sensitivity Y").pack()
sensitivity_y_slider = ttk.Scale(root, from_=0.1, to=2.0, orient="horizontal", command=update_sensitivity_y)
sensitivity_y_slider.set(sensitivity_y)
sensitivity_y_slider.pack()

ttk.Label(root, text="Deadzone X").pack()
deadzone_x_slider = ttk.Scale(root, from_=0.0, to=0.5, orient="horizontal", command=update_deadzone_x)
deadzone_x_slider.set(deadzone_x)
deadzone_x_slider.pack()

ttk.Label(root, text="Deadzone Y").pack()
deadzone_y_slider = ttk.Scale(root, from_=0.0, to=0.5, orient="horizontal", command=update_deadzone_y)
deadzone_y_slider.set(deadzone_y)
deadzone_y_slider.pack()

start_button = ttk.Button(root, text="Start Emulation", command=toggle_emulation)
start_button.pack(pady=20)

root.mainloop()
