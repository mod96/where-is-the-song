from abc import *

import pywt

from .functions import *


class PreprocessManager:
    class ModeEnum:
        BASIC = 1
        SPECTRAL = 2

    def __init__(self, mode: int, sr: float = 8000):
        if mode == self.ModeEnum.BASIC:
            self.preprocessor = BasicPreprocessor(sr)
        elif mode == self.ModeEnum.SPECTRAL:
            self.preprocessor = SpectralPreprocessor(sr)
        else:
            raise ValueError(f"Invalid Preprocessor Type : {mode}")

    def run(self, audio_path: str) -> tuple[np.ndarray, float]:
        return self.preprocessor.run(audio_path)


class BasePreprocessor(ABC):
    def __init__(self, sr: float = 8000):
        self.sr = sr

    @abstractmethod
    def run(self, audio_path: str) -> tuple[np.ndarray, float]:
        raise NotImplementedError("run method must be overrided.")


class BasicPreprocessor(BasePreprocessor):
    def run(self, audio_path: str) -> tuple[np.ndarray, float]:
        y, sr = librosa.load(audio_path, sr=None)
        y = remove_noise(y)
        y = emphasize_audio(y)
        y = normalize_audio(y)
        y = librosa.resample(y, orig_sr=sr, target_sr=self.sr)

        return y, self.sr


class SpectralPreprocessor(BasePreprocessor):
    def run(self, audio_path: str) -> tuple[np.ndarray, float]:
        y, sr = librosa.load(audio_path, sr=None)
        print(f"{audio_path} - shape: {y.shape}, sr: {sr}")
        # 노이즈 제거
        y = spectral_subtraction(y, sr)

        # 이산 웨이블릿 변환
        coeffs = pywt.wavedec(y, wavelet='db4', mode='per')
        y = pywt.waverec(coeffs, wavelet='db4', mode='per')

        # 음성 강조
        y = emphasize_audio(y)

        # 정규화
        y = normalize_audio(y)

        # 리샘플링 (선택 사항)
        y = librosa.resample(y, orig_sr=sr, target_sr=self.sr)
        print(f"{audio_path} - resampled - shape: {y.shape}, sr: {self.sr}")
        return y, self.sr
