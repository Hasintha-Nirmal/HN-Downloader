# HN Downloader

A modern, user-friendly desktop application for downloading videos and audio from YouTube using yt-dlp with a clean dark-themed interface.

<img src="https://raw.githubusercontent.com/Hasintha-Nirmal/HN-Downloader/refs/heads/main/images/Screenshot.png" alt="Screenshot of HN Downloader" width="500" >


## Features

- Download videos in multiple formats (MP4, MKV, AVI)
- Extract audio in various formats (MP3, M4A, Opus)
- Batch download support (multiple URLs)
- Video quality selection
- Audio-only and video-only download options
- Custom download location
- Cookie support for private/restricted videos
- Progress tracking with visual progress bar
- Dark theme interface
- Format information fetching
- Download cancellation support

## Requirements

- Python 3.6+
- FFmpeg
- Required Python packages (installed automatically):
  - ttkbootstrap
  - yt-dlp
  - ffmpeg-python

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/hn-downloader.git
cd hn-downloader
```

2. Run the setup script:
```bash
python setup.py
```

The setup script will:
- Install required Python packages
- Set up yt-dlp
- Download and configure FFmpeg if not already installed
- Add FFmpeg to system PATH (Windows only)

**Note:** After installation on Windows, you may need to restart your terminal or command prompt for PATH changes to take effect.

## Usage

1. Launch the application:
```bash
python HNDL.py
```

2. Enter YouTube URLs (one per line) in the text area.

3. Configure download options:
   - Select video quality
   - Choose output format for video/audio
   - Toggle audio-only or video-only download
   - Set download location
   - Add cookies if needed for restricted content

4. Click "Fetch Formats" to see available format options for the URLs.

5. Click "Download" to start downloading.

6. Monitor progress in the log window and progress bar.

7. Use the "Stop" button to cancel ongoing downloads.

## Interface Guide

- **URLs Input**: Enter one or more YouTube URLs, each on a new line
- **Quality Selection**: Choose video quality (defaults to best available)
- **Format Selection**: 
  - Video formats: MP4, MKV, AVI
  - Audio formats: MP3, M4A, Opus
- **Download Options**:
  - Audio Only: Extract only audio from videos
  - Video Only: Download video without audio
- **Location**: Choose where to save downloaded files
- **Cookies**: Paste cookies for accessing restricted content
- **Controls**:
  - Fetch Formats: View available formats for URLs
  - Download: Start downloading
  - Stop: Cancel current download

## Error Handling

- The application validates URLs before downloading
- Displays detailed error messages in the log window
- Handles network interruptions gracefully
- Prevents multiple simultaneous downloads

## Contributing

Feel free to submit issues, fork the repository, and create pull requests for any improvements.

## License

[MIT License](LICENSE)

## Acknowledgments

- Built with [yt-dlp](https://github.com/yt-dlp/yt-dlp)
- UI powered by [ttkbootstrap](https://github.com/israel-dryer/ttkbootstrap)
- Uses [FFmpeg](https://ffmpeg.org/) for media processing

## Disclaimer

This tool is for personal use only. Respect YouTube's terms of service and content creators' rights when downloading videos.
