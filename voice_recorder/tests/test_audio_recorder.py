import pytest
import os
from recorder.audio_recorder import AudioRecorder

TEST_FILE = "test_recording.wav"

@pytest.fixture
def recorder():
    return AudioRecorder()

def test_recording(recorder):
    recorder.record(1.0, TEST_FILE)
    assert os.path.exists(TEST_FILE)
    os.remove(TEST_FILE)  # Cleanup