import os
import tempfile
import numpy as np
from scipy.io import wavfile

class BioClassifier:
    def __init__(self, min_confidence=0.7, lat=None, lon=None):
        self.min_confidence = min_confidence
        self.lat = lat
        self.lon = lon
        self.has_birdnet = False
        try:
            from birdnetlib import Recording
            from birdnetlib.analyzer import Analyzer
            self.analyzer = Analyzer()
            self.Recording = Recording
            self.has_birdnet = True
        except ImportError:
            pass

    def analyze_audio(self, audio_data: np.ndarray, sample_rate=48000):
        if not self.has_birdnet:
            return None
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as f:
            temp_path = f.name
            scaled = np.int16(audio_data * 32767)
            wavfile.write(temp_path, sample_rate, scaled)
        try:
            recording = self.Recording(self.analyzer, temp_path, lat=self.lat, lon=self.lon, min_conf=self.min_confidence)
            recording.analyze()
            if recording.detections:
                best = max(recording.detections, key=lambda x: x["confidence"])
                return best["common_name"], best["confidence"]
        finally:
            if os.path.exists(temp_path):
                os.remove(temp_path)
        return None
