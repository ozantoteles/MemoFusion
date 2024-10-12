# MemoFusion

**MemoFusion** is a Python tool designed to convert and merge WhatsApp voice memos from `.dat` format into a single, high-quality MP3 file. Simplify your voice memo management by seamlessly combining multiple recordings into one convenient file.

## Features

- **Convert `.dat` Files**: Transforms WhatsApp's `.dat` voice memos into standard audio formats.
- **Merge Audio Files**: Combines multiple voice memos into a single MP3 file.
- **Automatic Library Installation**: Attempts to install required Python libraries if they are missing.
- **Unique Output Naming**: Ensures each merged file has a unique name to prevent overwriting.
- **Conversion Logging**: Generates a detailed log file for each conversion process.
- **User-Friendly**: Simple command-line interface with clear instructions and error messages.

## Installation

### Prerequisites

- **Python 3.6 or higher**: Ensure Python is installed on your system. [Download Python](https://www.python.org/downloads/)
- **FFmpeg**: Required for audio processing.
  - **Download FFmpeg**: [ffmpeg.org](https://ffmpeg.org/download.html)
  - **Installation**:
    1. **Download FFmpeg**: Visit [ffmpeg.org](https://ffmpeg.org/download.html) and download the appropriate version for your system.
    2. **Extract FFmpeg**: Extract the downloaded archive to a directory (e.g., `C:\ffmpeg`).
    3. **Add FFmpeg to PATH**:
       - Open **System Properties** > **Advanced** > **Environment Variables**.
       - Under **System variables**, find and select the **Path** variable, then click **Edit**.
       - Click **New** and add the path to the `ffmpeg` `bin` folder, e.g., `C:\ffmpeg\bin`.
       - Click **OK** to apply the changes.
    4. **Verify Installation**:
       - Open Command Prompt and type `ffmpeg -version`. You should see version information if installed correctly.

### Clone the Repository

```bash
git clone https://github.com/ozantoteles/MemoFusion.git
cd MemoFusion
```

## Usage

Place Your .dat Files:

Ensure all WhatsApp .dat voice memos you wish to merge are in a single directory.
Run the Script:

```bash
python converter.py "path_to_your_dat_files" --ffmpeg "path_to_ffmpeg_executable" --log "path_to_log_file"
```

Parameters:

path_to_your_dat_files: Replace with the path to the directory containing your .dat files.
--ffmpeg: (Optional) Path to the ffmpeg executable. If ffmpeg is added to your system PATH, this parameter can be omitted.
--log: (Optional) Path to the log file. If not provided, a log file will be created in the specified directory with a unique name.
Examples:

With ffmpeg in PATH and default log file location:
```bash
python converter.py "C:\Users\ozantoteles\Desktop\photonext lab recordings"
```
Specifying ffmpeg path and custom log file location:

```bash
python converter.py "C:\Users\ozantoteles\Desktop\photonext lab recordings" --ffmpeg "C:\ffmpeg\bin\ffmpeg.exe" --log "C:\Users\ozantoteles\Desktop\conversion_log.txt"
```

Output:

The merged MP3 file will be saved in the specified directory with a unique name, e.g., merged_audio_20241012_153045_a1b2c3.mp3.
A conversion log file will be created detailing the conversion process, including any errors encountered.
Conversion Logging
MemoFusion generates a log file for each conversion process, providing detailed information about the operation. The log includes:

Start and End Timestamps: Marks the beginning and completion of the conversion process.
Processed Files: Lists each .dat file processed successfully.
Errors: Details any issues encountered during file processing or export.
Example Log Entry

```yaml
=== MemoFusion Conversion Started at 2024-04-27 10:00:00 ===
2024-04-27 10:00:01 - INFO - Processed memo1.dat
2024-04-27 10:00:02 - INFO - Processed memo2.dat
2024-04-27 10:00:03 - ERROR - Failed to process memo3.dat: [Error Details]
2024-04-27 10:00:04 - INFO - Merged audio exported to: C:\Users\ozantoteles\Desktop\photonext lab recordings\merged_audio_20240427_100003_a1b2c3.mp3
=== MemoFusion Conversion Ended at 2024-04-27 10:00:04 ===
```

## Error Handling
FFmpeg Not Found:

If ffmpeg is not installed or not found in the specified path, the script will prompt you to install it.
Ensure ffmpeg is correctly installed and the path is added to your system's PATH variable or provided via the --ffmpeg parameter.
No .dat Files Found:

The script will notify you if no .dat files are found in the specified directory.
Library Installation Issues:

If pydub or tqdm fails to install automatically, manually install them using:
```bash
pip install pydub tqdm
```

## Contributing
Contributions are welcome! Please fork the repository and submit a pull request for any enhancements or bug fixes.

