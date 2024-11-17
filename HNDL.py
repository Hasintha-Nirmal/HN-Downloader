import ttkbootstrap as ttk
from ttkbootstrap.constants import *
import subprocess
import threading
import os
import tkinter.filedialog as filedialog
import re

# Initialize app with ttkbootstrap theme
app = ttk.Window(themename="darkly")
app.title("HN Downloader")
app.geometry("900x900")
app.minsize(900, 900)

# Disable maximizing by setting the window attributes
app.resizable(False, False)  # Disable resizing in both directions

# Set window style to remove maximize and minimize buttons
app.attributes("-toolwindow", True)

# Global variables
download_process = None

# Functions
def fetch_formats():
    url = url_entry.get("1.0", "end-1c").strip()
    if not url:
        log_message("Please enter a URL first.")
        return

    command = ["yt-dlp", "-F", url]
    log_message(f"Fetching formats for {url}...")

    def run_command():
        result = subprocess.run(command, capture_output=True, text=True)
        log_message(result.stdout)

    threading.Thread(target=run_command).start()

def log_message(message):
    log_text.config(state="normal")
    log_text.insert("end", message + "\n")
    log_text.see("end")
    log_text.config(state="disabled")

def select_download_location():
    folder = filedialog.askdirectory()
    if folder:
        download_location_entry.delete(0, "end")
        download_location_entry.insert(0, folder)

def download_media():
    urls = url_entry.get("1.0", "end-1c").strip().splitlines()
    if not urls:
        log_message("Please enter at least one URL.")
        return

    quality = quality_combobox.get()
    video_format = format_combobox.get()
    audio_format = audio_format_combobox.get()
    download_location = download_location_entry.get()
    audio_only = audio_only_var.get()
    video_only = video_only_var.get()
    cookies = cookies_entry.get("1.0", "end-1c").strip()

    command = ["yt-dlp", "-o", os.path.join(download_location, "%(title)s.%(ext)s")]

    # Handle cookies input
    if cookies:
        command.extend(["--cookies", "cookies.txt"])  # Temporarily write cookies to a file
        with open("cookies.txt", "w") as f:
            f.write(cookies)

    if audio_only:
        command.extend(["--extract-audio", "--audio-format", audio_format])
    elif video_only:
        command.append("-f bestvideo")
    else:
        command.append(f"-f {quality}")
        command.extend(["-S", "ext:" + video_format])

    log_message(f"Starting download for URLs: {urls}")

    # Reset progress bar
    progress_bar['value'] = 0
    progress_bar['maximum'] = 100

    def run_download():
        global download_process
        for url in urls:
            download_process = subprocess.Popen(command + [url], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)

            for line in download_process.stdout:
                log_message(line.strip())
                # Check for progress lines and update progress bar
                progress_match = re.search(r'(\d+)%', line)  # Capture percentage
                if progress_match:
                    percent = int(progress_match.group(1))
                    # Only update if the percentage is greater than the current value
                    if percent > progress_bar['value']:
                        progress_bar['value'] = percent
                        app.update_idletasks()  # Update the UI

            download_process = None

    threading.Thread(target=run_download).start()

def stop_download():
    global download_process
    if download_process and download_process.poll() is None:
        download_process.terminate()
        log_message("Download stopped.")

# Header Label
header_label = ttk.Label(app, text="HN Downloader", font=("Helvetica", 24, "bold"), bootstyle=INFO)
header_label.pack(pady=20)

# URL Entry Section
frame_input = ttk.Frame(app, padding=(10, 5))
frame_input.pack(fill=X, padx=20)
url_label = ttk.Label(frame_input, text="YouTube URLs (one per line):")
url_label.pack(anchor=W)
url_entry = ttk.Text(frame_input, height=5, width=60)
url_entry.pack(fill=X, pady=5)

fetch_button = ttk.Button(frame_input, text="Fetch Formats", bootstyle=SUCCESS, command=fetch_formats)
fetch_button.pack(anchor=E, pady=5)

# Options Section
frame_options = ttk.Frame(app, padding=(10, 5))
frame_options.pack(fill=X, padx=20, pady=10)

# Quality Dropdown
ttk.Label(frame_options, text="Select Quality:").grid(row=0, column=0, sticky=W, padx=5, pady=5)
quality_combobox = ttk.Combobox(frame_options, width=15, values=["best"], state="readonly")
quality_combobox.grid(row=0, column=1, padx=5, pady=5)

# Video Format Dropdown
ttk.Label(frame_options, text="Convert Video to Format:").grid(row=1, column=0, sticky=W, padx=5, pady=5)
format_combobox = ttk.Combobox(frame_options, width=15, values=["mp4", "mkv", "avi"], state="readonly")
format_combobox.set("mp4")
format_combobox.grid(row=1, column=1, padx=5, pady=5)

# Audio Format Dropdown
ttk.Label(frame_options, text="Convert Audio to Format:").grid(row=2, column=0, sticky=W, padx=5, pady=5)
audio_format_combobox = ttk.Combobox(frame_options, width=15, values=["mp3", "m4a", "opus"], state="readonly")
audio_format_combobox.set("mp3")
audio_format_combobox.grid(row=2, column=1, padx=5, pady=5)

# Audio-Only and Video-Only Checkboxes
audio_only_var = ttk.BooleanVar()
video_only_var = ttk.BooleanVar()
audio_check = ttk.Checkbutton(frame_options, text="Download Audio Only", variable=audio_only_var)
video_check = ttk.Checkbutton(frame_options, text="Download Video Only", variable=video_only_var)
audio_check.grid(row=3, column=0, sticky=W, padx=5, pady=5)
video_check.grid(row=3, column=1, sticky=W, padx=5, pady=5)

# Download Location
ttk.Label(frame_options, text="Download Location:").grid(row=4, column=0, sticky=W, padx=5, pady=5)
download_location_entry = ttk.Entry(frame_options, width=50)
download_location_entry.grid(row=4, column=1, padx=5, pady=5)

# Set default download location to Windows Downloads folder
default_download_location = os.path.join(os.path.expanduser("~"), "Downloads")
download_location_entry.insert(0, default_download_location)  # Insert the default path
select_location_button = ttk.Button(frame_options, text="Browse", command=select_download_location)
select_location_button.grid(row=4, column=2, padx=5, pady=5)


# Cookies Entry
ttk.Label(frame_options, text="Cookies (paste here):").grid(row=5, column=0, sticky=W, padx=5, pady=5)
cookies_entry = ttk.Text(frame_options, height=5, width=60)
cookies_entry.grid(row=5, column=1, padx=5, pady=5)

# Download Controls
frame_controls = ttk.Frame(app, padding=(10, 5))
frame_controls.pack(fill=X, padx=20, pady=10)

download_button = ttk.Button(frame_controls, text="Download", bootstyle=PRIMARY, command=download_media)
stop_button = ttk.Button(frame_controls, text="Stop", bootstyle=DANGER, command=stop_download)
download_button.pack(side=LEFT, padx=10)
stop_button.pack(side=RIGHT, padx=10)

# Progress Bar
progress_bar = ttk.Progressbar(app, orient=HORIZONTAL, length=400, mode='determinate')
progress_bar.pack(pady=10)

# Progress and Log Section
frame_log = ttk.Frame(app, padding=(10, 5))
frame_log.pack(fill=BOTH, expand=True, padx=20, pady=10)

log_text = ttk.Text(frame_log, height=10)
log_text.pack(fill=BOTH, expand=True)
log_text.config(state="disabled")

# Run the app
app.mainloop()
