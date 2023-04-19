import os

def merge_audio_video_files(folder_path):    
    # Get a list of files in the folder
    files = os.listdir(folder_path)

    # Group files with the same name (excluding the audio_ and video_ prefixes)
    grouped_files = {}
    for file in files:
        if file.startswith("audio_") or file.startswith("video_"):
            base_name = file[6:]
            grouped_files.setdefault(base_name, []).append(file)

    if not grouped_files:
        print("No audio and video files to merge.")
        return
    
    # Merge audio and video files with the same name
    for base_name, file_group in grouped_files.items():
        if len(file_group) == 2:
            audio_file = None
            video_file = None

            for file in file_group:
                if file.startswith("audio_"):
                    audio_file = os.path.join(folder_path, file)
                elif file.startswith("video_"):
                    video_file = os.path.join(folder_path, file)

            if audio_file and video_file:
                # Merge video and audio streams using ffmpeg (make sure ffmpeg is installed and in your PATH)
                output_file = os.path.join(folder_path, base_name)
                os.system(f'ffmpeg -i "{video_file}" -i "{audio_file}" -c copy "{output_file}"')

                # Remove temporary video and audio files
                os.remove(video_file)
                os.remove(audio_file)
