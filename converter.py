import os
import sys
import subprocess
import uuid
from datetime import datetime

# Attempt to import pydub, install if not available
try:
    from pydub import AudioSegment
except ImportError:
    print("pydub is not installed. Attempting to install it now...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pydub"])
        from pydub import AudioSegment

        print("pydub installed successfully.")
    except subprocess.CalledProcessError:
        print("Failed to install pydub. Please install it manually using 'pip install pydub'.")
        sys.exit(1)


def merge_voice_memos(directory, ffmpeg_path=None):
    # Set ffmpeg path if provided
    if ffmpeg_path:
        AudioSegment.converter = ffmpeg_path
        AudioSegment.ffmpeg = ffmpeg_path
        AudioSegment.ffprobe = ffmpeg_path.replace('ffmpeg', 'ffprobe')

    # Verify ffmpeg is accessible
    try:
        AudioSegment.ffmpeg
    except Exception:
        print("ffmpeg not found. Please ensure ffmpeg is installed and the path is correct.")
        print(
            "Download ffmpeg from https://ffmpeg.org/download.html and add it to your PATH or provide the path as a parameter.")
        sys.exit(1)

    # List all .dat files in the directory
    files = sorted([file for file in os.listdir(directory) if file.lower().endswith('.dat')])

    if not files:
        print("No .dat files found in the specified directory.")
        sys.exit(1)

    merged_audio = AudioSegment.empty()
    for file in files:
        file_path = os.path.join(directory, file)
        try:
            # Attempt to convert .dat to audio. Adjust format if necessary.
            audio_segment = AudioSegment.from_file(file_path, format='m4a')  # Adjust 'm4a' if needed
            merged_audio += audio_segment
            print(f"Processed {file}")
        except Exception as e:
            print(f"Failed to process {file}: {e}")

    # Generate a unique output file name with timestamp and UUID
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    unique_id = uuid.uuid4().hex[:6]
    output_file = os.path.join(directory, f"merged_audio_{timestamp}_{unique_id}.mp3")

    # Export merged audio as MP3
    try:
        merged_audio.export(output_file, format='mp3')
        print(f"Merged audio exported to: {output_file}")
    except Exception as e:
        print(f"Failed to export merged audio: {e}")
        sys.exit(1)


def main():
    import argparse

    parser = argparse.ArgumentParser(description="MemoFusion: Convert and merge WhatsApp voice memos.")
    parser.add_argument(
        "directory",
        type=str,
        help="Path to the directory containing .dat voice memo files."
    )
    parser.add_argument(
        "--ffmpeg",
        type=str,
        default=None,
        help="Path to the ffmpeg executable (e.g., C:\\ffmpeg\\bin\\ffmpeg.exe). If not provided, ffmpeg must be in the system PATH."
    )

    args = parser.parse_args()

    if not os.path.isdir(args.directory):
        print(f"The directory {args.directory} does not exist.")
        sys.exit(1)

    merge_voice_memos(args.directory, args.ffmpeg)


if __name__ == "__main__":
    main()
