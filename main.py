"""Main entry point for Remote Script Runner."""

from typing import Tuple
import tkinter as tk
from tkinter import messagebox

from config import SYSTEMS
from auth import AuthManager
from ssh_manager import SSHManager
from salt_manager import SaltManager
from gui import LoginWindow, MainWindow

class RemoteScriptRunner:
    def __init__(self):
        self.auth_manager = AuthManager()
        self.ssh_manager = SSHManager(username="", key_path="")  # Set proper credentials
        self.salt_manager = SaltManager()

    def run_script(self, system_label: str, script_path: str) -> Tuple[str, str]:
        """Execute script on selected system."""
        if system_label == "All Systems":
            return self.salt_manager.execute_script(script_path)
        else:
            system = SYSTEMS[system_label]
            if not system:
                raise ValueError(f"Invalid system: {system_label}")
            
            self.ssh_manager.connect(system)
            return self.ssh_manager.execute_script(script_path)

    def handle_script_execution(self, system_label: str, script_path: str) -> None:
        """Handle script execution and display results."""
        try:
            output, error = self.run_script(system_label, script_path)
            if output:
                messagebox.showinfo("Output", f"Script Output:\n{output}")
            if error:
                messagebox.showwarning("Error", f"Script Error:\n{error}")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

    def start(self):
        """Start the application."""
        def handle_login(username: str, password: str) -> bool:
            if self.auth_manager.validate_credentials(username, password):
                MainWindow(self.handle_script_execution).run()
                return True
            return False

        login_window = LoginWindow(handle_login)
        login_window.run()

if __name__ == "__main__":
    app = RemoteScriptRunner()
    app.start()