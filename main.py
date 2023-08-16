import argparse
from modules import VideoToAudioRunner, VideoAudioMatchRunner

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Video to audio converter and audio matcher')
    parser.add_argument('-c', '--convert', action='store_true',
                        help='Convert all .mp4 files in the video folder to .mp3 files in the converted_video folder')
    parser.add_argument('-m', '--match', action='store_true',
                        help='Match the audio files in the audio folder with the '
                             'converted video files in the converted_video folder')
    parser.add_argument('-th', '--threshold', help='Video Matcher Threshold. Use GraphMatch Option for tuning',
                        default=20)
    parser.add_argument('-sr', '--samplingrate', help='Sampling rate for both videos and songs. Larger makes '
                                                      'significantly slower but little accurate', default=2048)
    parser.add_argument('-mo', '--matchermode', help='Video Matcher Mode. 1~4', default=2)

    args = parser.parse_args()

    video_folder = './video'
    converted_folder = './converted_video'
    audio_folder = './audio'
    results_folder = './results'

    threashold = int(args.threshold)
    samplingrate = int(args.samplingrate)
    matchermode = int(args.matchermode)

    if args.convert:
        VideoToAudioRunner(video_folder, converted_folder).run()

    if args.match:
        VideoAudioMatchRunner(converted_folder, audio_folder, results_folder,
                              samplingrate, threashold, matchermode).run()
