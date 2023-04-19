import tkinter as tk
from tkinter import simpledialog

def show_about(root):
    about_dialog = tk.Toplevel()
    about_dialog.title("About")

    about_label = tk.Label(about_dialog, text="NightHawk - A Video Downloader")
    about_label.pack(padx=20, pady=20)

    # Get main window's geometry
    main_x = root.winfo_x()
    main_y = root.winfo_y()
    main_width = root.winfo_width()
    main_height = root.winfo_height()

    # Wait for the About dialog to get its dimensions
    about_dialog.update_idletasks()

    # Calculate the position to center the About dialog over the main window
    about_width = about_dialog.winfo_width()
    about_height = about_dialog.winfo_height()
    pos_x = main_x + (main_width // 2) - (about_width // 2)
    pos_y = main_y + (main_height // 2) - (about_height // 2)

    # Set the About dialog's position
    about_dialog.geometry(f"+{pos_x}+{pos_y}")
