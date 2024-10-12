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

# Attempt to import tqdm, install if not available
try:
    from tqdm import tqdm
except ImportError:
    print("tqdm is not installed. Attempting to install it now...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "tqdm"])
        from tqdm import tqdm
        print("tqdm installed successfully.")
    except subprocess.CalledProcessError:
        print("Failed to install tqdm. Please install it manually using 'pip install tqdm'.")
        sys.exit(1)

def merge_voice_memos(directory, ffmpeg_path=None, log_file=None):
    # Set ffmpeg path if provided
    if ffmpeg_path:
        if not os.path.isfile(ffmpeg_path):
            error_message = f"FFmpeg executable not found at: {ffmpeg_path}"
            print(error_message)
            if log_file:
                with open(log_file, 'a') as log:
                    log.write(f"{datetime.now()} - ERROR - {error_message}\n")
            sys.exit(1)
        AudioSegment.converter = ffmpeg_path
        AudioSegment.ffmpeg = ffmpeg_path
        AudioSegment.ffprobe = ffmpeg_path.replace('ffmpeg.exe', 'ffprobe.exe')

    # Verify ffmpeg is accessible
    try:
        subprocess.check_output([AudioSegment.converter, "-version"], stderr=subprocess.STDOUT)
    except Exception as e:
        error_message = (
            "FFmpeg not accessible. Please ensure FFmpeg is installed correctly and the path is accurate.\n"
            f"Details: {e}"
        )
        print(error_message)
        if log_file:
            with open(log_file, 'a') as log:
                log.write(f"{datetime.now()} - ERROR - {error_message}\n")
        sys.exit(1)

    # List all .dat files in the directory
    files = sorted([file for file in os.listdir(directory) if file.lower().endswith('.dat')])

    if not files:
        no_files_message = "No .dat files found in the specified directory."
        print(no_files_message)
        if log_file:
            with open(log_file, 'a') as log:
                log.write(f"{datetime.now()} - ERROR - {no_files_message}\n")
        sys.exit(1)

    merged_audio = AudioSegment.empty()
    # Initialize tqdm progress bar
    for file in tqdm(files, desc="Processing files", unit="file"):
        file_path = os.path.join(directory, file)
        try:
            # Attempt to convert .dat to audio. Adjust format if necessary.
            audio_segment = AudioSegment.from_file(file_path, format='m4a')  # Adjust 'm4a' if needed
            merged_audio += audio_segment
            success_message = f"Processed {file}"
            print(success_message)
            if log_file:
                with open(log_file, 'a') as log:
                    log.write(f"{datetime.now()} - INFO - {success_message}\n")
        except Exception as e:
            error_message = f"Failed to process {file}: {e}"
            print(error_message)
            if log_file:
                with open(log_file, 'a') as log:
                    log.write(f"{datetime.now()} - ERROR - {error_message}\n")

    # Generate a unique output file name with timestamp and UUID
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    unique_id = uuid.uuid4().hex[:6]
    output_file = os.path.join(directory, f"merged_audio_{timestamp}_{unique_id}.mp3")

    # Export merged audio as MP3
    try:
        merged_audio.export(output_file, format='mp3')
        success_export = f"Merged audio exported to: {output_file}"
        print(success_export)
        if log_file:
            with open(log_file, 'a') as log:
                log.write(f"{datetime.now()} - INFO - {success_export}\n")
    except Exception as e:
        error_export = f"Failed to export merged audio: {e}"
        print(error_export)
        if log_file:
            with open(log_file, 'a') as log:
                log.write(f"{datetime.now()} - ERROR - {error_export}\n")
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
    parser.add_argument(
        "--log",
        type=str,
        default=None,
        help="Path to the log file. If not provided, a log file will be created in the specified directory."
    )

    args = parser.parse_args()

    if not os.path.isdir(args.directory):
        error_dir = f"The directory {args.directory} does not exist."
        print(error_dir)
        sys.exit(1)

    # Set default log file path if not provided
    if args.log:
        log_file = args.log
    else:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        unique_id = uuid.uuid4().hex[:6]
        log_file = os.path.join(args.directory, f"conversion_log_{timestamp}_{unique_id}.txt")

    # Initialize log file
    with open(log_file, 'a') as log:
        log.write(f"=== MemoFusion Conversion Started at {datetime.now()} ===\n")

    merge_voice_memos(args.directory, args.ffmpeg, log_file)

    with open(log_file, 'a') as log:
        log.write(f"=== MemoFusion Conversion Ended at {datetime.now()} ===\n")

if __name__ == "__main__":
    main()
