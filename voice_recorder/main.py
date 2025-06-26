import os
import time
from recorder.audio_recorder import AudioRecorder
from recorder.utils import validate_output_dir

def main():
    print("=== Python Voice Recorder (Noise-Reduced) ===")
    output_dir = "recordings"
    validate_output_dir(output_dir)

    recorder = AudioRecorder()

    while True:
        print("\nOptions:")
        print("1. Start Recording")
        print("2. Exit")

        choice = input("Choose (1/2): ").strip()

        if choice == "1":
            try:
                duration = float(input("Duration (seconds): "))
                filename = input("Filename (without .wav): ") + ".wav"
                filepath = os.path.join(output_dir, filename)

                print(f"\n🎤 Recording for {duration} seconds... (Press Ctrl+C to stop early)")
                recorder.record(duration, filepath)
                print(f"✅ Saved to: {filepath}")
            except KeyboardInterrupt:
                print("\n⏹ Stopped early!")
                recorder.stop()
            except Exception as e:
                print(f"❌ Error: {e}")
        elif choice == "2":
            print("Exiting...")
            break
        else:
            print("Invalid choice!")

if __name__ == "__main__":
    main()