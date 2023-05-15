import tensorflow as tf
import numpy as np
from tensorflow.keras.utils import custom_object_scope
from tensorflow.keras.models import load_model
from keras import backend as K
import librosa

def get_spectrogram_image(waveform, sr=22050):
    """
    Transforms a 'waveform' into a 'spectrogram image', adding padding if needed.
    """
    waveform = tf.cast(waveform, tf.float32)
    spectrogram = tf.signal.stft(
        waveform, frame_length=1024, frame_step=256, fft_length=1024
    )
    spectrogram = tf.abs(spectrogram)

    num_spectrogram_bins = spectrogram.shape[-1]
    lower_edge_hertz, upper_edge_hertz, num_mel_bins = 80.0, 7600.0, 80
    linear_to_mel_weight_matrix = tf.signal.linear_to_mel_weight_matrix(
        num_mel_bins, num_spectrogram_bins, sr, lower_edge_hertz, upper_edge_hertz
    )
    mel_spectrogram = tf.tensordot(spectrogram, linear_to_mel_weight_matrix, 1)
    mel_spectrogram.set_shape(
        spectrogram.shape[:-1].concatenate(linear_to_mel_weight_matrix.shape[-1:])
    )

    mel_spectrogram = tf.expand_dims(mel_spectrogram, -1)

    sample = tf.image.resize(mel_spectrogram, [224, 512])
    sample = tf.image.grayscale_to_rgb(sample)
    return sample


def process_audio(file_path):
    """
    Load an audio file and transform it into a spectrogram image.
    """
    sound, sample_rate = librosa.load(file_path)
    audio_trimmed, _ = librosa.effects.trim(sound, top_db=20)
    spectrogram_image = get_spectrogram_image(audio_trimmed)
    spectrogram_image = tf.expand_dims(spectrogram_image, 0)

    return spectrogram_image