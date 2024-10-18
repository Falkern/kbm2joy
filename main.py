import tkinter as tk
from tkinter import messagebox
from pynput import mouse
import time
import json
import os
import threading
import pyautogui  # Ensure you install this with pip
import ttkbootstrap as ttkb
from ttkbootstrap import Style  # Change this line

class Tooltip:
    def __init__(self, widget, text):
        self.widget = widget
        self.text = text
        self.tooltip_window = None
        self.widget.bind("<Enter>", self.show_tooltip)
        self.widget.bind("<Leave>", self.hide_tooltip)

    def show_tooltip(self, event=None):
        if self.tooltip_window is not None:
            return
        x = self.widget.winfo_rootx() + 20
        y = self.widget.winfo_rooty() + 20
        self.tooltip_window = ttkb.Toplevel(self.widget)
        self.tooltip_window.wm_overrideredirect(True)
        self.tooltip_window.wm_geometry(f"+{x}+{y}")
        label = ttkb.Label(self.tooltip_window, text=self.text, bootstyle="light")
        label.pack()

    def hide_tooltip(self, event=None):
        if self.tooltip_window:
            self.tooltip_window.destroy()
            self.tooltip_window = None

class MacroRecorder:
    def __init__(self):
        self.macros = []
        self.recording = False

    def on_click(self, x, y, button, pressed):
        if self.recording:
            action = 'Pressed' if pressed else 'Released'
            self.macros.append((time.time(), action, (x, y), str(button)))

    def start_recording(self):
        self.recording = True
        self.macros.clear()
        self.listener = mouse.Listener(on_click=self.on_click)
        self.listener.start()  # Start the listener in a non-blocking way

    def stop_recording(self):
        self.recording = False
        self.listener.stop()  # Stop the listener

    def play_macros(self):
        threading.Thread(target=self._play_macros).start()  # Play in a separate thread

    def _play_macros(self):
        start_time = time.time()
        for timestamp, action, position, button in self.macros:
            time.sleep(timestamp - (time.time() - start_time))  # Correct timing
            if action == 'Pressed':
                pyautogui.click(*position)  # Simulate click at the recorded position
                print(f"{action} at {position} with {button}")
            elif action == 'Released':
                print(f"{action} at {position} with {button}")

    def edit_macro(self, index, new_macro):
        if 0 <= index < len(self.macros):
            self.macros[index] = new_macro

class App:
    def __init__(self, root):
        self.root = root
        
        # Set dark theme
        self.style = Style(theme='darkly')  # Set the dark theme here
        self.root.title("Mouse Macro")
        self.root.geometry("600x600")
        self.profiles_dir = "profiles"
        os.makedirs(self.profiles_dir, exist_ok=True)

        self.macro_recorder = MacroRecorder()
        self.selected_button = None

        # Create Notebook (Tabs)
        self.notebook = ttkb.Notebook(self.root)
        self.notebook.pack(expand=True, fill="both")

        self.macro_tab = ttkb.Frame(self.notebook)
        self.profile_tab = ttkb.Frame(self.notebook)

        self.notebook.add(self.macro_tab, text="Macros")
        self.notebook.add(self.profile_tab, text="Profiles")

        self.setup_macro_tab()
        self.setup_profile_tab()

    def setup_macro_tab(self):
        macro_frame = ttkb.Frame(self.macro_tab)
        macro_frame.pack(pady=20, padx=20, fill="both", expand=True)

        self.record_button = ttkb.Button(macro_frame, text="Record Macro", command=self.record_macro, bootstyle="success")
        Tooltip(self.record_button, "Click to start recording macros.")
        self.record_button.pack(pady=10, fill='x')

        self.stop_button = ttkb.Button(macro_frame, text="Stop Recording", command=self.stop_recording, bootstyle="danger", state="disabled")
        Tooltip(self.stop_button, "Click to stop recording macros.")
        self.stop_button.pack(pady=10, fill='x')

        self.play_button = ttkb.Button(macro_frame, text="Play Macros", command=self.play_macro, bootstyle="primary")
        Tooltip(self.play_button, "Click to play the recorded macros.")
        self.play_button.pack(pady=10, fill='x')

        self.macro_listbox = tk.Text(macro_frame, height=10, bg="#2c2c2c", fg="white")
        self.macro_listbox.pack(pady=10, fill='x')

        self.edit_macro_entry = ttkb.Entry(macro_frame)
        self.edit_macro_entry.insert(0, "Edit Selected Macro")  # Add placeholder text
        self.edit_macro_entry.bind("<FocusIn>", self.on_entry_click)
        self.edit_macro_entry.bind("<FocusOut>", self.on_focusout)
        self.edit_macro_entry.pack(pady=10, fill='x')

        self.edit_macro_button = ttkb.Button(macro_frame, text="Edit Selected Macro", command=self.edit_macro, bootstyle="primary")
        Tooltip(self.edit_macro_button, "Click to edit the selected macro.")
        self.edit_macro_button.pack(pady=10, fill='x')

        self.clear_button = ttkb.Button(macro_frame, text="Clear Macros", command=self.clear_macros, bootstyle="danger")
        Tooltip(self.clear_button, "Click to clear all recorded macros.")
        self.clear_button.pack(pady=10, fill='x')

        self.move_up_button = ttkb.Button(macro_frame, text="Move Up", command=self.move_macro_up, bootstyle="warning")
        Tooltip(self.move_up_button, "Move the selected macro up.")
        self.move_up_button.pack(pady=5, fill='x')

        self.move_down_button = ttkb.Button(macro_frame, text="Move Down", command=self.move_macro_down, bootstyle="warning")
        Tooltip(self.move_down_button, "Move the selected macro down.")
        Tooltip(self.move_down_button, "Move the selected macro down.")
        self.move_down_button.pack(pady=5, fill='x')

    def setup_profile_tab(self):
        profile_frame = ttkb.Frame(self.profile_tab)
        profile_frame.pack(pady=20, padx=20, fill="both", expand=True)

        self.profile_name_entry = ttkb.Entry(profile_frame)
        self.profile_name_entry.insert(0, "Profile Name")
        self.profile_name_entry.bind("<FocusIn>", self.on_profile_entry_click)
        self.profile_name_entry.bind("<FocusOut>", self.on_profile_focusout)
        self.profile_name_entry.pack(pady=10, fill='x')

        self.save_profile_button = ttkb.Button(profile_frame, text="Save Profile", command=self.save_profile, bootstyle="success")
        Tooltip(self.save_profile_button, "Click to save the current macros as a profile.")
        self.save_profile_button.pack(pady=10, fill='x')

        self.load_profile_button = ttkb.Button(profile_frame, text="Load Profile", command=self.load_profile, bootstyle="primary")
        Tooltip(self.load_profile_button, "Click to load a previously saved profile.")
        self.load_profile_button.pack(pady=10, fill='x')

        self.delete_profile_button = ttkb.Button(profile_frame, text="Delete Profile", command=self.delete_profile, bootstyle="danger")
        Tooltip(self.delete_profile_button, "Click to delete the selected profile.")
        self.delete_profile_button.pack(pady=10, fill='x')

        self.profile_listbox = tk.Text(profile_frame, height=10, bg="#2c2c2c", fg="white")
        self.profile_listbox.pack(pady=10, fill='x')

        self.update_profile_list()

        # Button Customization
        self.button_customization_label = ttkb.Label(profile_frame, text="Customize Mouse Button:", bootstyle="light")
        self.button_customization_label.pack(pady=10, fill='x')

        self.button_dropdown = ttkb.Combobox(profile_frame, values=["Left", "Right", "Middle"], bootstyle="primary")
        self.button_dropdown.pack(pady=10, fill='x')

        self.assign_macro_button = ttkb.Button(profile_frame, text="Assign Macro", command=self.assign_macro, bootstyle="primary")
        Tooltip(self.assign_macro_button, "Click to assign the selected macro to the chosen mouse button.")
        self.assign_macro_button.pack(pady=10, fill='x')

    def on_entry_click(self, event):
        if self.edit_macro_entry.get() == "Edit Selected Macro":
            self.edit_macro_entry.delete(0, tk.END)  # Clear placeholder text

    def on_focusout(self, event):
        if not self.edit_macro_entry.get():
            self.edit_macro_entry.insert(0, "Edit Selected Macro")  # Add placeholder text if empty

    def on_profile_entry_click(self, event):
        if self.profile_name_entry.get() == "Profile Name":
            self.profile_name_entry.delete(0, tk.END)  # Clear placeholder text

    def on_profile_focusout(self, event):
        if not self.profile_name_entry.get():
            self.profile_name_entry.insert(0, "Profile Name")  # Add placeholder text if empty

    def record_macro(self):
        self.macro_recorder.start_recording()
        self.record_button.config(state="disabled")
        self.stop_button.config(state="normal")

    def stop_recording(self):
        self.macro_recorder.stop_recording()
        self.record_button.config(state="normal")
        self.stop_button.config(state="disabled")

    def play_macro(self):
        self.macro_recorder.play_macros()

    def edit_macro(self):
        selected_index = self.macro_listbox.index("insert")  # Get selected index
        if selected_index < 0:
            messagebox.showwarning("Warning", "No macro selected.")
            return

        new_macro = self.edit_macro_entry.get()
        if new_macro:
            self.macro_recorder.edit_macro(selected_index, new_macro)

    def clear_macros(self):
        self.macro_recorder.macros.clear()
        self.update_macro_listbox()

    def move_macro_up(self):
        selected_index = self.macro_listbox.index("insert")  # Get selected index
        if selected_index > 0:
            self.macro_recorder.macros[selected_index], self.macro_recorder.macros[selected_index - 1] = \
                self.macro_recorder.macros[selected_index - 1], self.macro_recorder.macros[selected_index]
            self.update_macro_listbox()

    def move_macro_down(self):
        selected_index = self.macro_listbox.index("insert")  # Get selected index
        if selected_index < len(self.macro_recorder.macros) - 1:
            self.macro_recorder.macros[selected_index], self.macro_recorder.macros[selected_index + 1] = \
                self.macro_recorder.macros[selected_index + 1], self.macro_recorder.macros[selected_index]
            self.update_macro_listbox()

    def update_macro_listbox(self):
        self.macro_listbox.delete('1.0', tk.END)
        for timestamp, action, position, button in self.macro_recorder.macros:
            self.macro_listbox.insert(tk.END, f"{action} at {position} with {button}\n")

    def save_profile(self):
        profile_name = self.profile_name_entry.get()
        if profile_name == "Profile Name":
            messagebox.showwarning("Warning", "Profile name cannot be empty.")
            return

        profile_path = os.path.join(self.profiles_dir, f"{profile_name}.json")
        with open(profile_path, 'w') as f:
            json.dump(self.macro_recorder.macros, f)
        self.update_profile_list()

    def load_profile(self):
        profile_name = self.profile_name_entry.get()
        profile_path = os.path.join(self.profiles_dir, f"{profile_name}.json")
        if not os.path.exists(profile_path):
            messagebox.showwarning("Warning", "Profile does not exist.")
            return

        with open(profile_path, 'r') as f:
            self.macro_recorder.macros = json.load(f)
        self.update_macro_listbox()

    def delete_profile(self):
        profile_name = self.profile_name_entry.get()
        profile_path = os.path.join(self.profiles_dir, f"{profile_name}.json")
        if os.path.exists(profile_path):
            os.remove(profile_path)
            self.update_profile_list()

    def update_profile_list(self):
        self.profile_listbox.delete('1.0', tk.END)
        profiles = os.listdir(self.profiles_dir)
        for profile in profiles:
            self.profile_listbox.insert(tk.END, profile.replace('.json', '') + '\n')

    def assign_macro(self):
        selected_index = self.macro_listbox.index("insert")  # Get selected index
        if selected_index < 0 or not self.macro_recorder.macros:
            messagebox.showwarning("Warning", "No macro selected to assign.")
            return
        
        selected_button = self.button_dropdown.get()
        if selected_button == '':
            messagebox.showwarning("Warning", "No mouse button selected.")
            return

        # Here you could implement the logic to bind the macro to the selected mouse button.
        # This is just a placeholder.
        print(f"Assigned macro '{self.macro_recorder.macros[selected_index]}' to {selected_button}")

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
