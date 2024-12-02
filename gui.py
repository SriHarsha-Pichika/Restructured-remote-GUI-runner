"""GUI implementation for Remote Script Runner."""

import tkinter as tk
from tkinter import messagebox, ttk
from typing import Callable
from config import SYSTEMS

class LoginWindow:
    def __init__(self, on_login: Callable[[str, str], bool]):
        self.window = tk.Tk()
        self.window.title("Login")
        self.on_login = on_login
        self._create_widgets()

    def _create_widgets(self):
        """Create login window widgets."""
        frame = ttk.Frame(self.window, padding="10")
        frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        self.username_var = tk.StringVar()
        self.password_var = tk.StringVar()

        ttk.Label(frame, text="Username:").grid(row=0, column=0, pady=5)
        ttk.Entry(frame, textvariable=self.username_var).grid(row=0, column=1, pady=5)

        ttk.Label(frame, text="Password:").grid(row=1, column=0, pady=5)
        ttk.Entry(frame, textvariable=self.password_var, show="*").grid(row=1, column=1, pady=5)

        ttk.Button(frame, text="Login", command=self._handle_login).grid(row=2, column=0, columnspan=2, pady=10)

    def _handle_login(self):
        """Handle login button click."""
        if self.on_login(self.username_var.get(), self.password_var.get()):
            self.window.destroy()
        else:
            messagebox.showerror("Login Failed", "Invalid username or password")

    def run(self):
        """Start the login window."""
        self.window.mainloop()

class MainWindow:
    def __init__(self, on_script_execute: Callable[[str, str], None]):
        self.window = tk.Tk()
        self.window.title("Remote Script Runner")
        self.on_script_execute = on_script_execute
        self._create_widgets()

    def _create_widgets(self):
        """Create main window widgets."""
        frame = ttk.Frame(self.window, padding="10")
        frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # System selection
        self.selected_system = tk.StringVar(value=list(SYSTEMS.keys())[0])
        ttk.Label(frame, text="Select System:").grid(row=0, column=0, pady=5)
        ttk.OptionMenu(frame, self.selected_system, *SYSTEMS.keys()).grid(row=0, column=1, pady=5)

        # Script path
        self.script_path = tk.StringVar()
        ttk.Label(frame, text="Script Path:").grid(row=1, column=0, pady=5)
        ttk.Entry(frame, textvariable=self.script_path, width=50).grid(row=1, column=1, pady=5)

        # Execute button
        ttk.Button(frame, text="Run Script", command=self._handle_execute).grid(row=2, column=0, columnspan=2, pady=10)

    def _handle_execute(self):
        """Handle script execution button click."""
        system = self.selected_system.get()
        script_path = self.script_path.get()

        if not script_path:
            messagebox.showerror("Error", "Please provide a script path!")
            return

        try:
            self.on_script_execute(system, script_path)
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def run(self):
        """Start the main window."""
        self.window.mainloop()