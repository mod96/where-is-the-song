from .ffmpeg import video_to_audio
from .analyze import VideoAudioMatchRunner


class VideoToAudioRunner:
    def __init__(self, video_folder, converted_folder):
        self.video_folder = video_folder
        self.converted_folder = converted_folder

    def run(self):
        video_to_audio(self.video_folder, self.converted_folder)
