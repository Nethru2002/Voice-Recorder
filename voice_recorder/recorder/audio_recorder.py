import sounddevice as sd
import numpy as np
import wave
from scipy.signal import butter, lfilter
import noisereduce as nr
from .exceptions import AudioRecorderError

class AudioRecorder:
    def __init__(self, sample_rate=44100, channels=1):
        self.sample_rate = sample_rate
        self.channels = channels
        self.is_recording = False
        self.recording = None

    def _butter_highpass(self, cutoff, order=5):
        """Design a high-pass filter to remove low-frequency noise."""
        nyquist = 0.5 * self.sample_rate
        normal_cutoff = cutoff / nyquist
        b, a = butter(order, normal_cutoff, btype='high', analog=False)
        return b, a

    def _apply_highpass(self, data, cutoff=100):
        """Apply high-pass filter to remove rumble and hum."""
        b, a = self._butter_highpass(cutoff)
        return lfilter(b, a, data)

    def _reduce_noise(self, audio):
        """Apply noise reduction using noisereduce."""
        return nr.reduce_noise(
            y=audio,
            sr=self.sample_rate,
            stationary=True,  # Better for constant background noise
            prop_decrease=0.9  # Aggressive noise reduction
        )

    def record(self, duration, filename):
        if self.is_recording:
            raise AudioRecorderError("Already recording!")

        print("🔊 Recording...")
        self.is_recording = True

        # Record audio
        self.recording = sd.rec(
            int(duration * self.sample_rate),
            samplerate=self.sample_rate,
            channels=self.channels,
            dtype='float32'
        )
        sd.wait()  # Block until recording is done
        self.is_recording = False

        # Process audio
        audio_data = self.recording.flatten()
        filtered_audio = self._apply_highpass(audio_data)  # Remove low-frequency noise
        clean_audio = self._reduce_noise(filtered_audio)  # Reduce background noise

        # Save as 16-bit WAV
        int16_audio = (clean_audio * 32767).astype(np.int16)
        with wave.open(filename, 'wb') as wf:
            wf.setnchannels(self.channels)
            wf.setsampwidth(2)  # 16-bit = 2 bytes
            wf.setframerate(self.sample_rate)
            wf.writeframes(int16_audio.tobytes())

    def stop(self):
        if self.is_recording:
            sd.stop()
            self.is_recording = False