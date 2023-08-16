import os
import subprocess


def video_to_audio(video_folder, converted_folder):
    for video_file in os.listdir(video_folder):
        if video_file.endswith('.mp4'):
            file_name, _ = os.path.splitext(video_file)
            input_path = os.path.join(video_folder, video_file)
            output_path = os.path.join(converted_folder, f'{file_name}.mp3')

            if not os.path.exists(output_path):
                command = f'ffmpeg -i "{input_path}" -vn -acodec libmp3lame -ac 2 -qscale:a 4 "{output_path}"'
                subprocess.call(command, shell=True)
                print(f'Converted: {video_file} to {file_name}.mp3')
            else:
                print(f'{file_name}.mp3 already exists, skipped converting {video_file}')
