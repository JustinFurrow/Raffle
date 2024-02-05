import tkinter as tk
from tkinter import messagebox, simpledialog, Toplevel, Listbox
import json
import os
import threading
import time
import schedule
from plyer import notification
from pystray import MenuItem as item
import pystray
from PIL import Image, ImageDraw
import random

# System tray icon
def create_image(width, height, color1, color2):
    # This is just a simple image for the icon. You might want to use a real .ico file
    image = Image.new('RGB', (width, height), color1)
    dc = ImageDraw.Draw(image)
    dc.rectangle(
        [width // 2, 0, width, height // 2],
        fill=color2)
    dc.rectangle(
        [0, height // 2, width // 2, height],
        fill=color2)

    return image

def show_hourly_notification():
    notification.notify(
        title='Time Check',
        message='Are you focusing? Open Reminder App for tasks.',
        app_name='Reminder App'
    )

def run_scheduler():
    schedule.every().hour.do(show_hourly_notification)

    while True:
        schedule.run_pending()
        time.sleep(1)

scheduler_thread = threading.Thread(target=run_scheduler, daemon=True)
scheduler_thread.start()

# Function to load tasks and categories
def load_raffle_data(filename):
    try:
        if os.path.exists(filename) and os.path.getsize(filename) > 0:  # Checks file exists and is not empty
            with open(filename, 'r') as file:
                return json.load(file)
        else:
            return {}  # Return an empty dictionary if the file doesn't exist or is empty
    except json.JSONDecodeError:  # Handle JSON decode error if the file is corrupted
        print(f"Error loading {filename}. File is corrupted or not valid JSON.")
        return {}

# Function to save tasks and categories
def save_raffle_data(filename, raffle_dict):
    with open(filename, 'w') as file:
        json.dump(raffle_dict, file, indent=4)

class ReminderApp:
    def __init__(self, master):
        self.master = master
        master.title('Reminder App')
        self.master.geometry("800x400")  # Adjusted window size for better layout

        # Load the tasks and categories data
        self.raffle_dict = load_raffle_data('raffle_data.txt')

        # Initialize suggestion and timer variables
        self.suggestion_var = tk.StringVar(self.master)
        self.timer_var = tk.StringVar(self.master, "60:00")

        # Initialize GUI components
        self.setup_ui()

        # Initialize the system tray icon but do not run it yet
        self.icon = pystray.Icon("ReminderApp", icon=create_image(64, 64, 'black', 'red'), title="Reminder App")
        self.icon.menu = pystray.Menu(
            item('Open', lambda icon, item: self.show_main_window()),
            item('Quit', lambda icon, item: self.quit_app())
        )

        # Start the background notification timer
        self.start_background_timer()

        # Start the system tray icon in a separate thread
        self.icon_thread = threading.Thread(target=self.icon.run)
        self.icon_thread.setDaemon(True)
        self.icon_thread.start()

        # Configure the window close handler
        self.master.protocol("WM_DELETE_WINDOW", self.minimize_to_tray)

    def minimize_to_tray(self):
        """Minimize the window to the system tray instead of exiting the application."""
        self.master.iconify()  # Minimize the main window
        self.icon.visible = True  # Show the system tray icon

    def setup_ui(self):
        # Categories section
        left_frame = tk.Frame(self.master)
        left_frame.pack(side='left', fill='y')

        self.category_label = tk.Label(left_frame, text="Categories")
        self.category_label.pack(side='top', fill='x')

        self.category_listbox = Listbox(left_frame)
        self.category_listbox.pack(side='top', fill='y', expand=True)

        self.add_category_button = tk.Button(left_frame, text="Add Category", command=self.add_category)
        self.add_category_button.pack(side='top', fill='x')

        self.remove_category_button = tk.Button(left_frame, text="Remove Selected Category", command=self.remove_selected_category)
        self.remove_category_button.pack(side='top', fill='x')

        self.update_category_listbox()

        # Center buttons
        center_frame = tk.Frame(self.master)
        center_frame.pack(side='left', padx=20)

        self.timer_label = tk.Label(center_frame, textvariable=self.timer_var)
        self.timer_label.pack(side='top')

        self.raffle_button = tk.Button(center_frame, text="Raffle!", command=self.raffle_task)
        self.raffle_button.pack(side='top')

        self.show_tasks_button = tk.Button(center_frame, text="Show Tasks", command=self.show_tasks)
        self.show_tasks_button.pack(side='top')

        self.hide_tasks_button = tk.Button(center_frame, text="Hide Tasks", command=self.hide_tasks)
        self.hide_tasks_button.pack(side='top')

        # Task management frame (initially hidden)
        self.task_frame = tk.Frame(self.master)
        self.task_frame.pack(side='left', fill='both', expand=True, padx=20)

        self.task_listbox = Listbox(self.task_frame)
        self.task_listbox.pack(side='top', fill='both', expand=True)

        self.add_task_button = tk.Button(self.task_frame, text="Add Task", command=self.add_task_to_category)
        self.add_task_button.pack(side='top', fill='x')

        self.remove_task_button = tk.Button(self.task_frame, text="Remove Selected Task", command=self.remove_selected_task)
        self.remove_task_button.pack(side='top', fill='x')

        # Suggestion label
        self.suggestion_label = tk.Label(self.master, textvariable=self.suggestion_var, wraplength=200)
        self.suggestion_label.pack(side='bottom', fill='x', expand=True)

    def update_category_listbox(self):
        self.category_listbox.delete(0, tk.END)  # Clear the listbox
        for category in self.raffle_dict.keys():
            self.category_listbox.insert(tk.END, category)
    
    def add_category(self):
        category = simpledialog.askstring("Add Category", "Category name:")
        if category and category not in self.raffle_dict:
            self.raffle_dict[category] = []
            self.update_category_listbox()
            self.save_raffle_data()
    
    def remove_selected_category(self):
        selection = self.category_listbox.curselection()
        if selection:
            category = self.category_listbox.get(selection[0])
            del self.raffle_dict[category]
            self.update_category_listbox()
            self.save_raffle_data()

    def add_task_to_category(self):
        selected_category = self.category_listbox.get(tk.ACTIVE)
        if selected_category:
            task = simpledialog.askstring("Add Task", "Task description:")
            if task and task not in self.raffle_dict[selected_category]:
                self.raffle_dict[selected_category].append(task)
                self.update_task_listbox(selected_category)
                self.save_raffle_data()

    def remove_selected_task(self):
        selected_category = self.category_listbox.get(tk.ACTIVE)
        if selected_category:
            selection = self.task_listbox.curselection()
            if selection:
                task = self.task_listbox.get(selection[0])
                self.raffle_dict[selected_category].remove(task)
                self.update_task_listbox(selected_category)
                self.save_raffle_data()

    def save_raffle_data(self):
        save_raffle_data('raffle_data.txt', self.raffle_dict)

    def raffle_task(self):
        selected_category = self.category_listbox.get(tk.ACTIVE)
        if selected_category:
            tasks = self.raffle_dict.get(selected_category, [])
            if tasks:
                self.suggestion_var.set(random.choice(tasks))
            else:
                messagebox.showinfo("Info", "No tasks in the selected category.")
        else:
            messagebox.showinfo("Info", "No category selected.")

    def show_tasks(self):
        selected_category = self.category_listbox.get(tk.ACTIVE)
        if selected_category:
            self.update_task_listbox(selected_category)
            self.task_frame.pack(side='right', fill='both', expand=True)

    def hide_tasks(self):
        self.task_frame.pack_forget()

    def add_task_to_category(self):
        selected_category = self.category_listbox.get(tk.ACTIVE)
        if selected_category:
            task = simpledialog.askstring("Add Task", "Task description:")
            if task:
                self.raffle_dict[selected_category].append(task)
                save_raffle_data('raffle_data.txt', self.raffle_dict)
                self.update_task_listbox(selected_category)

    def remove_selected_task(self):
        selected_category = self.category_listbox.get(tk.ACTIVE)
        if selected_category:
            selected_task_index = self.task_listbox.curselection()
            if selected_task_index:
                selected_task = self.task_listbox.get(selected_task_index)
                self.raffle_dict[selected_category].remove(selected_task)
                save_raffle_data('raffle_data.txt', self.raffle_dict)
                self.update_task_listbox(selected_category)

    def update_task_listbox(self, category):
        self.task_listbox.delete(0, tk.END)
        for task in self.raffle_dict.get(category, []):
            self.task_listbox.insert(tk.END, task)

    # Create the system tray application
    def setup_system_tray_app(self):
       # Check if the system tray icon already exists
       if hasattr(self, 'icon'):
            self.icon.stop()
       
       # Create a system tray icon
       self.icon = pystray.Icon("ReminderApp", icon=create_image(64, 64, 'black', 'red'), title="Reminder App")
       self.icon.menu = pystray.Menu(
           item('Open', self.show_main_window),
           item('Quit', self.quit_app)
       )
       self.icon.run_detached()  # This ensures the icon runs without blocking

    # Define the method for handling the window close event
    def on_close(self):
        """Handles the window close event."""
        # Minimize to system tray instead of exiting the application
        self.master.iconify()  # Hide the main window

    # Define actions
    def show_main_window(self):
        """Shows the main application window."""
        self.master.deiconify()  # Show the main window again
        self.icon.visible = False # Hide the system tray icon

    def quit_app(self):
        self.icon.stop()
        self.master.destroy()  # Destroy the main window to quit the application

    def quit_app_main_thread(self):
        if self.master:
            self.master.destroy() # This will quit the application
        os._exit(0)  # Ensure the program exits

    def start_background_timer(self):
        # Initialize the next notification time
        self.next_notification_time = time.time() + 3600
    
        # Start the timer update loop for the GUI
        self.update_timer()

        # Use threading to run the notification timer in the background
        def background_timer():
            while True:
                now = time.time()
                if now >= self.next_notification_time:
                    self.trigger_notification()
                    self.next_notification_time = now + 3600
                time.sleep(1)  # Check every second

        # Use threading to run the notification timer in the background
        timer_thread = threading.Thread(target=self.background_timer, daemon=True)
        timer_thread.start()

    def background_timer(self):
    # Sleep until it's time for the next notification
        while True:
            time.sleep(self.calculate_sleep_duration())
            self.trigger_notification()

    def calculate_sleep_duration(self):
        # Calculate how much time to sleep until the next notification
        now = time.time()
        time_remaining = self.next_notification_time - now
        return max(time_remaining, 0)
    
    def trigger_notification(self):
        # Trigger the desktop notification and reset the notification timer
        notification.notify(
            title='Time Check',
            message='Are you focusing on your tasks?',
            app_name='Reminder App'
        )
        # Reset the timer for the next notification
        self.next_notification_time = time.time() + 3600
        # Since trigger_notification is called from a background thread,
        # we need to use .after to update the GUI in the main thread
        self.master.after(0, lambda: self.update_timer())
    
    def update_timer(self):
        # Calculate the time remaining until the next notification
        now = time.time()
        time_remaining = max(self.next_notification_time - now, 0)
        minutes, seconds = divmod(int(time_remaining), 60)
        self.timer_var.set(f"{minutes:02d}:{seconds:02d}")
        # Reschedule the update_timer to run after 1000ms
        self.master.after(1000, self.update_timer)

if __name__ == "__main__":
    root = tk.Tk()
    app = ReminderApp(root)
    root.mainloop()