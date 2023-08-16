import librosa
import numpy as np


# 노이즈 제거 함수
def remove_noise(audio):
    noise_reduced_audio = librosa.effects.remix(audio, intervals=librosa.effects.split(audio, top_db=20))
    return noise_reduced_audio


# 스펙트럼 서브트랙션을 사용한 노이즈 제거 함수
def spectral_subtraction(audio, sr):
    noise_est = np.mean(audio)
    _, spectral_noise = librosa.magphase(librosa.stft(audio))
    spectral_noise = np.abs(np.mean(spectral_noise, axis=1))

    S = librosa.stft(audio)
    magnitude, phase = librosa.magphase(S)

    magnitude -= noise_est * spectral_noise[:, np.newaxis]
    magnitude = np.maximum(magnitude, 0.0)

    noise_reduced_audio = librosa.istft(magnitude * phase)
    return noise_reduced_audio



# 음성 강조 함수
def emphasize_audio(audio, alpha=0.97):
    pre_emphasis = np.append(audio[0], audio[1:] - alpha * audio[:-1])
    return pre_emphasis


# 정규화 함수
def normalize_audio(audio):
    normalized_audio = audio / np.max(np.abs(audio))
    return normalized_audio
