# Version 2

"""
- Add a function to handle the Download a Video
    - Create the ./downloads folder if it doesn't exist
    - Use the pytube library to download the video
"""
import os
import re
import json
import configparser
import tkinter as tk
from tkinter import messagebox, simpledialog, filedialog
from pytube import YouTube
from merge_audio_and_video import merge_audio_video_files
from config import Config
from nighthawk.property_editor import PropertyEditor
from nighthawk.show_about import show_about

# properties = [
#     {
#         'section': 'NightHawk',
#         'key': 'download_folder',
#         'property_type': 'directory',
#         'prompt': 'Enter the download folder:',
#         'value': None,
#         'default_value': './downloads'
#     },
#     {
#         'section': 'NightHawk',
#         'key': 'video_codec',
#         'property_type': 'string',
#         'prompt': 'Enter the video codec:',
#         'value': None,
#         'default_value': 'avc1'
#     }
# ]

# def load_properties_from_file(filepath):
#     with open(filepath, 'r') as file:
#         properties = json.load(file)
#     return properties

def load_properties_from_file(filename):
    base_path = os.path.dirname(os.path.abspath(__file__))
    filepath = os.path.join(base_path, filename)
    
    with open(filepath, 'r') as file:
        properties = json.load(file)
    return properties

def clean_folder_name(folder_name):
    # Remove invalid Windows characters: < > : " / \ | ? *
    cleaned_name = re.sub(r'[<>:"/\\|?*]', '_', folder_name)
    return cleaned_name


def handle_merge_audio_video_files(config):
    download_folder = config.get('Download', 'download_folder', default=None)

    if not download_folder:
        download_folder = filedialog.askdirectory()
        config.set('Download', 'download_folder', download_folder)

    merge_audio_video_files(download_folder)


def get_file_extension(yt):
    # Get all available streams
    all_streams = yt.streams

    # Extract the unique file extensions from the streams
    file_extensions = set(stream.mime_type.split('/')[-1] for stream in all_streams)

    return file_extensions

def display_available_file_extensions(file_extensions):
    # Print the file extensions
    print("Available file extensions:")
    for ext in file_extensions:
        print(ext)

def prepare_download_folder(download_folder='./downloads'):
    # Create the downloads folder if it doesn't exist    
    if not os.path.exists(download_folder):
        os.makedirs(download_folder)


def download_video_stream(yt, download_folder, stream):
    custom_filename = f"video_{stream.title} [{stream.video_codec}].{stream.subtype}"        
    cleaned_name = clean_folder_name(custom_filename)

    # Check if the file already exists
    if os.path.exists(os.path.join(download_folder, cleaned_name)):
        print("Warning", "File already exists. Skipping download.")
    else:
        print(f"Downloading: {cleaned_name}")
        stream.download(download_folder, filename=cleaned_name)

    if stream.includes_audio_track:
        print(f"\tIncludes Audio Track")
    else:
        # must download audio separately
        # Get the highest quality audio stream
        audio_stream = yt.streams.filter(adaptive=True, file_extension='mp4', only_audio=True).order_by('abr').desc().first()
        
        if audio_stream:
            custom_filename = f"audio_{stream.title} [{stream.video_codec}].{stream.subtype}"        
            cleaned_name = clean_folder_name(custom_filename)
            
            # Check if the file already exists
            if os.path.exists(os.path.join(download_folder, cleaned_name)):
                print("Warning", "File already exists. Skipping download.")
            else:
                print(f"Downloading: {cleaned_name}")
                audio_file = audio_stream.download(download_folder, filename=cleaned_name)


def download_video(url):
    download_folder = './downloads'

    print(f"Downloading {url}")    
    yt = YouTube(url)
    file_extensions = get_file_extension(yt)
    display_available_file_extensions(file_extensions)

    video_streams = yt.streams.order_by('resolution').desc()

    prepare_download_folder()
    there_is_no_1080p = False

    if video_streams:
        # Print available resolutions
        print("Available resolutions:")
        for index, stream in enumerate(video_streams):
            print(f"{index+1} Resolution: {stream.resolution}")
            print(f"\tTitle:{stream.default_filename}")
            print(f"\tFilesize:{stream.filesize_mb} MB")
            print(f"\tVideo Code:{stream.video_codec}")           
            print(f"\Sub Type:{stream.subtype}")           
            
            if stream.resolution == '1080p':
              download_video_stream(yt, download_folder, stream)

        first_stream = video_streams.first()
        download_video_stream(yt, download_folder, first_stream)
    else:
        print("No video streams found.")

def download_url():
    url = simpledialog.askstring("Download URL", "Enter the URL to download:")
    if url:
        # Add your download logic here
        print(f"Downloading {url}")
        download_video(url)
    else:
        print("No URL entered")

def exit_app():
    if messagebox.askokcancel("Exit", "Do you want to exit? Make sure no downloads are in progress."):
        root.destroy()

def about():
    about_dialog = tk.Toplevel(root)
    about_dialog.title("About")
    about_label = tk.Label(about_dialog, text="This is a simple Tkinter UI example\nVersion 1.0", padx=10, pady=10)
    about_label.pack()
    about_dialog.transient(root)

def edit_properties(properties, config):
    editor = PropertyEditor(root, properties, config)
    root.wait_window(editor)
    print("Updated properties:", properties)
    
properties_file = 'properties.json'
properties = load_properties_from_file(properties_file)

# Create a config object
config_file = 'config.ini'
config = Config(config_file, properties)

root = tk.Tk()
root.title("Simple Tkinter UI")

menu_bar = tk.Menu(root)
root.config(menu=menu_bar)

file_menu = tk.Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="File", menu=file_menu)
file_menu.add_command(label="Download", command=download_url)
file_menu.add_command(label="Merge Audio and Video Files", command=lambda: handle_merge_audio_video_files())
file_menu.add_command(label="Properties", command=lambda: edit_properties(properties, config))
file_menu.add_separator()
file_menu.add_command(label="Exit", command=exit_app)

help_menu = tk.Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="Help", menu=help_menu)
help_menu.add_command(label="About", command=lambda: show_about(root))

root.mainloop()
