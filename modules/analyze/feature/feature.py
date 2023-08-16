from abc import *

import librosa.feature
import numpy as np


class FeatureManager:
    class ModeEnum:
        BASIC = 1
        SPECTRAL = 2

    def __init__(self, mode: int, sr: float = 8000):
        if mode == self.ModeEnum.BASIC:
            self.feature_extractor = BasicFeatureExtractor(sr)
        elif mode == self.ModeEnum.SPECTRAL:
            self.feature_extractor = SpectralFeatureExtractor(sr)
        else:
            raise ValueError(f"Invalid FeatureExtractor Type : {mode}")

    def run(self, audio: np.ndarray) -> tuple[np.ndarray, float]:
        return self.feature_extractor.run(audio)


class BaseFeatureExtractor(ABC):
    def __init__(self, sr: float):
        self.sr = sr

    @abstractmethod
    def run(self, audio: np.ndarray) -> tuple[np.ndarray, float]:
        raise NotImplementedError("run method must be overrided.")


class BasicFeatureExtractor(BaseFeatureExtractor):
    def run(self, y: np.ndarray) -> tuple[np.ndarray, float]:
        mfccs = librosa.feature.mfcc(y=y, sr=self.sr)
        chroma = librosa.feature.chroma_cqt(y=y, sr=self.sr)
        features = np.concatenate((mfccs, chroma), axis=0)
        return features, self.sr / 512


class SpectralFeatureExtractor(BaseFeatureExtractor):
    def run(self, y: np.ndarray) -> tuple[np.ndarray, float]:
        """
        :param y: resampled data shape with (frames,)
        :return: feature extracted data (features, frames), hopped_sr (sr / 512)
        """
        # MFCC
        mfcc = librosa.feature.mfcc(y=y, sr=self.sr, n_mfcc=13)

        # 크로마 그램
        chromagram = librosa.feature.chroma_stft(y=y, sr=self.sr)

        # 스펙트럼 대비
        spectral_contrast = librosa.feature.spectral_contrast(y=y, sr=self.sr, fmin=self.sr / 128)

        # 특징 벡터 결합
        features = np.concatenate((mfcc, chromagram, spectral_contrast), axis=0)

        return features, self.sr / 512
