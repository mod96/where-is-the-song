import time
import fcntl
import multiprocessing as mp
import os

from .preprocess import PreprocessManager
from .feature import FeatureManager
from .matching import MatchingManager


def process_video_audio_pair(video_path, audio_path,
                             results, results_folder,
                             ns, sr, th, mode):
    # Preprocess & Feature Extraction
    preprocessor = PreprocessManager(PreprocessManager.ModeEnum.SPECTRAL, sr=sr)
    feature_extractor = FeatureManager(FeatureManager.ModeEnum.SPECTRAL, sr=sr)
    # Synchronize video_preprocessed access
    with ns.video_preprocessed_lock:
        if video_path not in ns.video_preprocessed:
            print(f"Preprocessing, Feature Extraction Start for {video_path}")
            st = time.time()
            video_processed, video_sr = preprocessor.run(video_path)
            video_features = feature_extractor.run(video_processed)
            ns.video_preprocessed[video_path] = video_features
            print(f"Preprocessing, Feature Extraction for {video_path} done with time: {time.time() - st}s")
        else:
            print(f"{video_path} already extracted, skipping...")
            video_features = ns.video_preprocessed[video_path]

    # Synchronize audio_preprocessed access
    with ns.audio_preprocessed_lock:
        if audio_path not in ns.audio_preprocessed:
            print(f"Preprocessing, Feature Extraction Start for {audio_path}")
            st = time.time()
            audio_processed, audio_sr = preprocessor.run(audio_path)
            audio_features = feature_extractor.run(audio_processed)
            ns.audio_preprocessed[audio_path] = audio_features
            print(f"Preprocessing, Feature Extraction for {audio_path} done with time: {time.time() - st}s")
        else:
            print(f"{audio_path} already extracted, skipping...")
            audio_features = ns.audio_preprocessed[audio_path]

    # Matching
    print(f"Match process start for {video_path} -- {audio_path}")
    st = time.time()
    matcher = MatchingManager(mode, sr=video_features[1], th=th)
    is_matched, matched_segments = matcher.run(video_features[0], audio_features[0], name=audio_path.split()[1])
    print(f"Match process done for {video_path} -- {audio_path} with time: {time.time() - st}s")

    if is_matched:
        result = (video_path, audio_path, matched_segments)
        results.append(result)
        save_result_to_file(result, results_folder)


def save_result_to_file(result, results_folder):
    video_path, audio_path, matched_segments = result
    video_name = os.path.splitext(os.path.basename(video_path))[0]
    audio_name = os.path.splitext(os.path.basename(audio_path))[0]

    with open(f"{results_folder}/{video_name}_report.txt", "a") as report_file:
        # Lock the file
        fcntl.flock(report_file, fcntl.LOCK_EX)

        # Write results
        report_file.write(f"Audio: {audio_name}\n")
        report_file.write(f"Matched segments: {matched_segments}\n")
        report_file.write("\n")

        # Unlock the file
        fcntl.flock(report_file, fcntl.LOCK_UN)


class VideoAudioMatchRunner:
    def __init__(self, converted_folder, audio_folder, results_folder, sr=2048, th=20,
                 mode=MatchingManager.ModeEnum.MULTI):
        self.converted_folder = converted_folder
        self.audio_folder = audio_folder
        self.results_folder = results_folder
        self.sr = sr
        self.th = th
        self.mode = mode

    def run(self):
        if not os.path.exists(self.results_folder):
            os.makedirs(self.results_folder)

        video_files = [os.path.join(self.converted_folder, f) for f in os.listdir(self.converted_folder)]
        audio_files = [os.path.join(self.audio_folder, f) for f in os.listdir(self.audio_folder)]

        manager = mp.Manager()
        results = manager.list()
        ns = manager.Namespace()
        ns.video_preprocessed = manager.dict()
        ns.audio_preprocessed = manager.dict()
        ns.video_preprocessed_lock = manager.Lock()
        ns.audio_preprocessed_lock = manager.Lock()

        # Using a process pool for parallel processing
        cores = max(int(mp.cpu_count() * 0.8), 1)
        print(f'Using {cores} cores')
        with mp.Pool(processes=cores) as pool:
            async_results = []  # Store the results of async calls
            for video_path in video_files:
                for audio_path in audio_files:
                    try:
                        async_result = pool.apply_async(process_video_audio_pair,
                                                        args=(video_path, audio_path,
                                                              results, self.results_folder,
                                                              ns, self.sr, self.th, self.mode))
                        async_results.append(async_result)
                    except Exception as e:
                        print(f'[ERROR] Matching {video_path} & {audio_path} failed. Skip. Traceback:')
                        print(e)

            # Wait for all async calls to finish
            for async_result in async_results:
                async_result.get()

            pool.close()
            pool.join()

        print("Results:")
        for video_path, audio_path, matched_segments in results:
            print(f"Video: {video_path}, Audio: {audio_path}, Matched segments: {matched_segments}")
