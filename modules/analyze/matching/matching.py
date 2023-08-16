from abc import *

import numpy as np
import matplotlib.pyplot as plt
from fastdtw import fastdtw
from scipy.spatial.distance import cosine, euclidean

from .segment_tree import RangeUpdatePointQuery


class MatchingManager:
    class ModeEnum:
        BASIC = 1
        MULTI = 2
        MULTG = 3
        CORRM = 4

    def __init__(self, mode: int, sr: float = 8000, th: float = 0.2):
        if mode == self.ModeEnum.BASIC:
            self.match_algorithm = BasicMatchAlgorithm(sr, th)
        elif mode == self.ModeEnum.MULTI:
            self.match_algorithm = MultiMatchAlgorithm(sr, th)
        elif mode == self.ModeEnum.MULTG:
            self.match_algorithm = MultiMatchWithGraphAlgorithm(sr, th)
        elif mode == self.ModeEnum.CORRM:
            self.match_algorithm = CorrMatchAlgorithm(sr, th)
        else:
            raise ValueError(f"Invalid Preprocessor Type : {mode}")

    def run(self, video: np.ndarray, audio: np.ndarray, **kwargs) -> tuple[bool, list[tuple[str, str]]]:
        results = self.match_algorithm.run(video, audio, **kwargs)
        if len(results) > 0:
            return True, results
        return False, results


class BaseMatchAlgorithm(ABC):
    def __init__(self, sr: float, th: float = 0.2):
        self.sr = sr
        self.th = th

    def index_to_timestamp(self, index):
        total_seconds = index / self.sr
        minutes, seconds = divmod(total_seconds, 60)
        return f"{int(minutes)}:{int(seconds)}"

    @abstractmethod
    def run(self, video: np.ndarray, audio: np.ndarray, **kwargs) -> list[tuple[str, str]]:
        raise NotImplementedError("run method must be overrided.")


class BasicMatchAlgorithm(BaseMatchAlgorithm):
    def run(self, video_features: np.ndarray, audio_features: np.ndarray, **kwargs) -> list[tuple[str, str]]:
        min_distance = np.inf
        matched_start = -1
        matched_end = -1

        for start_idx in range(len(video_features) - len(audio_features) + 1):
            end_idx = start_idx + len(audio_features)

            video_clip_features = video_features[start_idx:end_idx]
            distance, _ = fastdtw(video_clip_features.T, audio_features.T, dist=euclidean)

            if distance < min_distance:
                min_distance = distance
                matched_start = start_idx
                matched_end = end_idx

        if min_distance < self.th:
            start_timestamp = self.index_to_timestamp(matched_start)
            end_timestamp = self.index_to_timestamp(matched_end)
            return [(start_timestamp, end_timestamp)]
        else:
            return []


class MultiMatchAlgorithm(BaseMatchAlgorithm):
    def run(self, video_features: np.ndarray, audio_features: np.ndarray, **kwargs) -> list[tuple[str, str]]:
        video_features_T = video_features.T  # (frames, features)
        audio_features_T = audio_features.T
        print(f"Matching Algorithm video shape: {video_features_T.shape}, audio shape: {audio_features_T.shape}")
        # print(f"Time Complexity: 5 * 29 * len(audio) * log(len(video)) + len(video) * log(len(video))")

        min_duration = 5
        matched_segments = []

        segment_tree1 = RangeUpdatePointQuery(video_features_T.shape[0])
        segment_tree2 = RangeUpdatePointQuery(video_features_T.shape[0])

        for audio_split in [4, 3]:
            window_size = int(audio_features_T.shape[0] / audio_split)
            step_size = int(window_size * 0.2)
            for audio_slice_num in range(audio_split):
                audio_slice = audio_features_T[audio_slice_num * window_size:(audio_slice_num + 1) * window_size]
                for start_idx in range(0, video_features_T.shape[0] - window_size + 1, step_size):
                    end_idx = start_idx + window_size
                    video_clip_features = video_features_T[start_idx:end_idx]
                    distance, _ = fastdtw(video_clip_features, audio_slice, dist=cosine)
                    segment_tree1.update(start_idx, end_idx, distance)
                    segment_tree2.update(start_idx, end_idx, 1)

        ratios = [0] * video_features_T.shape[0]
        for idx in range(video_features_T.shape[0]):
            denom = segment_tree2.get(idx)
            if denom > 0:
                ratios[idx] = segment_tree1.get(idx) / denom

        idx = 0
        while idx < len(ratios):
            start_idx = idx
            while idx < len(ratios) and ratios[idx] < self.th:
                idx += 1
            end_idx = idx
            duration = (end_idx - start_idx) / self.sr
            if duration >= min_duration:
                start_timestamp = self.index_to_timestamp(start_idx)
                end_timestamp = self.index_to_timestamp(end_idx)
                matched_segments.append((start_timestamp, end_timestamp))
            idx += 1

        return matched_segments


class MultiMatchWithGraphAlgorithm(BaseMatchAlgorithm):
    def run(self, video_features: np.ndarray, audio_features: np.ndarray, **kwargs) -> list[tuple[str, str]]:
        video_features_T = video_features.T  # (frames, features)
        audio_features_T = audio_features.T
        print(f"Matching Algorithm video shape: {video_features_T.shape}, audio shape: {audio_features_T.shape}")
        # print(f"Time Complexity: 5 * 29 * len(audio) * log(len(video)) + len(video) * log(len(video))")

        min_duration = 5
        matched_segments = []

        segment_tree1 = RangeUpdatePointQuery(video_features_T.shape[0])
        segment_tree2 = RangeUpdatePointQuery(video_features_T.shape[0])

        for audio_split in [4, 3]:
            window_size = int(audio_features_T.shape[0] / audio_split)
            step_size = max(int(window_size * 0.2), 1)
            for audio_slice_num in range(audio_split):
                audio_slice = audio_features_T[audio_slice_num * window_size:(audio_slice_num + 1) * window_size]
                for start_idx in range(0, video_features_T.shape[0] - window_size + 1, step_size):
                    end_idx = start_idx + window_size
                    video_clip_features = video_features_T[start_idx:end_idx]
                    distance, _ = fastdtw(video_clip_features, audio_slice, dist=cosine)
                    segment_tree1.update(start_idx, end_idx, distance)
                    segment_tree2.update(start_idx, end_idx, 1)

        ratios = [0] * video_features_T.shape[0]
        for idx in range(video_features_T.shape[0]):
            denom = segment_tree2.get(idx)
            if denom > 0:
                ratios[idx] = segment_tree1.get(idx) / denom

        idx = 0
        while idx < len(ratios):
            start_idx = idx
            while idx < len(ratios) and ratios[idx] < self.th:
                idx += 1
            end_idx = idx
            duration = (end_idx - start_idx) / self.sr
            if duration >= min_duration:
                start_timestamp = self.index_to_timestamp(start_idx)
                end_timestamp = self.index_to_timestamp(end_idx)
                matched_segments.append((start_timestamp, end_timestamp))
            idx += 1

        plt.plot(ratios)
        plt.xlabel('Index')
        plt.ylabel('segment_tree1.get(idx) / div')
        plt.axhline(y=self.th, color='r', linestyle='--', label='Threshold')
        plt.legend()
        plt.savefig(f'{kwargs.get("name", audio_features_T.shape[0])}.png', dpi=300)

        return matched_segments


class CorrMatchAlgorithm(BaseMatchAlgorithm):
    def run(self, video_features: np.ndarray, audio_features: np.ndarray, **kwargs) -> list[tuple[str, str]]:
        """
        Finds the location where the pattern might be present in multivariate data using
        frequency domain correlation (convolution).
        """
        data = video_features.T  # (frames, features)
        pattern = audio_features.T

        n = len(data)
        m = len(pattern)
        if n > m:
            pattern = np.pad(pattern, ((0, n - m), (0, 0)))
        elif n < m:
            data = np.pad(data, ((0, m - n), (0, 0)))

        total_score = 0
        best_loc = None
        max_score = 0

        for i in range(data.shape[1]):
            # Convert both data and pattern of this feature to frequency domain
            data_fft = np.fft.fft(data[:, i])
            pattern_fft = np.conj(np.fft.fft(pattern[:, i]))  # conjugate for correlation

            # Compute correlation in the frequency domain (using convolution theorem)
            result = np.fft.ifft(data_fft * pattern_fft)

            # Get the location of maximum correlation for this feature
            max_loc = np.argmax(np.abs(result))
            score = np.abs(result[max_loc])
            if score > max_score:
                best_loc = max_loc

            total_score += score

        if total_score > np.mean(np.abs(data)) and best_loc is not None:
            start_timestamp = self.index_to_timestamp(best_loc)
            return [(start_timestamp, "")]
        return []
