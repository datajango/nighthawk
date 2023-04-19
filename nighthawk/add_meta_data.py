import ffmpy
import re
import os
import json
import subprocess
import glob
import sys
import tkinter as tk
from tkinter import filedialog
from pymp4 import mp4

def update_metadata(input_file, metadata):
    # Open the MP4 file
    with mp4.MP4(input_file) as video_file:
        # Update metadata
        for key, value in metadata.items():
            video_file[key] = value

        # Save the changes
        video_file.save()

def remove_bracketed_substrings(filename):
    # Use a regular expression to remove substrings enclosed in brackets
    cleaned_filename = re.sub(r'\[.*?\]', '', filename)
    return cleaned_filename

def write_metadata(input_file, output_file, metadata):
    metadata_args = []
    for key, value in metadata.items():
        metadata_args.append('-metadata')
        metadata_args.append(f'{key}={value}')

    ff = ffmpy.FFmpeg(
        inputs={input_file: None},
        outputs={output_file: metadata_args},
    )
    ff.run()

def find_videos_with_codec(folder, codec):
    # Get all video files in the folder
    video_files = glob.glob(os.path.join(folder, '*.*'))

    matching_files = []

    for video_file in video_files:
        # Get metadata of the video file
        ffprobe_command = [
            'ffprobe',
            '-v', 'quiet',
            '-print_format', 'json',
            '-show_streams',
            video_file
        ]
        # ffprobe -v quiet -print_format json -show_streams E:/dev/nighthawk/downloads\America's Secret Space Program and the Alien Connection_ Solar Warden [avc1.640028].mp4

        print(' '.join(ffprobe_command))
        result = subprocess.run(ffprobe_command, stdout=subprocess.PIPE)
        metadata = json.loads(result.stdout.decode('utf-8'))

        if 'streams' not in metadata:
            print(f"Error: no streams found in metadata for {video_file}")
            continue

        # Check if the video file has the desired codec
        for stream in metadata['streams']:
            if stream['codec_tag_string'] == codec:
                matching_files.append(video_file)
                break

    return matching_files

def get_file_path():
    # Create a Tkinter root window (it won't be displayed)
    root = tk.Tk()
    root.withdraw()

    # Open a file dialog and get the selected file path
    file_path = filedialog.askdirectory()

    # Destroy the root window and exit
    root.destroy()

    return file_path


def add_meta_to_filename(file_path):
    # Split the file path into directory, name, and extension
    file_dir, file_name = os.path.split(file_path)
    file_base, file_ext = os.path.splitext(file_name)

    # Create the new filename with "(meta)" added
    new_file_name = f"{file_base} (meta){file_ext}"
    new_file_path = os.path.join(file_dir, new_file_name)

    # Rename the file
    #os.rename(file_path, new_file_path)

    return new_file_path


def run():

    file_path = get_file_path()
    print("Selected file path:", file_path)

    
    #codec = 'avc1.640028'
    codec = 'avc1'

    matching_files = find_videos_with_codec(file_path, codec)
    print("Matching video files:", matching_files)


    # files = [
    #     "America's Secret Space Program and the Alien Connection_ Solar Warden 2023-04-06 [avc1.640028].mp4",    
    #     "How to Build a Working UFO _ Alien Reproduction Vehicles (ARVs)  2022-12-08 [avc1.640028].mp4",
    #     "TESLA KNEW The Secret of the Great Pyramid_ Unlimited Energy to Power the World 2022-10-06  [avc1.640028].mp4",
    #     "What Are They Hiding Underneath_ The Truth about the Denver International Airport Conspiracy 2023-03-30  [avc1.640028].mp4"
    # ]

    for index, filename in enumerate(matching_files):

        #new_filename = add_meta_to_filename(filename)

        metadata = {
            'title': remove_bracketed_substrings(filename),
            'show': 'The Why Files',
            'season_number': '1',
            'episode_number': str(index + 1)
        }

        #write_metadata(filename, new_filename, metadata)
        update_metadata(filename, metadata)

if __name__ == "__main__":
    run()