import numpy as np
import sounddevice as sd

class AudioRecorder:
    def __init__(self, sample_rate=48000, chunk_seconds=3.0, device=None):
        self.sample_rate = sample_rate
        self.chunk_seconds = chunk_seconds
        self.chunk_samples = int(sample_rate * chunk_seconds)
        self.device = device

    def record_chunk(self) -> np.ndarray:
        audio = sd.rec(
            frames=self.chunk_samples,
            samplerate=self.sample_rate,
            channels=1,
            dtype="float32",
            device=self.device
        )
        sd.wait()
        return audio.flatten()
