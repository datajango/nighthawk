import tkinter as tk

class CenteredDialogMixin:
    def center_over_master(self):
        # Get main window's geometry
        main_x = self.master.winfo_x()
        main_y = self.master.winfo_y()
        main_width = self.master.winfo_width()
        main_height = self.master.winfo_height()

        # Wait for the dialog to get its dimensions
        self.update_idletasks()

        # Calculate the position to center the dialog over the main window
        dialog_width = self.winfo_width()
        dialog_height = self.winfo_height()
        pos_x = main_x + (main_width // 2) - (dialog_width // 2)
        pos_y = main_y + (main_height // 2) - (dialog_height // 2)

        # Set the dialog's position
        self.geometry(f"+{pos_x}+{pos_y}")
